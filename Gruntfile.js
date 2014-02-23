/* jshint indent:2,maxstatements:false */
/* global module,require */

/*
This file configures common tasks when developing on slingsby.

Static files like css and js needs to be 'compiled' (minified and concatenated) before they can be served,
and SASS needs to be compiled to CSS and so on. In broad steps this process is first collecting all files needed
in the ./tmp directory, and then building the final set of files into ./build, which is also served by the
devserver. Some processes might skip the ./tmp directory entirely, like the imagemin step which takes the
graphics directly from slingsby/static-src to build/static.
*/
module.exports = function (grunt) {
  "use strict";

  // Load all grunt tasks defined in package.json
  require('load-grunt-tasks')(grunt);

  // Project configuration.
  grunt.initConfig({


    pkg: grunt.file.readJSON('package.json'),

    /*
     * Compile all .hbs (handlebars) templates to a shared file
     */
    handlebars: {
      compile: {
        options: {
          namespace: "slingsby.templates",
          // Transform paths to sensible template names -> Extract filename, remove ext
          processName: function (name) {
            var path = name.split('/');
            var filename = path[path.length - 1];
            var parts = filename.split('.');
            parts.pop(); //removes extension
            return parts.join('.');
          }
        },
        files: {
          ".tmp/static/js/handlebars_templates.js": "slingsby/*/templates/handlebars/*.hbs"
        }
      }
    },

    /*
    * Compile SASS stylesheets.
    */
    compass: {
      dist: {
        options: {
          sassDir: '.tmp/sass/',
          cssDir: 'build/static/stylesheets',
          outputStyle: "compressed"
        }
      }
    },

    copy: {
      other: {
        files: [
          {
            expand: true,
            src: [
              'favicon.ico',
              'robots.txt',
            ],
            cwd: 'slingsby/static-src/',
            dest: 'build/static',
          }
        ]
      },
      tmpToBuild: {
        files: [{expand: true, src: ['**'], cwd: '.tmp/static', dest: 'build/static/'}]
      },
      sass: {
        files: [{expand: true, src: ['**'], cwd: 'slingsby/static-src/sass', dest: '.tmp/sass'}]
      },
      js: {
        files: [{expand: true, src: ['**'], cwd: 'slingsby/static-src/js', dest: '.tmp/static/js'}]
      },
      libsToTmp: {
        files: [{expand: true, src: ['**'], cwd: 'bower_components', dest: '.tmp/static/libs'}]
      },
      libsToBuild: {
        files: [{expand: true, src: ['**'], cwd: '.tmp/static/libs', dest: 'build/static/libs'}]
      },
    },

    jshint: {
      options: {
        'jshintrc': '.jshintrc',
      },
      all: [
        'Gruntfile.js',
        'slingsby/static-src/js/*.js',
        'slingsby/**/static/js/*.js',

        // Ignore the built stuff
        '!slingsby/static/**',
      ]
    },

    /*
    * Recompile css, update static dir and reload on template changes.
    */
    watch: {
      options: {
        livereload: true
      },
      css: {
        files: ['slingsby/static-src/stylesheets/sass/*.scss'],
        tasks: ['compass']
      },
      js: {
        files: ['<%= jshint.all %>'],
        tasks: ['jshint', 'shell:collectstatic', 'copy:tmpToBuild']
      },
      templates: {
        files: ['slingsby/**/templates/*.html'],
        tasks: []
      },
      handlebars: {
        files: ['slingsby/**/handlebars/*.hbs'],
        tasks: ['handlebars']
      },
      python: {
        files: ['slingsby/**/*.py']
      }
    },

    pylint: {
      slingsby: {
        options: {
          rcfile: '.pylintrc',
        },
        src: ['slingsby', '*.py', 'tools/*.py'],
      }
    },

    // Shortcuts for some often used commands
    shell: {
      options: {
        stderr: true,
      },
      buildPython: {
        command: 'python setup.py sdist --dist-dir build --formats gztar',
      },
      provision: {
        options: {
          stdout: true,
        },
        command: [
          'python ./tools/dump_secure_env_vars_to_pillar.py',
          'tar czf build/salt_and_pillar.tar.gz salt pillar',
          'scp build/salt_and_pillar.tar.gz slingsby:/tmp/',
          'ssh slingsby "sudo tar xf /tmp/salt_and_pillar.tar.gz -C /srv/',
          'sudo salt-call --local state.highstate --force-color',
          'rm /tmp/salt_and_pillar.tar.gz"'
        ].join('&&'),
      },
      collectstatic: {
        command: function () {
          // The build/static directory needs to exist for the collectstatic command to succeed
          grunt.file.mkdir('build/static');
          return 'python manage.py collectstatic --settings dev_settings --noinput';
        },
      },
      buildStatic: {
        command: [
          'cd build/static',
          'tar czf ../static_files.tar.gz *',
        ].join(' && '),
      },
      deployCode: {
        options: {
          stdout: true
        },
        command: [
          'scp build/slingsby-1.0.0.tar.gz slingsby:/tmp/slingsby.tar.gz',
          'ssh slingsby "sudo /srv/ntnuita.no/venv/bin/pip uninstall slingsby -y || echo',
          'sudo /srv/ntnuita.no/venv/bin/pip install /tmp/slingsby.tar.gz',
          'sudo restart uwsgi',
          'rm /tmp/slingsby.tar.gz"'
        ].join(' && '),
      },
      deployStatic: {
        options: {
          stdout: true,
        },
        command: [
          'scp build/static_files.tar.gz slingsby:/tmp/static_files.tar.gz',
          'ssh slingsby "cd /srv/ntnuita.no/static/',
          'test -d <%= grunt.option("slingsby-version") %> || sudo mkdir <%= grunt.option("slingsby-version") %>',
          'sudo tar xf /tmp/static_files.tar.gz -C <%= grunt.option("slingsby-version") %>',
          'sudo chown -R root:www <%= grunt.option("slingsby-version") %>',
          'find /srv/ntnuita.no/static -type f -print0 | xargs -0 sudo chmod 444',
          'find /srv/ntnuita.no/static -type d -print0 | xargs -0 sudo chmod 555',
          'rm /tmp/static_files.tar.gz"'
        ].join(' && '),
      },
      devserver: {
        options: {
          stdout: true,
        },
        command: 'python manage.py runserver --settings secret_settings <%= grunt.option("port") || 80 %>'
      },
      test: {
        command: 'python manage.py test --settings dev_settings slingsby.general.tests',
      }
    },

    clean: {
      options: {
        'no-write': false,
      },
      python: [
        'slingsby/**/*.pyc',
      ],
      builds: [
        'build',
        'slingsby.egg-info',
        '.tmp',
      ]
    },

    concurrent: {
      server: {
        tasks: ['watch', 'shell:devserver'],
        options: {
          logConcurrentOutput: true,
        }
      }
    },

    // This task configures the uglify task with the files specified in build blocks
    // in our html files.
    useminPrepare: {
      options: {
        dest: 'build/static',
        root: '.tmp',
        flow: {
          html: {
            steps: {'js': ['uglifyjs']},
            post: {}
          }
        }
      },
      html: 'slingsby/**/templates/**/*.html',
    },

    imagemin: {
      static: {
        files: [{
          expand: true,
          cwd: 'slingsby/static-src/gfx',
          src: [
            '**/*.{png,jpg,gif}',

            // Ignore originals
            '!originals/**',
          ],
          dest: 'build/static/gfx',
        }]
      }
    },

    cssUrlEmbed: {
      css: {
        options: {
          baseDir: 'slingsby/static-src/',
        },
        files: {
          '.tmp/sass/_fonts.scss': 'slingsby/static-src/sass/_fonts.scss',
        }
      }
    },

    uglify: {
      dist: {
        files: {
          'build/static/js/socialSummary.min.js': '.tmp/static/js/socialSummary.js',
          'build/static/js/widgEditor.min.js': '.tmp/static/js/widgEditor.js',
        }
      }
    },

  });


  // Default task
  grunt.registerTask('default', [
    'server',
  ]);
  grunt.registerTask('lint', [
    'jshint',
    'pylint',
  ]);
  grunt.registerTask('test', [
    'shell:test',
  ]);
  grunt.registerTask('deploy', [
    'shell:deployStatic',
    'shell:deployCode',
  ]);
  grunt.registerTask('pybuild', [
    'shell:buildPython',
  ]);
  grunt.registerTask('provision', [
    'shell:provision',
  ]);
  grunt.registerTask('server', [
    'concurrent:server',
  ]);
  grunt.registerTask('build', [
    'clean',
    'copy:libsToTmp',
    'shell:collectstatic',
    'buildStyles',
    'buildScripts',
    'imagemin',
    'copy:tmpToBuild',
    'copy:other',
    'copy:libsToBuild',
    'shell:buildStatic',
    'pybuild',
  ]);
  grunt.registerTask('buildStyles', [
    'copy:sass',
    'cssUrlEmbed',
    'compass',
  ]);
  grunt.registerTask('buildScripts', [
    'useminPrepare',
    'copy:js',
    'handlebars',
    'uglify',
  ]);
};

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
  /* jshint camelcase: false */

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
          ".tmp/handlebars_templates.js": "slingsby/*/templates/handlebars/*.hbs"
        }
      }
    },

    /*
    * Compile SASS stylesheets.
    */
    compass: {
      dist: {
        options: {
          sassDir: 'slingsby/static-src/sass/',
          cssDir: '.tmp/static/stylesheets',
          outputStyle: 'compressed',
          importPath: ['.tmp/sass'],
        }
      }
    },

    /* Needed because django can't serve out of the same directory it collects static files to */
    copy: {
      tmpToBuild: {
        files: [{
          expand: true,
          src: ['**'],
          cwd: '.tmp/static',
          dest: 'build/static/'
        }]
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
        tasks: ['compass', 'clean:build', 'copy:tmpToBuild']
      },
      js: {
        files: ['<%= jshint.all %>'],
        tasks: ['uglify', 'clean:build', 'copy:tmpToBuild']
      },
      templates: {
        files: ['slingsby/**/templates/*.html'],
        tasks: []
      },
      handlebars: {
        files: ['slingsby/**/handlebars/*.hbs'],
        tasks: ['handlebars', 'uglify', 'clean:build', 'copy:tmpToBuild']
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
          return 'python manage.py collectstatic --noinput';
        },
      },
      packageStatic: {
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
          'ssh slingsby "sudo /srv/ntnuita.no/venv/bin/pip install --upgrade /tmp/slingsby.tar.gz',
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
          'ssh slingsby "cd /srv/ntnuita.no',
          'sudo tar xf /tmp/static_files.tar.gz -C static',
          'sudo chown -R root:www static',
          'find static -type f -print0 | xargs -0 sudo chmod 444',
          'find static -type d -print0 | xargs -0 sudo chmod 555',
          'rm /tmp/static_files.tar.gz"'
        ].join(' && '),
      },
      devserver: {
        options: {
          stdout: true,
        },
        command: 'python manage.py runserver --settings secret_settings <%= grunt.option("port") || 80 %>'
      },
    },

    clean: {
      options: {
        'no-write': false,
      },
      python: [
        'slingsby/**/*.pyc',
        'slingsby.egg-info',
      ],
      build: [
        'build',
      ],
      tmp: [
        '.tmp',
      ],
      serverAssets: [
        'sligsby/server-assets',
      ],
    },

    concurrent: {
      server: {
        tasks: ['watch', 'shell:devserver'],
        options: {
          logConcurrentOutput: true,
        }
      }
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
          dest: '.tmp/static/gfx',
        }]
      }
    },

    filerev: {
      options: {
        algorithm: 'md5',
        length: 8,
      },
      gfx: {
        src: 'build/static/gfx/**/*.{png,jpg,gif}',
      },
      styles: {
        src: 'build/static/stylesheets/*.css',
      },
      js: {
        src: 'build/static/js/*.js',
      },
      misc: {
        src: [
          'build/static/favicon.ico',
          'build/static/robots.txt',
        ],
      },
    },

    // Dumps filerev results to disk
    filerev_assets: {
      dist: {
        options: {
          dest: 'slingsby/server-assets/filerevs.json',
          cwd: 'build/static/',
          prettyPrint: true,
        }
      }
    },

    cssUrlEmbed: {
      css: {
        options: {
          baseDir: 'slingsby/static-src/',
        },
        files: {
          '.tmp/sass/_fonts.scss': 'slingsby/static-src/sass/_fonts_separate.scss',
        }
      }
    },

    uglify: {
      dist: {
        files: {
          '.tmp/static/js/main.min.js': [
            'bower_components/jquery/jquery.js',
            'slingsby/general/static/js/main.js',
          ],
          '.tmp/static/js/articles.min.js': [
            'bower_components/handlebars/handlebars.runtime.js',
            '.tmp/handlebars_templates.js',
            'bower_components/moment/moment.js',
            'bower_components/moment/lang/nb.js',
            'slingsby/articles/static/js/articles.js',
          ],
          '.tmp/static/js/musikk.min.js': [
            'slingsby/musikk/static/js/musikk.js',
          ],
          '.tmp/static/js/event_detail.min.js': [
            'bower_components/moment/moment.js',
            'slingsby/events/static/js/event_detail.js',
          ],
          'build/static/js/socialSummary.min.js': 'slingsby/general/static/js/socialSummary.js',
          'build/static/js/widgEditor.min.js': 'slingsby/general/static/js/widgEditor.js',
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
  grunt.registerTask('rev-files', [
    'filerev',
    'filerev_assets',
  ]);
  grunt.registerTask('prep', [
    'clean:build',
    'shell:collectstatic',
    'buildStyles',
    'buildScripts',
    'imagemin',
    'copy:tmpToBuild',
  ]);
  grunt.registerTask('build', [
    'clean',
    'prep',
    'rev-files',
    'shell:packageStatic',
    'pybuild',
  ]);
  grunt.registerTask('buildStyles', [
    'cssUrlEmbed',
    'compass',
  ]);
  grunt.registerTask('buildScripts', [
    'handlebars',
    'uglify',
  ]);
};

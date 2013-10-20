/* jshint indent:2,maxstatements:false */
/* global module,require */
module.exports = function (grunt) {
  "use strict";

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    /*
     * Compile all .hbs (handlebars) templates to a shared file
     */
    handlebars: {
      compile: {
        options: {
          namespace: "Handlebars.templates",
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
          "slingsby/static/js/handlebars_templates.js": "**/handlebars/*.hbs"
        }
      }
    },

    /*
    * Compile SASS stylesheets.
    */
    compass: {
      dist: {
        options: {
          sassDir: 'slingsby/static-src/stylesheets/sass/',
          cssDir: 'slingsby/static/stylesheets/',
          outputStyle: "compressed"
        }
      }
    },

    /*
     * Copy the static dir over to the fileserver.
     */
    copy: {
      main: {
        files: [
          {
            expand: true,
            src: ['**/*.*'],
            cwd: 'slingsby/static/',
            dest: '/Volumes/groupswww-1/telemark/static/',
            //dest: '//webedit.ntnu.no/groupswww/telemark/static/'
          }
        ]
      },
      srcToStatic: {
        files: [
          {
            expand: true,
            src: ['**/*.*', '!**/*.scss'],
            cwd: 'slingsby/static-src/',
            dest: 'slingsby/static/'
          }
        ]
      }

    },

    jshint: {
      options: {
        'jshintrc': '.jshintrc',
      },
      all: ['Gruntfile.js', 'slingsby/static-src/js/*.js']
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
        tasks: ['jshint']
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
        src: ['slingsby', 'local_settings.py', 'tools/*.py'],
      }
    },

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
      deploy: {
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
      devserver: {
        options: {
          stdout: true,
        },
        command: 'python manage.py runserver --settings secret_settings 80'
      },
    },

    clean: {
      python: [
        'slingsby/**/*.pyc',
      ],
      builds: [
        'build',
        'slingsby.egg-info',
      ]
    },

    concurrent: {
      server: {
        tasks: ['watch', 'shell:devserver'],
        options: {
          logConcurrentOutput: true,
        }
      }
    }
  });

  // Load all grunt tasks defined in package.json
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  // Default tasks
  grunt.registerTask('default', ['server']);
  grunt.registerTask('lint', ['jshint', 'pylint']);
  grunt.registerTask('build', ['handlebars', 'compass', 'copy:srcToStatic', 'pybuild']);
  grunt.registerTask('deploy', ['shell:deploy']);//, 'copy:main']);
  grunt.registerTask('pybuild', ['clean:builds', 'shell:buildPython']);
  grunt.registerTask('provision', ['shell:provision']);
  grunt.registerTask('server', ['concurrent:server']);

};

/* jshint indent:2 */
/* global module */
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
    }

  });

  grunt.loadNpmTasks('grunt-contrib-handlebars');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default tasks
  grunt.registerTask('build', ['handlebars', 'compass', 'copy:srcToStatic']);
  grunt.registerTask('deploy', ['copy:main']);
  grunt.registerTask('default', ['watch']);

};

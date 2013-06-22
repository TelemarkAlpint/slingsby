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
          "../static/js/handlebars_templates.js": "../**/handlebars/*.hbs"
        }
      }
    },

    /*
    * Compile SASS stylesheets.
    */
    compass: {
      dist: {
        options: {
          sassDir: '../static-src/stylesheets/sass/',
          cssDir: '../static/stylesheets/',
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
            cwd: '../static/',
            dest: '//webedit.ntnu.no/groupswww/telemark/static/'
          }
        ]
      },
      srcToStatic: {
        files: [
          {
            expand: true,
            src: ['**/*.*', '!**/*.scss'],
            cwd: '../static-src/',
            dest: '../static/'
          }
        ]
      }

    },

    jshint: {
      options: {
        "browser": true,
        "bitwise": true,
        "camelcase": true,
        "curly": true,
        "eqeqeq": true,
        "immed": true,
        "indent": 4,
        "latedef": true,
        "newcap": true,
        "noarg": true,
        "noempty": true,
        "regexp": true,
        "undef": true,
        "unused": true,
        "strict": true,
        "trailing": true,
        "maxparams": 3,
        "maxdepth": 3,
        "maxstatements": 10,
        "maxlen": 110,
        "smarttabs": true,
        "white": true,
        globals: {
          jQuery: false
        }
      },
      all: ['Gruntfile.js', '../static-src/js/*.js']
    },

    /*
    * Recompile css, update static dir and reload on template changes.
    */
    watch: {
      options: {
        livereload: true
      },
      css: {
        files: ['../static-src/stylesheets/sass/*.scss'],
        tasks: ['compass']
      },
      js: {
        files: ['<%= jshint.all %>'],
        tasks: ['jshint']
      },
      templates: {
        files: ['../templates/*.html', '../*/templates/*/*.html'],
        tasks: []
      },
      handlebars: {
        files: ['../**/handlebars/*.hbs'],
        tasks: ['handlebars']
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-handlebars');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default tasks
  grunt.registerTask('build', ['handlebars', 'compass', 'copy:srcToStatic', 'copy:main']);
  grunt.registerTask('default', ['watch']);

};
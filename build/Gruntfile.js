module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    /*
     * Compile all .handlebars templates in an app to a shared file for that app, eq. articles.js, or event.js.
     */
    handlebars: {
      compile: {
        options: {
          namespace: "Handlebars.templates",
          processName: function(name){
            var path = name.split('/');
            var filename = path[path.length - 1];
            var parts = filename.split('.');
            parts.pop(); //removes extension
            return parts.join('.');
          },
        },
        files: {
            "../static/js/handlebars_templates.js": "../**/handlebars/*.hbs",
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
                outputStyle: "compressed",
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
              dest: '//webedit.ntnu.no/groupswww/telemark/static/',
          }
        ]
      },
      srcToStatic: {
        files: [
          {
              expand: true,
              src: ['**/*.*', '!**/*.scss'],
              cwd: '../static-src/',
              dest: '../static/',
          }
        ]
      }

    },

    jshint: {
      all: ['../static-src/js/*.js'],
    },

    /*
    * Recompile css, coffeescript and reload on template changes.
    */
    watch: {
      options: {
        livereload: true,
      },
      css: {
        files: ['../static-src/stylesheets/sass/*.scss'],
        tasks: ['compass'],
      },
      js: {
        files: ['../static-src/js/*.js'],
        tasks: []
      },
      templates: {
        files: ['../templates/*.html', '../*/templates/*/*.html'],
        tasks: [],
      },
      handlebars: {
        files: ['../**/handlebars/*.hbs'],
        tasks: ['handlebars'],
      },
    },

  });

  grunt.loadNpmTasks('grunt-contrib-handlebars');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default tasks
  grunt.registerTask('default', ['handlebars', 'compass', 'copy:srcToStatic', 'copy:main']);
  grunt.registerTask('dev', ['handlebars', 'compass', 'copy:srcToStatic']);

};
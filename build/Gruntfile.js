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
          namespace: false,
          wrapped: false,
          // Closure is not an official option, it's something we've created to make sure that Handlebars.templates.<template>
          // will be created if the script is included. Check out the src of the task for details. Found no other way of doing
          // this, other suggestions welcome!
          closure: true,
        },
        files: {
            "../static/js/handlebars_templates/articles.js": "../articles/templates/articles/handlebars/*.handlebars",
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
      }
    },

  });

  grunt.loadNpmTasks('grunt-contrib-handlebars');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default tasks
  grunt.registerTask('default', ['handlebars', 'copy']);

};
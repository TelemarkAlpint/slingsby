/* jshint indent:2,maxstatements:false */
/* global module,require */

/*
This file configures common tasks when developing on slingsby.

Static files like css and js needs to be transpiled (minified and concatenated) before they can be
served, and SASS needs to be compiled to CSS and so on. In broad steps this process is first
collecting all files needed in the ./tmp directory, and then building the final set of files into
./build, which is also served by the devserver. Some processes might skip the ./tmp directory
entirely, like the imagemin step which takes the graphics directly from slingsby/static-src to
build/static.

To just run the devserver, all you need to do is `grunt prep`. This will generate all the files you
need, and when deploying Travis will run `grunt build` which in addition to prep also packages the
python code and the static files into tarballs that can be pushed to the server.
*/
module.exports = function (grunt) {
  "use strict";
  /* jshint camelcase: false */

  // Load all grunt tasks defined in package.json
  require('load-grunt-tasks')(grunt);

  // Project configuration.
  grunt.initConfig({


    pkg: grunt.file.readJSON('package.json'),

    bower: {
      install: {
        options: {
          copy: false,
        }
      }
    },

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
          importPath: [
            '.tmp/sass',
            'bower_components/bootstrap-sass-official/assets/stylesheets',
            'bower_components/blueimp-gallery/css',
          ],
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
        'slingsby/**/static/js/*.js',

        // Ignore the widgEditor lib that's not in the bower registry
        '!slingsby/general/static/js/widgEditor.js',
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
        files: ['slingsby/static-src/sass/*.scss'],
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
          ignore: 'migrations',
        },
        src: ['slingsby', '*.py', 'tools/*.py'],
      }
    },

    rename: {
      blueimp_gallery: {
        files: [
          {
            src: 'bower_components/blueimp-gallery/css/blueimp-gallery.min.css',
            dest: 'bower_components/blueimp-gallery/css/_blueimp-gallery.scss'
          }
        ]
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
        'slingsby/server-assets',
      ],
      media: [
        'media/**',
        '!media',
      ]
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
      },
    },

    filerev: {
      options: {
        algorithm: 'md5',
        length: 8,
      },
      gfx: {
        src: [
          'build/static/gfx/**/*.{png,jpg,gif}',
          '!build/static/gfx/widgEditor/**',
          '!build/static/stylesheets/img/**',
        ]
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
      options: {
        sourceMap: true,
        sourceMapIncludeSources: true,
      },
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
            'slingsby/events/static/js/event_detail.js',
          ],
          '.tmp/static/js/instagram.min.js': [
            'bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/modal.js',
            'slingsby/instagram/static/js/instagram.js',
          ],
          '.tmp/static/js/archive.min.js': [
            // Only add required parts of blueimp-gallery

            //'bower_components/blueimp-gallery/js/blueimp-helper.js',
            'bower_components/blueimp-gallery/js/blueimp-gallery.js',
            'bower_components/blueimp-gallery/js/blueimp-gallery-fullscreen.js',
            'bower_components/blueimp-gallery/js/blueimp-gallery-indicator.js',
            //'bower_components/blueimp-gallery/js/blueimp-gallery-video.js',
            //'bower_components/blueimp-gallery/js/blueimp-gallery-youtube.js',
            //'bower_components/blueimp-gallery/js/blueimp-gallery-vimeo.js',
            'bower_components/blueimp-gallery/js/jquery.blueimp-gallery.js',

            'slingsby/archive/static/js/archive.js',
          ],
          'build/static/js/socialSummary.min.js': 'slingsby/articles/static/js/socialSummary.js',
          'build/static/js/widgEditor.min.js': 'slingsby/general/static/js/widgEditor.js',
        }
      }
    },

  });

  // Default task
  grunt.registerTask('default', [
    'clean',
    'prep',
    'watch',
  ]);
  grunt.registerTask('lint', [
    'jshint',
    'pylint',
  ]);
  grunt.registerTask('pybuild', [
    'shell:buildPython',
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
  grunt.registerTask('init-bower-deps', [
    'bower',
    'rename:blueimp_gallery',
  ]);
};

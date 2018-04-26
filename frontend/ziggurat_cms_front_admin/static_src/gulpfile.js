/**
 * @license
 * Copyright (c) 2016 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
 */

'use strict';

const path = require('path');
const gulp = require('gulp');
const gulpif = require('gulp-if');
const webpack = require('gulp-webpack');
var sass = require('gulp-sass');

// Got problems? Try logging 'em
// const logging = require('plylog');
// logging.setVerbose();

// !!! IMPORTANT !!! //
// Keep the global.config above any of the gulp-tasks that depend on it
global.config = {
    polymerJsonPath: path.join(process.cwd(), 'polymer.json'),
    build: {
        rootDirectory: path.join(process.cwd(), 'build'),
        bundledDirectory: 'bundled',
        unbundledDirectory: 'unbundled',
        bundleType: 'both'
    },
    destinationDirectory: path.join(process.cwd(), '..', '..','..' ,'static'),
    rootDir: process.cwd(path.join('src', 'ziggurat_cms_front_admin')),
    name: 'ziggurat_cms_front_admin'
};

if (process.env.ZIGGURAT_CMS_STATIC_DIR) {
    global.config.destinationDirectory = process.env.ZIGGURAT_CMS_STATIC_DIR
}

if (process.env.ZIGGURAT_CMS_ROOT_DIR) {
    global.config.rootDir = process.env.ZIGGURAT_CMS_ROOT_DIR
}

if (process.env.ZIGGURAT_CMS_BUILD_ROOT_DIR) {
    global.config.build.rootDirectory = process.env.ZIGGURAT_CMS_BUILD_ROOT_DIR
}


console.log(global.config.destinationDirectory);
console.log(global.config.rootDir);
console.log(global.config.build.rootDirectory);

const clean = require('./gulp-tasks/clean.js');
const adminView = require('./gulp-tasks/vulcanized-admin.js');


// Rerun the task when a file changes
var notifyWatch = function (filepath) {
    console.log('File ' + filepath + ' was changed running tasks...');
};

gulp.task('watch', function () {
    var jsWatcher = gulp.watch('src/**/*.js', gulp.series('watch_build'));
    var htmlWatcher = gulp.watch('src/**/*.html', gulp.series('watch_build'));
    var cssWatcher = gulp.watch('sass/**/*.*', gulp.series('watch_build'));
    jsWatcher.on('change', notifyWatch);
    htmlWatcher.on('change', notifyWatch);
    cssWatcher.on('change', notifyWatch);
});


function copy_build() {
    return gulp.src(global.config.build.rootDirectory + '/**')
        .pipe(gulp.dest(global.config.destinationDirectory));
}
function copy_bower() {
    return gulp.src(path.join(global.config.rootDir, 'bower_components', '**'))
        .pipe(gulp.dest(path.join(global.config.destinationDirectory, global.config.name, 'bower_components')));
}
function copy_locale() {
    return gulp.src(path.join(global.config.rootDir, 'locale', '**'))
        .pipe(gulp.dest(path.join(global.config.destinationDirectory,
            global.config.name, 'locale')));
}

function webpack_stuff() {
    return gulp.src([path.join(global.config.rootDir, 'src', 'quill', 'quill.js')])
        .pipe(webpack(require('./webpack.config.js')))
        .pipe(gulp.dest('build/quill'));
}

function sass_build() {
    return gulp.src(path.join(global.config.rootDir, 'sass', '*.scss'))
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(path.join(global.config.build.rootDirectory, global.config.name, 'css')));
}

gulp.task('default', gulp.series([
    clean.build,
    sass_build,
    adminView.build,
    copy_build,
    copy_bower,
    copy_locale,
    clean.build,
]));

gulp.task('watch_build', gulp.series([
    clean.build,
    sass_build,
    adminView.build,
    copy_build,
    copy_locale,
    clean.build,
]));

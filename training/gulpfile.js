'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass');
const minifyCSS = require('gulp-minify-css');
const concatCSS = require('gulp-concat-css');
const concatJS = require('gulp-concat');
const autoprefixer = require('gulp-autoprefixer');
const uglify = require('gulp-uglify');
const babel = require('gulp-babel');

const SRC_CSS = './ticketing_system/src/scss/**/*.scss'
const DEST_CSS = './ticketing_system/static/ticketing_system/css'

/**
 * Tarea para compilar scss
 * 1) Compila scss
 * 2) Agrega los prefijos propietarios
 * 3) Concatena a styles.min.css
 * 4) Minifica el archivo
 * 5) Mueve el resultado a la carpeta destino
 */
gulp.task('scss', function () {
    gulp.src(SRC_CSS)
        .pipe(sass({
            outputStyle: 'expanded'
        }))
        .pipe(autoprefixer({
            versions: ['last 2 browsers']
        }))
        .pipe(concatCSS('style.min.css'))
        .pipe(minifyCSS({
            keepBreaks: false
        }))
        .pipe(gulp.dest(DEST_CSS));
});

gulp.task('es5', () => {
    gulp.src('./resources/src/js/**/*.js')
        .pipe(babel())
        .pipe(gulp.dest('./public/js'));
});

gulp.task('default', () => {
    gulp.watch(SRC_CSS, ['scss']);
    //gulp.watch('./resources/src/js/**/*.js', ['es5']);
});
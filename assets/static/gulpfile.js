var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

var browserSync = require('browser-sync');
var reload = browserSync.reload;

/**
 * Подготовка HTML-файлов к продакшену
 */
gulp.task('build-html', function () {
	return gulp.src('./src/templates/**/*.html')
		.pipe(gulp.dest('build'))
		.pipe(reload({ stream:true }));
});

/**
 * Подготовка CSS-файлов
 */
gulp.task('build-css', function () {
	return gulp.src('./src/sass/main.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('./build/css'))
		.pipe(autoprefixer({
			browsers: ['> 1%', 'IE 7']
		}))
		.pipe(reload({ stream:true }));
});

/**
 * Подготовка Картинок
 */
gulp.task('build-img', function () {
	return gulp.src('./src/img/**/**/*.+(jpg|png|gif|ico)')
		.pipe(gulp.dest('./build/img'))
		.pipe(reload({ stream:true }));
});

/**
 * Подготовка JS-файлов
 */
gulp.task('build-js', function () {
	return gulp.src('./src/js/**/*.js')
		.pipe(gulp.dest('./build/js'))
		.pipe(reload({ stream:true }));
});

/**
 * Подготовка шрифтов
 */
gulp.task('build-font', function () {
	return gulp.src('./src/fonts/**/*')
		.pipe(gulp.dest('./build/fonts'))
		.pipe(reload({ stream:true }));
});

gulp.task('default', ['build-html', 'build-css', 'build-font', 'build-img', 'build-js'], function () {

	gulp.watch(['src/templates/**/*.html'], ['build-html']);
	gulp.watch(['src/sass/**/*.scss'], ['build-css']);
	gulp.watch(['src/img/**/*.+(jpg|png|gif)'], ['build-img']);
	gulp.watch(['src/js/**/*.js'], ['build-js']);
});

gulp.task('build', ['build-html', 'build-css', 'build-font', 'build-img', 'build-js']);

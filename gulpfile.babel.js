/* Theme builder and previewer.

   Minimize JavaScript.
   Convert SASS to CSS and minify.
   Start MkDocs server
*/
import yargs from "yargs"
import gulp from "gulp"
import sass from "gulp-sass"
import uglify from "gulp-uglify"
import postcss from "gulp-postcss"
import autoprefixer from "autoprefixer"
import cssnano from "cssnano"
import child_process from "child_process"
import rename from "gulp-rename"
import gulpif from "gulp-if"
import clean from "gulp-clean"
import concat from "gulp-concat"
import mqpacker from "css-mqpacker"
import stream from "webpack-stream"
import webpack from "webpack"

/* Argument Flags */
const args = yargs.argv

/* Paths */
const config = {
  files: {
    scss: "./doc_theme/src/scss/*.scss",
    css: "./doc_theme/*.min.css",
    es6: "./doc_theme/src/js/*.js",
    js: ["./doc_theme/*.min.js", "./doc_theme/*.js.map"],
  },
  folders: {
    mkdocs: "./site",
    theme: './doc_theme'
  },
  compress: (args.compress) ? true : false,
  clean: (args.clean) ? true : false
}

/* Mkdocs server */
let mkdocs = null

// ------------------------------
// SASS/SCSS processing 
// ------------------------------
gulp.task("scss", () => {
  const processors = [
    autoprefixer,
    mqpacker,
    (config.compress) ? cssnano : false
  ].filter(t => t)

  return gulp.src(config.files.scss)
    .pipe(sass({includePaths: [
      "node_modules/modularscale-sass/stylesheets",
      "node_modules/material-design-color",
      "node_modules/material-shadows"
    ]}).on("error", sass.logError))
    .pipe(postcss(processors))
    .pipe(concat('extra.min.css'))
    .pipe(gulp.dest(config.folders.theme))
})

gulp.task("scss:watch", () => {
  gulp.watch(config.files.scss, ["scss"])
})

gulp.task("scss:clean", () => {
  return gulp.src(config.files.css)
    .pipe(clean())
})

// ------------------------------
// JavaScript processing 
// ------------------------------
gulp.task("js", () => {
  return gulp.src(config.files.es6)
    .pipe(
      stream(
        {
          devtool: 'source-map',
          entry: ['extra.js'],
          output: {
              filename: 'extra.min.js'
          },

          module: {
            loaders: [
              {
                test: /\.js$/,
                loader: 'babel-loader'
              }
            ]
          },

          plugins: [
            /* Don't emit assets that include errors */
            new webpack.NoEmitOnErrorsPlugin(),
            new webpack.DefinePlugin({
              'process.env': {
                'NODE_ENV': JSON.stringify('production')
              }
            }),
          ].concat(
            config.compress ? [
              new webpack.optimize.UglifyJsPlugin({
                compress: {
                  warnings: false,
                  screw_ie8: true,
                  conditionals: true,
                  unused: true,
                  comparisons: true,
                  sequences: true,
                  dead_code: true,
                  evaluate: true,
                  if_return: true,
                  join_vars: true
                },
                output: {
                  comments: false
                }
              })
          ] : []),

          resolve: {
            modules: [
              "doc_theme/src/js",
              "node_modules"
            ],
            extensions: [
              ".js"
            ]
          }
        },
        webpack
      )
    )
    .pipe(gulp.dest(config.folders.theme))
})

gulp.task("js:watch", () => {
  gulp.watch(config.files.es6, ["js"])
})

gulp.task("js:clean", () => {
  return gulp.src(config.files.js)
    .pipe(clean())
})

// ------------------------------
// MkDocs Server 
// ------------------------------
gulp.task("mkdocs:serve", () => {
  if (mkdocs) {
    mkdocs.kill()
  }
  mkdocs = child_process.spawn(
    "mkdocs",
    ["serve", "--dev-addr", "0.0.0.0:8000"],
    {stdio: "inherit"})
})

gulp.task("mkdocs:clean", () => {
  return gulp.src(config.folders.mkdocs)
    .pipe(clean())
})

// ------------------------------
// Main entry points
// ------------------------------
gulp.task("build", [
  config.clean ? "clean" : false,
  "scss",
  "js"
].filter(t => t))

gulp.task("serve", [
  config.clean ? "clean" : false,
  "build",
  "scss:watch",
  "js:watch",
  "mkdocs:serve"
].filter(t => t))

gulp.task("clean", [
  "scss:clean",
  "js:clean",
  "mkdocs:clean"
])

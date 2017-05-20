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
import childProcess from "child_process"
import gulpif from "gulp-if"
import clean from "gulp-clean"
import concat from "gulp-concat"
import mqpacker from "css-mqpacker"
import stream from "webpack-stream"
import webpack from "webpack"
import sourcemaps from "gulp-sourcemaps"
import rollup from "gulp-rollup"
import rollupBabel from "rollup-plugin-babel"
import stylelint from "gulp-stylelint"
import eslint from "gulp-eslint"

/* Argument Flags */
const args = yargs.argv

/* Paths */
const config = {
  files: {
    scss: "./doc_theme/src/scss/*.scss",
    css: "./doc_theme/*.min.css",
    es6: "./doc_theme/src/js/*.js",
    js: ["./doc_theme/*.min.js", "./doc_theme/*.js.map"],
    vendor: "./node_modules/clipboard/dist/*.js",
    gulp: "gulpfile.babel.js"
  },
  folders: {
    mkdocs: "./site",
    theme: "./doc_theme"
  },
  compress: {
    enabled: args.compress,
    jsOptions: {
      warnings: false,
      screw_ie8: true,    // eslint-disable-line camelcase
      conditionals: true,
      unused: true,
      comparisons: true,
      sequences: true,
      dead_code: true,    // eslint-disable-line camelcase
      evaluate: true,
      if_return: true,    // eslint-disable-line camelcase
      join_vars: true     // eslint-disable-line camelcase
    }
  },
  lint: {
    enabled: args.lint
  },
  clean: args.clean,
  sourcemaps: args.sourcemaps,
  webpack: args.webpack
}

/* Mkdocs server */
let mkdocs = null

// ------------------------------
// SASS/SCSS processing
// ------------------------------
gulp.task("scss:build", () => {
  const processors = [
    autoprefixer,
    mqpacker,
    (config.compress.enabled) ? cssnano : false
  ].filter(t => t)

  return gulp.src(config.files.scss)
    .pipe(sass({includePaths: [
      "node_modules/modularscale-sass/stylesheets",
      "node_modules/material-design-color",
      "node_modules/material-shadows"
    ]}).on("error", sass.logError))
    .pipe(postcss(processors))
    .pipe(concat("extra.min.css"))
    .pipe(gulp.dest(config.folders.theme))
})

gulp.task("scss:lint", () => {
  return gulp.src(config.files.scss)
    .pipe(
      stylelint({
        reporters: [
          {formatter: "string", console: true}
        ]
      }))
})

gulp.task("scss:watch", () => {
  gulp.watch(config.files.scss, ["scss:build"])
})

gulp.task("scss:clean", () => {
  return gulp.src(config.files.css)
    .pipe(clean())
})

// ------------------------------
// JavaScript processing
// ------------------------------
gulp.task("js:build:rollup", () => {
  return gulp.src(config.files.es6)
    .pipe(gulpif(config.sourcemaps, sourcemaps.init()))
    .pipe(rollup({
      "globals": {
        "clipboard": "Clipboard",
        "flowchart": "flowchart",
        "sequence-diagram": "Diagram"
      },
      "external": [
        "clipboard",
        "flowchart",
        "sequence-diagram"
      ],
      "format": "iife",
      "plugins": [
        rollupBabel({
          "presets": [
            ["es2015", {"modules": false}]
          ],
          babelrc: false,
          "plugins": ["external-helpers"]
        })
      ],
      "moduleName": "extra",
      "entry": `${config.folders.theme}/src/js/extra.js`
    }))
    .pipe(concat("extra.min.js"))
    .pipe(gulpif(config.compress.enabled, uglify({compress: config.compress.jsOptions})))
    .pipe(gulpif(config.sourcemaps, sourcemaps.write(config.folders.theme)))
    .pipe(gulp.dest(config.folders.theme))
})

gulp.task("js:build:webpack", () => {
  // Probably overkill for what we need.
  return gulp.src(config.files.es6)
    .pipe(
      stream(
        {
          devtool: (config.sourcemaps) ? "source-map" : "",
          entry: "extra.js",
          output: {filename: "extra.min.js"},
          module: {
            loaders: [
              {
                test: /\.js$/,
                loader: "babel-loader"
              }
            ]
          },
          plugins: [
            // Don't emit assets that include errors
            new webpack.NoEmitOnErrorsPlugin(),
            new webpack.DefinePlugin({
              "process.env": {
                "NODE_ENV": JSON.stringify("production")
              }
            })
          ].concat(
            config.compress.enabled ? [
              new webpack.optimize.UglifyJsPlugin({
                sourceMap: config.sourcemaps,
                compress: config.compress.jsOptions,
                output: {comments: false}
              })
            ] : []
          ),
          stats: {color: true},
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

gulp.task("js:lint", () => {
  return gulp.src([config.files.es6, config.files.gulp])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError())
})

gulp.task("js:watch", () => {
  gulp.watch(config.files.es6, ["js:build:rollup"])
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
  mkdocs = childProcess.spawn(
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
  config.webpack ? "js:build:webpack" : "js:build:rollup",
  "scss:build",
  config.lint.enabled ? "js:lint" : false,
  config.lint.enabled ? "scss:lint" : false
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

/* Theme builder and previewer.

   Minimize JavaScript.
   Convert SASS to CSS and minify.
   Start MkDocs server
*/
import Promise from "promise"
import yargs from "yargs"
import gulp from "gulp"
import sass from "gulp-sass"
import uglify from "gulp-uglify"
import postcss from "gulp-postcss"
import autoprefixer from "autoprefixer"
import cleanCSS from "gulp-clean-css"
import childProcess from "child_process"
import gulpif from "gulp-if"
import concat from "gulp-concat"
import mqpacker from "css-mqpacker"
import sourcemaps from "gulp-sourcemaps"
import rollup from "gulp-rollup"
import rollupBabel from "rollup-plugin-babel"
import stylelint from "gulp-stylelint"
import eslint from "gulp-eslint"
import rev from "gulp-rev"
import revReplace from "gulp-rev-replace"
import vinylPaths from "vinyl-paths"
import del from "del"
import touch from "gulp-touch-fd"
import path from "path"
import inlineSvg from "postcss-inline-svg"
import cssSvgo from "postcss-svgo"

/* Argument Flags */
const args = yargs
  .boolean("compress")
  .boolean("lint")
  .boolean("clean")
  .boolean("sourcemaps")
  .boolean("buildmkdocs")
  .boolean("revision")
  .default("mkdocs", "mkdocs")
  .argv

/* Mkdocs server */
let mkdocs = null

// ------------------------------
// Configuration
// ------------------------------
const config = {
  files: {
    scss: "./docs/src/scss/**/*.scss",
    css: "./docs/theme/assets/pymdownx-extras/*.css",
    jsSrc: "./docs/src/js/*.js",
    js: ["./docs/theme/assets/pymdownx-extras/*.js", "./docs/theme/assets/pymdownx-extras/*.js.map"],
    gulp: "gulpfile.babel.js",
    mkdocsSrc: "./docs/src/mkdocs.yml"
  },
  folders: {
    mkdocs: "./site",
    theme: "./docs/theme/assets/pymdownx-extras",
    src: "./docs/src"
  },
  compress: {
    enabled: args.compress,
    jsOptions: {
      conditionals: true,
      unused: true,
      comparisons: true,
      sequences: true,
      dead_code: true,    // eslint-disable-line camelcase
      evaluate: true,
      if_return: true,    // eslint-disable-line camelcase
      join_vars: true     // eslint-disable-line camelcase,
    }
  },
  lint: {
    enabled: args.lint
  },
  clean: args.clean,
  sourcemaps: args.sourcemaps,
  buildmkdocs: args.buildmkdocs,
  revision: args.revision,
  mkdocsCmd: args.mkdocs
}

// ------------------------------
// SASS/SCSS processing
// ------------------------------
gulp.task("scss:build:sass", () => {
  const plugins = [
    autoprefixer,
    mqpacker,
    inlineSvg(
      {
        paths: [
          "node_modules"
        ],
        encode: false
      }
    ),
    cssSvgo(
      {
        plugins: [
          {removeDimensions: true},
          {removeViewBox: false}
        ],
        encode: false
      }
    )
  ].filter(t => t)

  return gulp.src("./docs/src/scss/extra*.scss")
    .pipe(sass({
      includePaths: [
        "node_modules/modularscale-sass/stylesheets",
        "node_modules/material-design-color",
        "node_modules/material-shadows",
        "node_modules/mermaid/src/themes"]
    }).on("error", sass.logError))
    .pipe(postcss(plugins))
    .pipe(gulpif(config.compress.enabled, cleanCSS()))
    .pipe(
      vinylPaths(
        filepath => {
          return concat(path.basename(filepath, ".scss"))
        }))

    // Revisioning
    .pipe(gulpif(config.revision, rev()))
    .pipe(gulp.dest(config.folders.theme))
    .pipe(gulpif(config.revision, rev.manifest("manifest.json", {base: config.folders.theme, merge: true})))
    .pipe(gulpif(config.revision, gulp.dest(config.folders.theme)))
})

gulp.task("scss:build", gulp.series("scss:build:sass", () => {
  return gulp.src(config.files.mkdocsSrc)
    .pipe(gulpif(config.revision, revReplace({
      manifest: gulp.src("manifest.json", {allowEmpty: true}),
      replaceInExtensions: [".yml"]
    })))
    .pipe(gulp.dest("."))
}))

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
  gulp.watch(config.files.scss, gulp.series("scss:build", "mkdocs:update"))
})

gulp.task("scss:clean", () => {
  return gulp.src(config.files.css, {allowEmpty: true})
    .pipe(vinylPaths(del))
})

// ------------------------------
// JavaScript processing
// ------------------------------
gulp.task("js:build:rollup", () => {
  return gulp.src(config.files.jsSrc)
    .pipe(gulpif(config.sourcemaps, sourcemaps.init()))
    .pipe(rollup({
      "output": {
        "name": "extra",
        "format": "iife",
        "globals": {
          "flowchart": "flowchart",
          "sequence-diagram": "Diagram"
        }
      },
      "external": [
        "flowchart",
        "sequence-diagram"
      ],
      "plugins": [
        rollupBabel({
          "presets": [
            ["@babel/preset-env", {"modules": false}]
          ],
          babelrc: false
        })
      ],
      "input": `${config.folders.src}/js/extra.js`
    }))
    .pipe(gulp.dest("docs/src/markdown/_snippets/.code"))
    .pipe(gulpif(config.compress.enabled, uglify({compress: config.compress.jsOptions, warnings: false})))
    .pipe(gulpif(config.sourcemaps, sourcemaps.write(config.folders.theme)))

    // Revisioning
    .pipe(gulpif(config.revision, rev()))
    .pipe(gulp.dest(config.folders.theme))
    .pipe(gulpif(config.revision, rev.manifest("manifest.json", {base: config.folders.theme, merge: true})))
    .pipe(gulpif(config.revision, gulp.dest(config.folders.theme)))
})

gulp.task("js:build", gulp.series("js:build:rollup", () => {
  return gulp.src(config.files.mkdocsSrc)
    .pipe(gulpif(config.revision, revReplace({
      manifest: gulp.src("manifest.json", {allowEmpty: true}),
      replaceInExtensions: [".yml"]
    })))
    .pipe(gulp.dest("."))
}))

gulp.task("js:lint", () => {
  return gulp.src([config.files.jsSrc, config.files.gulp])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError())
})

gulp.task("js:watch", () => {
  gulp.watch(config.files.jsSrc, gulp.series("js:build", "mkdocs:update"))
})

gulp.task("js:clean", () => {
  return gulp.src(config.files.js, {allowEmpty: true})
    .pipe(vinylPaths(del))
})

// ------------------------------
// MkDocs
// ------------------------------
gulp.task("mkdocs:serve", () => {
  if (mkdocs) {
    mkdocs.kill()
  }

  const cmdParts = (`${config.mkdocsCmd} serve --dev-addr=0.0.0.0:8000`).split(/ +/)
  const cmd = cmdParts[0]
  const cmdArgs = cmdParts.slice(1, cmdParts.length - 1)

  mkdocs = childProcess.spawn(
    cmd,
    cmdArgs,
    {stdio: "inherit"})
})

gulp.task("mkdocs:watch", () => {
  gulp.watch(config.files.mkdocsSrc, gulp.series("mkdocs:update"))
})

gulp.task("mkdocs:update", () => {
  return gulp.src(config.files.mkdocsSrc)
    .pipe(gulp.dest("."))
    .pipe(touch())
})

gulp.task("mkdocs:build", () => {
  return new Promise((resolve, reject) => {
    const cmdParts = (`${config.mkdocsCmd} build`).split(/ +/)
    const cmd = cmdParts[0]
    const cmdArgs = cmdParts.slice(1, cmdParts.length - 1)

    const proc = childProcess.spawnSync(cmd, cmdArgs)
    if (proc.status)
      reject(proc.stderr.toString())
    else
      resolve()
  })
})

gulp.task("mkdocs:clean", () => {
  return gulp.src(config.folders.mkdocs, {allowEmpty: true})
    .pipe(vinylPaths(del))
})

// ------------------------------
// Main entry points
// ------------------------------
gulp.task("serve", gulp.series(
  // Clean
  "scss:clean",
  "js:clean",
  // Build JS and CSS
  "js:build",
  "scss:build",
  // Watch for changes and start mkdocs
  gulp.parallel(
    "scss:watch",
    "js:watch",
    "mkdocs:watch",
    "mkdocs:serve"
  )
))

gulp.task("clean", gulp.series(
  "scss:clean",
  "js:clean",
  "mkdocs:clean"
))

gulp.task("lint", gulp.series(
  "js:lint",
  "scss:lint"
))

gulp.task("build", gulp.series(
  // Clean
  config.clean ? "clean" : ["scss:clean", "js:clean"],
  // Build JS and CSS
  "js:build",
  "scss:build",
  [
    // Lint
    config.lint.enabled ? "lint" : false,
    // Build Mkdocs
    config.buildmkdocs ? "mkdocs:build" : false
  ].filter(t => t)
))

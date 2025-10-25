/* Theme builder and previewer.

   Minimize JavaScript.
   Convert SASS to CSS and minify.
   Start MkDocs server
*/
import Promise from "promise"
import yargs from "yargs"
import {hideBin} from "yargs/helpers"
import gulp from "gulp"
import gulpSass from "gulp-sass"
import * as sassCompiler from "sass"
import postcss from "gulp-postcss"
import scss from "postcss-scss"
import autoprefixer from "autoprefixer"
import childProcess from "child_process"
import gulpif from "gulp-if"
import concat from "gulp-concat"
import mqpacker from "css-mqpacker"
import terser from '@rollup/plugin-terser'
import {rollup} from "rollup"
import {babel as rollupBabel, getBabelOutputPlugin} from "@rollup/plugin-babel"
import gStylelintEsm from 'gulp-stylelint-esm'
import eslint from "gulp-eslint"
import rev from "gulp-rev"
import revReplace from "gulp-rev-replace"
import vinylPaths from "vinyl-paths"
import {deleteAsync, deleteSync} from "del"
import touch from "gulp-touch-fd"
import path from "path"
import inlineSvg from "postcss-inline-svg"
import cssSvgo from "postcss-svgo"
import replace from "gulp-replace"
import outputManifest from "rollup-plugin-output-manifest"
import sourcemaps from "gulp-sourcemaps"

const sass = gulpSass(sassCompiler)

/* Argument Flags */
const args = yargs(hideBin(process.argv))
  .boolean("compress")
  .boolean("lint")
  .boolean("clean")
  .boolean("sourcemaps")
  .boolean("buildmkdocs")
  .boolean("revision")
  .default("mkdocs", "mkdocs")
  .argv

// ------------------------------
// Configuration
// ------------------------------
const config = {
  files: {
    scss: "./docs/src/scss/**/*.scss",
    css: [
      "./docs/theme/assets/pymdownx-extras/*.css",
      "./docs/theme/assets/pymdownx-extras/*.css.map"
    ],
    jsSrc: "./docs/src/js/**/*.js",
    js: [
      "./docs/theme/assets/pymdownx-extras/*.js",
      "./docs/theme/assets/pymdownx-extras/*.js.map"
    ],
    gulp: "gulpfile.babel.mjs",
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

const rollupjs = async(sources, options) => {

  const pluginModules = [rollupBabel({babelHelpers: "bundled"})]
  if (options.revision) {
    pluginModules.push(outputManifest.default({fileName: "manifest-js.json", isMerge: options.merge}))
  }
  const outputPlugins = [getBabelOutputPlugin({allowAllFormats: true, presets: ["@babel/preset-env"]})]
  if (options.minify) {
    outputPlugins.push(terser())
  }

  let p = Promise.resolve()
  for (let i = 0; i < sources.length; i++) {
    const src = sources[i]

    p = p.then(async() => {
      return await rollup({
        input: src,
        plugins: pluginModules
      }).then(async bundle => {
        await bundle.write({
          dir: options.dest,
          format: "iife",
          sourcemapPathTransform: (relativeSourcePath, sourcemapPath) => {  // eslint-disable-line no-unused-vars
            // Something changed and now we must force the mapping to be relative to the file.
            return path.basename(relativeSourcePath)
          },
          sourcemapFile: src,
          entryFileNames: (options.revision) ? "[name]-[hash].js" : "[name].js",
          chunkFileNames: (options.revision) ? "[name]-[hash].js" : "[name].js",
          sourcemap: options.sourcemap,
          plugins: outputPlugins
        })
      })
    })
  }

  return await p
}

// ------------------------------
// SASS/SCSS processing
// ------------------------------
gulp.task("scss:build:sass", () => {
  const plugins = [
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
          {
            name: "preset-default"
          },
          'removeDimensions'
        ],
        encode: false
      }
    ),
    mqpacker,
    autoprefixer
  ].filter(t => t)

  deleteSync(`${config.folders.theme}/manifest-css.json`)

  return gulp.src("./docs/src/scss/extra*.scss")
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        "node_modules/modularscale-sass/stylesheets",
        "node_modules/material-design-color",
        "node_modules/material-shadows"],
      silenceDeprecations: ['legacy-js-api'],
      style: "compressed"
    }).on("error", sass.logError))
    .pipe(postcss(plugins))
    .pipe(
      vinylPaths(
        filepath => {
          return concat(path.basename(filepath, ".scss"))
        }))

    // Revisioning
    .pipe(gulpif(config.revision, rev()))
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(config.folders.theme))
    .pipe(
      gulpif(
        config.revision,
        rev.manifest(`${config.folders.theme}/manifest-css.json`, {base: config.folders.theme, merge: true})
      ))
    .pipe(gulpif(config.revision, gulp.dest(config.folders.theme)))
})

gulp.task("scss:build", gulp.series("scss:build:sass", () => {
  return gulp.src(config.files.mkdocsSrc)
    .pipe(gulpif(config.revision, revReplace({
      manifest: gulp.src(`${config.folders.theme}/manifest*.json`, {allowEmpty: true}),
      replaceInExtensions: [".yml"]
    })))
    .pipe(gulp.dest("."))
}))

gulp.task("scss:lint", () => {
  return gulp.src(config.files.scss)
    .pipe(
      gStylelintEsm({
        customSyntax: scss,
        reporters: [
          {formatter: "string", console: true}
        ]
      }))
})

gulp.task("scss:watch", () => {
  gulp.watch(config.files.scss, gulp.series("scss:build", "mkdocs:update"))
})

gulp.task("scss:clean", () => {
  return deleteAsync(config.files.css)
})

gulp.task("js:build:rollup", async() => {
  deleteSync(`${config.folders.theme}/manifest-js.json`)

  return await rollupjs(
    [
      `${config.folders.src}/js/material-extra-theme.js`,
      `${config.folders.src}/js/material-extra-3rdparty.js`,
      `${config.folders.src}/js/extra-loader.js`
    ],
    {
      dest: `${config.folders.theme}`,
      minify: config.compress.enabled,
      revision: config.revision,
      sourcemap: config.sourcemaps,
      merge: true
    }
  )
})

gulp.task("html:build", () => {
  return gulp.src("./docs/src/html/*.html")
    .pipe(gulpif(config.revision, revReplace({
      manifest: gulp.src(`${config.folders.theme}/manifest*.json`, {allowEmpty: true}),
      replaceInExtensions: [".html"]
    })))
    .pipe(replace(/((?:\r?\n?\s*)<!--[\s\S]*?-->(?:\s*)(?=\r?\n)|<!--[\s\S]*?-->)/g, ""))
    .pipe(gulp.dest("./docs/theme/partials/"))
})

gulp.task("html:watch", () => {
  gulp.watch("./docs/src/html/*.html", gulp.series("html:build", "mkdocs:update"))
})

gulp.task("js:build", gulp.series("js:build:rollup", "html:build", () => {
  return gulp.src(config.files.mkdocsSrc)
    .pipe(gulpif(config.revision, revReplace({
      manifest: gulp.src(`${config.folders.theme}/manifest*.json`, {allowEmpty: true}),
      replaceInExtensions: [".yml"]
    })))
    .pipe(gulp.dest("./"))
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
  return deleteAsync(config.files.js)
})

// ------------------------------
// MkDocs
// ------------------------------
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
  return deleteAsync(config.folders.mkdocs)
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
    "html:watch",
    "mkdocs:watch"
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

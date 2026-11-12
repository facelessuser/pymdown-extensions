import js from "@eslint/js"
import globals from "globals"
import stylistic from "@stylistic/eslint-plugin"
import jsdoc from "eslint-plugin-jsdoc"

export default [
  {
    ignores: ["node_modules/**", "site/**", "docs/theme/**", "build/**", "dist/**"]
  },
  js.configs.recommended,
  {
    files: ["**/*.js", "**/*.mjs"],
    plugins: {
      "@stylistic": stylistic,
      jsdoc
    },
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.es2015,
        ...globals.node,
        mermaid: "readonly",
        mermaidConfig: "readonly",
        MathJax: "readonly",
        katex: "readonly"
      }
    },
    settings: {
      jsdoc: {
        tagNamePreference: {
          returns: "return",
          arg: "param",
          argument: "param",
          class: "constructor",
          virtual: "abstract"
        }
      }
    },
    rules: {
      // Code quality
      "array-callback-return": 2,
      "block-scoped-var": 2,
      camelcase: [2, {properties: "always"}],
      complexity: 2,
      "consistent-this": 2,
      "dot-notation": 2,
      eqeqeq: 2,
      "func-names": [2, "never"],
      "func-style": 2,
      "init-declarations": 2,
      "lines-around-directive": 2,
      "max-depth": 2,
      "max-nested-callbacks": 2,
      "max-params": 2,
      "new-cap": 2,
      "no-array-constructor": 2,
      "no-alert": 2,
      "no-caller": 2,
      "no-console": 1,
      "no-duplicate-imports": 2,
      "no-eq-null": 2,
      "no-eval": 2,
      "no-extend-native": 2,
      "no-extra-bind": 2,
      "no-global-assign": 2,
      "no-invalid-this": 2,
      "no-labels": 2,
      "no-lone-blocks": 2,
      "no-loop-func": 2,
      "no-nested-ternary": 2,
      "no-new": 0,
      "no-object-constructor": 2,
      "no-param-reassign": 2,
      "no-prototype-builtins": 2,
      "no-shadow": 2,
      "no-template-curly-in-string": 2,
      "no-throw-literal": 2,
      "no-undefined": 2,
      "no-underscore-dangle": [2, {allowAfterThis: true, allowAfterSuper: true}],
      "no-unneeded-ternary": 2,
      "no-unsafe-negation": 2,
      "no-unused-expressions": 2,
      "no-unused-vars": [1, {caughtErrors: "none"}],
      "no-use-before-define": 2,
      "no-useless-call": 2,
      "no-useless-computed-key": 2,
      "no-useless-constructor": 2,
      "no-useless-rename": 2,
      "no-var": 2,
      "no-with": 2,
      "object-shorthand": 2,
      "operator-assignment": 2,
      "prefer-arrow-callback": 2,
      "prefer-const": 2,
      "prefer-numeric-literals": 2,
      "prefer-spread": 2,
      "prefer-template": 2,
      radix: 2,
      strict: 2,
      "unicode-bom": 2,

      // Formatting
      "@stylistic/array-bracket-spacing": 2,
      "@stylistic/arrow-parens": [2, "as-needed"],
      "@stylistic/arrow-spacing": 2,
      "@stylistic/block-spacing": 2,
      "@stylistic/brace-style": 2,
      "@stylistic/comma-dangle": [2, "never"],
      "@stylistic/comma-style": [2, "last"],
      "@stylistic/computed-property-spacing": 2,
      "@stylistic/eol-last": 2,
      "@stylistic/function-call-spacing": 2,
      "@stylistic/generator-star-spacing": 2,
      "@stylistic/indent": [2, 2, {
        FunctionDeclaration: {
          body: 1,
          parameters: 2
        },
        FunctionExpression: {
          body: 1,
          parameters: 2
        },
        MemberExpression: 1,
        VariableDeclarator: {
          var: 2,
          let: 2,
          const: 3
        },
        ignoredNodes: [
          "TemplateLiteral"
        ],
        SwitchCase: 1
      }],
      "@stylistic/key-spacing": 2,
      "@stylistic/keyword-spacing": 2,
      "@stylistic/lines-around-comment": 2,
      "@stylistic/max-len": [1, {
        code: 120,
        ignorePattern: "// TODO"
      }],
      "@stylistic/max-statements-per-line": 2,
      "@stylistic/newline-per-chained-call": 2,
      "@stylistic/no-confusing-arrow": [2, {allowParens: false}],
      "@stylistic/no-floating-decimal": 2,
      "@stylistic/no-multiple-empty-lines": [1, {max: 1}],
      "@stylistic/no-tabs": 2,
      "@stylistic/no-trailing-spaces": 2,
      "@stylistic/no-whitespace-before-property": 2,
      "@stylistic/object-curly-spacing": [2, "never"],
      "@stylistic/one-var-declaration-per-line": 2,
      "@stylistic/rest-spread-spacing": 2,
      "@stylistic/semi": [2, "never"],
      "@stylistic/semi-spacing": 2,
      "@stylistic/space-before-function-paren": [2, {
        anonymous: "never",
        named: "never",
        asyncArrow: "never",
        catch: "ignore"
      }],
      "@stylistic/space-in-parens": 2,
      "@stylistic/space-infix-ops": 2,
      "@stylistic/space-unary-ops": 2,
      "@stylistic/spaced-comment": [2, "always", {
        line: {
          markers: ["/", ":"],
          exceptions: ["-", "+"]
        },
        block: {
          markers: ["!"],
          exceptions: ["*"],
          balanced: true
        }
      }],
      "@stylistic/template-curly-spacing": "off",
      "@stylistic/yield-star-spacing": 2,

      // JSDoc (replaces the removed `require-jsdoc` and `valid-jsdoc` core rules)
      "jsdoc/require-jsdoc": [1, {
        require: {
          FunctionDeclaration: true,
          MethodDefinition: true,
          ClassDeclaration: false
        }
      }],
      "jsdoc/check-param-names": 1,
      "jsdoc/check-tag-names": 1,
      "jsdoc/require-param": 1,
      "jsdoc/require-param-description": 1,
      "jsdoc/require-returns": 1,
      "jsdoc/require-returns-description": 1
    }
  }
]

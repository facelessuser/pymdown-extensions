function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

(function () {
  'use strict';

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function");
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        writable: true,
        configurable: true
      }
    });
    if (superClass) _setPrototypeOf(subClass, superClass);
  }

  function _getPrototypeOf(o) {
    _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
      return o.__proto__ || Object.getPrototypeOf(o);
    };
    return _getPrototypeOf(o);
  }

  function _setPrototypeOf(o, p) {
    _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
      o.__proto__ = p;
      return o;
    };

    return _setPrototypeOf(o, p);
  }

  function _isNativeReflectConstruct() {
    if (typeof Reflect === "undefined" || !Reflect.construct) return false;
    if (Reflect.construct.sham) return false;
    if (typeof Proxy === "function") return true;

    try {
      Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {}));
      return true;
    } catch (e) {
      return false;
    }
  }

  function _construct(Parent, args, Class) {
    if (_isNativeReflectConstruct()) {
      _construct = Reflect.construct;
    } else {
      _construct = function _construct(Parent, args, Class) {
        var a = [null];
        a.push.apply(a, args);
        var Constructor = Function.bind.apply(Parent, a);
        var instance = new Constructor();
        if (Class) _setPrototypeOf(instance, Class.prototype);
        return instance;
      };
    }

    return _construct.apply(null, arguments);
  }

  function _isNativeFunction(fn) {
    return Function.toString.call(fn).indexOf("[native code]") !== -1;
  }

  function _wrapNativeSuper(Class) {
    var _cache = typeof Map === "function" ? new Map() : undefined;

    _wrapNativeSuper = function _wrapNativeSuper(Class) {
      if (Class === null || !_isNativeFunction(Class)) return Class;

      if (typeof Class !== "function") {
        throw new TypeError("Super expression must either be null or a function");
      }

      if (typeof _cache !== "undefined") {
        if (_cache.has(Class)) return _cache.get(Class);

        _cache.set(Class, Wrapper);
      }

      function Wrapper() {
        return _construct(Class, arguments, _getPrototypeOf(this).constructor);
      }

      Wrapper.prototype = Object.create(Class.prototype, {
        constructor: {
          value: Wrapper,
          enumerable: false,
          writable: true,
          configurable: true
        }
      });
      return _setPrototypeOf(Wrapper, Class);
    };

    return _wrapNativeSuper(Class);
  }

  function _assertThisInitialized(self) {
    if (self === void 0) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return self;
  }

  function _possibleConstructorReturn(self, call) {
    if (call && (_typeof(call) === "object" || typeof call === "function")) {
      return call;
    } else if (call !== void 0) {
      throw new TypeError("Derived constructors may only return object or undefined");
    }

    return _assertThisInitialized(self);
  }

  function _createSuper(Derived) {
    var hasNativeReflectConstruct = _isNativeReflectConstruct();

    return function _createSuperInternal() {
      var Super = _getPrototypeOf(Derived),
          result;

      if (hasNativeReflectConstruct) {
        var NewTarget = _getPrototypeOf(this).constructor;

        result = Reflect.construct(Super, arguments, NewTarget);
      } else {
        result = Super.apply(this, arguments);
      }

      return _possibleConstructorReturn(this, result);
    };
  }

  function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(o);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
  }

  function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;

    for (var i = 0, arr2 = new Array(len); i < len; i++) {
      arr2[i] = arr[i];
    }

    return arr2;
  }

  function _createForOfIteratorHelper(o, allowArrayLike) {
    var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"];

    if (!it) {
      if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") {
        if (it) o = it;
        var i = 0;

        var F = function F() {};

        return {
          s: F,
          n: function n() {
            if (i >= o.length) return {
              done: true
            };
            return {
              done: false,
              value: o[i++]
            };
          },
          e: function e(_e) {
            throw _e;
          },
          f: F
        };
      }

      throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
    }

    var normalCompletion = true,
        didErr = false,
        err;
    return {
      s: function s() {
        it = it.call(o);
      },
      n: function n() {
        var step = it.next();
        normalCompletion = step.done;
        return step;
      },
      e: function e(_e2) {
        didErr = true;
        err = _e2;
      },
      f: function f() {
        try {
          if (!normalCompletion && it["return"] != null) it["return"]();
        } finally {
          if (didErr) throw err;
        }
      }
    };
  }
  /* Notes (as of Mermaid 8.7.0):
   * - Gantt: width is always relative to the parent, if you have a small parent, the chart will be squashed.
   *   Can't help it.
   * - Journey: Suffers from the same issues that Gantt does.
   * - Pie: These charts have no default height or width. Good luck pinning them down to a reasonable size.
   * - Git: The render portion is agnostic to the size of the parent element. But padding of the SVG is relative
   *   to the parent element. You will never find a happy size.
   */

  /**
   * Targets special code or div blocks and converts them to UML.
   * @param {string} className is the name of the class to target.
   * @return {void}
   */


  var uml = function uml(className) {
    // Custom element to encapsulate Mermaid content.
    var MermaidDiv = /*#__PURE__*/function (_HTMLElement) {
      _inherits(MermaidDiv, _HTMLElement);

      var _super = _createSuper(MermaidDiv);
      /**
      * Creates a special Mermaid div shadow DOM.
      * Works around issues of shared IDs.
      * @return {void}
      */


      function MermaidDiv() {
        var _this;

        _classCallCheck(this, MermaidDiv);

        _this = _super.call(this); // Create the Shadow DOM and attach style

        var shadow = _this.attachShadow({
          mode: "open"
        });

        var style = document.createElement("style");
        style.textContent = "\n      :host {\n        display: block;\n        line-height: initial;\n        font-size: 16px;\n      }\n      div.diagram {\n        margin: 0;\n        overflow: visible;\n      }";
        shadow.appendChild(style);
        return _this;
      }

      return MermaidDiv;
    }( /*#__PURE__*/_wrapNativeSuper(HTMLElement));

    if (typeof customElements.get("diagram-div") === "undefined") {
      customElements.define("diagram-div", MermaidDiv);
    }

    var getFromCode = function getFromCode(parent) {
      // Handles <pre><code> text extraction.
      var text = "";

      for (var j = 0; j < parent.childNodes.length; j++) {
        var subEl = parent.childNodes[j];

        if (subEl.tagName.toLowerCase() === "code") {
          for (var k = 0; k < subEl.childNodes.length; k++) {
            var child = subEl.childNodes[k];
            var whitespace = /^\s*$/;

            if (child.nodeName === "#text" && !whitespace.test(child.nodeValue)) {
              text = child.nodeValue;
              break;
            }
          }
        }
      }

      return text;
    }; // We use this to determine if we want the dark or light theme.
    // This is specific for our MkDocs Material environment.
    // You should load your configs based on your own environment's needs.


    var defaultConfig = {
      startOnLoad: false,
      theme: "default",
      flowchart: {
        htmlLabels: false
      },
      er: {
        useMaxWidth: false
      },
      sequence: {
        useMaxWidth: false,
        noteFontWeight: "14px",
        actorFontSize: "14px",
        messageFontSize: "16px"
      }
    };
    mermaid.mermaidAPI.globalReset(); // Non Material themes should just use "default"

    var scheme = null;

    try {
      scheme = document.querySelector("[data-md-color-scheme]").getAttribute("data-md-color-scheme");
    } catch (err) {
      scheme = "default";
    }

    var config = typeof mermaidConfig === "undefined" ? defaultConfig : mermaidConfig[scheme] || mermaidConfig["default"] || defaultConfig;
    mermaid.initialize(config); // Find all of our Mermaid sources and render them.

    var blocks = document.querySelectorAll("pre.".concat(className, ", diagram-div"));
    var surrogate = document.querySelector("html");

    var _loop = function _loop(i) {
      var block = blocks[i];
      var parentEl = block.tagName.toLowerCase() === "diagram-div" ? block.shadowRoot.querySelector("pre.".concat(className)) : block; // Create a temporary element with the typeset and size we desire.
      // Insert it at the end of our parent to render the SVG.

      var temp = document.createElement("div");
      temp.style.visibility = "hidden";
      temp.style.display = "display";
      temp.style.padding = "0";
      temp.style.margin = "0";
      temp.style.lineHeight = "initial";
      temp.style.fontSize = "16px";
      surrogate.appendChild(temp);

      try {
        mermaid.mermaidAPI.render("_diagram_".concat(i), getFromCode(parentEl), function (content) {
          var el = document.createElement("div");
          el.className = className;
          el.innerHTML = content; // Insert the render where we want it and remove the original text source.
          // Mermaid will clean up the temporary element.

          var shadow = document.createElement("diagram-div");
          shadow.shadowRoot.appendChild(el);
          block.parentNode.insertBefore(shadow, block);
          parentEl.style.display = "none";
          shadow.shadowRoot.appendChild(parentEl);

          if (parentEl !== block) {
            block.parentNode.removeChild(block);
          }
        }, temp);
      } catch (err) {} // eslint-disable-line no-empty


      if (surrogate.contains(temp)) {
        surrogate.removeChild(temp);
      }
    };

    for (var i = 0; i < blocks.length; i++) {
      _loop(i);
    }
  };

  var arithmatex = function arithmatex(className, mode) {
    if (mode === 'katex') {
      var maths = document.querySelectorAll(".".concat(className));

      for (var i = 0; i < maths.length; i++) {
        var tex = maths[i].textContent || maths[i].innerText;

        if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
          katex.render(tex.slice(2, -2), maths[i], {
            'displayMode': false
          });
        } else if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
          katex.render(tex.slice(2, -2), maths[i], {
            'displayMode': true
          });
        }
      }
    } else if (mode === 'mathjax') {
      MathJax.typesetPromise();
    }
  };

  var tabbed = function tabbed() {
    var tabOverflow = function tabOverflow() {
      var checkScroll = function checkScroll(e) {
        var target = e.target.closest('.tabbed-labels');
        target.classList.remove('tabbed-scroll-left', 'tabbed-scroll-right');

        if (e.type === "mouseover") {
          var scrollWidth = target.scrollWidth - target.clientWidth;
          var hscroll = target.scrollLeft;

          if (!hscroll) {
            target.scrollLeft = 1;
            hscroll = target.scrollLeft;
            target.scrollLeft = 0;

            if (hscroll) {
              target.classList.add('tabbed-scroll-right');
            }
          } else if (hscroll !== scrollWidth) {
            target.classList.add('tabbed-scroll-left', 'tabbed-scroll-right');
          } else if (hscroll) {
            target.classList.add('tabbed-scroll-left');
          }
        }
      };

      var labels = document.querySelectorAll('.tabbed-alternate > .tabbed-labels');
      labels.forEach(function (el) {
        el.addEventListener('mouseover', checkScroll);
        el.addEventListener('mouseout', checkScroll);
      });
    };

    var tabScroll = function tabScroll() {
      var tabs = document.querySelectorAll(".tabbed-alternate > input");

      var _iterator = _createForOfIteratorHelper(tabs),
          _step;

      try {
        var _loop = function _loop() {
          var tab = _step.value;
          tab.addEventListener("change", function () {
            var label = document.querySelector("label[for=".concat(tab.id, "]"));
            label.scrollIntoView({
              block: "nearest",
              inline: "nearest",
              behavior: "smooth"
            });
          });
        };

        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          _loop();
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    };

    var tabSync = function tabSync() {
      var tabs = document.querySelectorAll(".tabbed-set > input");

      var _iterator2 = _createForOfIteratorHelper(tabs),
          _step2;

      try {
        var _loop2 = function _loop2() {
          var tab = _step2.value;
          tab.addEventListener("click", function () {
            var labelContent = document.querySelector("label[for=".concat(tab.id, "]")).innerHTML;
            var labels = document.querySelectorAll('.tabbed-set > label, .tabbed-alternate > .tabbed-labels > label');

            var _iterator3 = _createForOfIteratorHelper(labels),
                _step3;

            try {
              for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
                var label = _step3.value;

                if (label.innerHTML === labelContent) {
                  document.querySelector("input[id=".concat(label.getAttribute('for'), "]")).checked = true;
                }
              }
            } catch (err) {
              _iterator3.e(err);
            } finally {
              _iterator3.f();
            }
          });
        };

        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          _loop2();
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }
    };

    tabOverflow();
    tabScroll();
    tabSync();
  };

  (function () {
    var umlPromise = Promise.resolve();
    var mathPromise = Promise.resolve();
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (mutation.type === "attributes") {
          var scheme = mutation.target.getAttribute("data-md-color-scheme");

          if (!scheme) {
            scheme = "default";
          }

          localStorage.setItem("data-md-color-scheme", scheme);

          if (typeof mermaid !== "undefined") {
            uml("diagram");
          }
        }
      });
    });

    var main = function main() {
      observer.observe(document.querySelector("body"), {
        attributeFilter: ["data-md-color-scheme"]
      });
      tabbed();

      if (typeof mermaid !== "undefined") {
        umlPromise = umlPromise.then(function () {
          uml("diagram");
        })["catch"](function (err) {
          console.log("UML loading failed...".concat(err)); // eslint-disable-line no-console
        });
      }

      if (typeof katex !== "undefined") {
        mathPromise = mathPromise.then(function () {
          arithmatex("arithmatex", "katex");
        })["catch"](function (err) {
          console.log("Math loading failed...".concat(err)); // eslint-disable-line no-console
        });
      } else if (typeof MathJax !== "undefined" && 'typesetPromise' in MathJax) {
        mathPromise = mathPromise.then(function () {
          arithmatex("arithmatex", "mathjax");
        })["catch"](function (err) {
          console.log("Math loading failed...".concat(err)); // eslint-disable-line no-console
        });
      }
    };

    if (window.document$) {
      // Material specific hook
      window.document$.subscribe(main);
    } else {
      // Normal non-Material specific hook
      document.addEventListener("DOMContentLoaded", main);
    }
  })();
})();

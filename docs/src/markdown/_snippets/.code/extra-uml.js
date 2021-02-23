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
        style.textContent = "\n      :host {\n        display: block;\n        line-height: initial;\n        font-size: 16px;\n      }\n      div.mermaid {\n        margin: 0;\n        overflow: visible;\n      }";
        shadow.appendChild(style);
        return _this;
      }

      return MermaidDiv;
    }( /*#__PURE__*/_wrapNativeSuper(HTMLElement));

    if (typeof customElements.get("mermaid-div") === "undefined") {
      customElements.define("mermaid-div", MermaidDiv);
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

    var blocks = document.querySelectorAll("pre.".concat(className, ", mermaid-div"));
    var surrogate = document.querySelector("html");

    var _loop = function _loop(i) {
      var block = blocks[i];
      var parentEl = block.tagName.toLowerCase() === "mermaid-div" ? block.shadowRoot.querySelector("pre.".concat(className)) : block; // Create a temporary element with the typeset and size we desire.
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
        mermaid.mermaidAPI.render("_mermaid_".concat(i), getFromCode(parentEl), function (content) {
          var el = document.createElement("div");
          el.className = className;
          el.innerHTML = content; // Insert the render where we want it and remove the original text source.
          // Mermaid will clean up the temporary element.

          var shadow = document.createElement("mermaid-div");
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

  (function () {
    var onReady = function onReady(fn) {
      document.addEventListener("DOMContentLoaded", fn);
      document.addEventListener("DOMContentSwitch", fn);
    };

    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (mutation.type === "attributes") {
          var scheme = mutation.target.getAttribute("data-md-color-scheme");

          if (!scheme) {
            scheme = "default";
          }

          localStorage.setItem("data-md-color-scheme", scheme);

          if (typeof mermaid !== "undefined") {
            uml("mermaid");
          }
        }
      });
    });
    onReady(function () {
      observer.observe(document.querySelector("body"), {
        attributeFilter: ["data-md-color-scheme"]
      });

      if (typeof mermaid !== "undefined") {
        uml("mermaid");
      }
    });
  })();
})();

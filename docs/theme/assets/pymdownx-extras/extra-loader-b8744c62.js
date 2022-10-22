function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
!function () {
  "use strict";

  function e(e, t) {
    for (var n = 0; n < t.length; n++) {
      var o = t[n];
      o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o);
    }
  }
  function t(e) {
    return t = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function (e) {
      return e.__proto__ || Object.getPrototypeOf(e);
    }, t(e);
  }
  function n(e, t) {
    return n = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function (e, t) {
      return e.__proto__ = t, e;
    }, n(e, t);
  }
  function o() {
    if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
    if (Reflect.construct.sham) return !1;
    if ("function" == typeof Proxy) return !0;
    try {
      return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})), !0;
    } catch (e) {
      return !1;
    }
  }
  function r(e, t, i) {
    return r = o() ? Reflect.construct.bind() : function (e, t, o) {
      var r = [null];
      r.push.apply(r, t);
      var i = new (Function.bind.apply(e, r))();
      return o && n(i, o.prototype), i;
    }, r.apply(null, arguments);
  }
  function i(e) {
    var o = "function" == typeof Map ? new Map() : void 0;
    return i = function i(e) {
      if (null === e || (i = e, -1 === Function.toString.call(i).indexOf("[native code]"))) return e;
      var i;
      if ("function" != typeof e) throw new TypeError("Super expression must either be null or a function");
      if (void 0 !== o) {
        if (o.has(e)) return o.get(e);
        o.set(e, a);
      }
      function a() {
        return r(e, arguments, t(this).constructor);
      }
      return a.prototype = Object.create(e.prototype, {
        constructor: {
          value: a,
          enumerable: !1,
          writable: !0,
          configurable: !0
        }
      }), n(a, e);
    }, i(e);
  }
  function a(e, t) {
    if (t && ("object" == _typeof(t) || "function" == typeof t)) return t;
    if (void 0 !== t) throw new TypeError("Derived constructors may only return object or undefined");
    return function (e) {
      if (void 0 === e) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
      return e;
    }(e);
  }
  var c,
    d,
    l,
    u,
    f = function f(r) {
      var c = function (r) {
        !function (e, t) {
          if ("function" != typeof t && null !== t) throw new TypeError("Super expression must either be null or a function");
          e.prototype = Object.create(t && t.prototype, {
            constructor: {
              value: e,
              writable: !0,
              configurable: !0
            }
          }), Object.defineProperty(e, "prototype", {
            writable: !1
          }), t && n(e, t);
        }(s, r);
        var i,
          c,
          d,
          l,
          u,
          f = (i = s, c = o(), function () {
            var e,
              n = t(i);
            if (c) {
              var o = t(this).constructor;
              e = Reflect.construct(n, arguments, o);
            } else e = n.apply(this, arguments);
            return a(this, e);
          });
        function s() {
          var e;
          !function (e, t) {
            if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
          }(this, s);
          var t = (e = f.call(this)).attachShadow({
              mode: "open"
            }),
            n = document.createElement("style");
          return n.textContent = "\n      :host {\n        display: block;\n        line-height: initial;\n        font-size: 16px;\n      }\n      div.diagram {\n        margin: 0;\n        overflow: visible;\n      }", t.appendChild(n), e;
        }
        return d = s, l && e(d.prototype, l), u && e(d, u), Object.defineProperty(d, "prototype", {
          writable: !1
        }), d;
      }(i(HTMLElement));
      void 0 === customElements.get("diagram-div") && customElements.define("diagram-div", c);
      var d = {
        startOnLoad: !1,
        theme: "default",
        flowchart: {
          htmlLabels: !1
        },
        er: {
          useMaxWidth: !1
        },
        sequence: {
          useMaxWidth: !1,
          noteFontWeight: "14px",
          actorFontSize: "14px",
          messageFontSize: "16px"
        }
      };
      mermaid.mermaidAPI.globalReset();
      var l = null;
      try {
        l = document.querySelector("[data-md-color-scheme]").getAttribute("data-md-color-scheme");
      } catch (e) {
        l = "default";
      }
      var u = "undefined" == typeof mermaidConfig ? d : mermaidConfig[l] || mermaidConfig["default"] || d;
      mermaid.initialize(u);
      for (var f = document.querySelectorAll("pre.".concat(r, ", diagram-div")), s = document.querySelector("html body"), m = function m(e) {
          var t = f[e],
            n = "diagram-div" === t.tagName.toLowerCase() ? t.shadowRoot.querySelector("pre.".concat(r)) : t,
            o = document.createElement("div");
          o.style.visibility = "hidden", o.style.display = "display", o.style.padding = "0", o.style.margin = "0", o.style.lineHeight = "initial", o.style.fontSize = "16px", s.appendChild(o);
          try {
            mermaid.mermaidAPI.render("_diagram_".concat(e), function (e) {
              for (var t = "", n = 0; n < e.childNodes.length; n++) {
                var o = e.childNodes[n];
                if ("code" === o.tagName.toLowerCase()) for (var r = 0; r < o.childNodes.length; r++) {
                  var i = o.childNodes[r];
                  if ("#text" === i.nodeName && !/^\s*$/.test(i.nodeValue)) {
                    t = i.nodeValue;
                    break;
                  }
                }
              }
              return t;
            }(n), function (e) {
              var o = document.createElement("div");
              o.className = r, o.innerHTML = e;
              var i = document.createElement("diagram-div");
              i.shadowRoot.appendChild(o), t.parentNode.insertBefore(i, t), n.style.display = "none", i.shadowRoot.appendChild(n), n !== t && t.parentNode.removeChild(t);
            }, o);
          } catch (e) {}
          s.contains(o) && s.removeChild(o);
        }, p = 0; p < f.length; p++) {
        m(p);
      }
    },
    s = function s(e, t) {
      if ("katex" === t) for (var n = document.querySelectorAll(".".concat(e)), o = 0; o < n.length; o++) {
        var r = n[o].textContent || n[o].innerText;
        r.startsWith("\\(") && r.endsWith("\\)") ? katex.render(r.slice(2, -2), n[o], {
          displayMode: !1
        }) : r.startsWith("\\[") && r.endsWith("\\]") && katex.render(r.slice(2, -2), n[o], {
          displayMode: !0
        });
      } else "mathjax" === t && MathJax.typesetPromise();
    };
  c = Promise.resolve(), d = Promise.resolve(), l = new MutationObserver(function (e) {
    e.forEach(function (e) {
      if ("attributes" === e.type) {
        var t = e.target.getAttribute("data-md-color-scheme");
        t || (t = "default"), localStorage.setItem("data-md-color-scheme", t), "undefined" != typeof mermaid && f("diagram");
      }
    });
  }), u = function u() {
    l.observe(document.querySelector("body"), {
      attributeFilter: ["data-md-color-scheme"]
    }), "undefined" != typeof mermaid && (c = c.then(function () {
      f("diagram");
    })["catch"](function (e) {
      console.log("UML loading failed...".concat(e));
    })), "undefined" != typeof katex ? d = d.then(function () {
      s("arithmatex", "katex");
    })["catch"](function (e) {
      console.log("Math loading failed...".concat(e));
    }) : "undefined" != typeof MathJax && "typesetPromise" in MathJax && (d = d.then(function () {
      s("arithmatex", "mathjax");
    })["catch"](function (e) {
      console.log("Math loading failed...".concat(e));
    }));
  }, window.document$ ? window.document$.subscribe(u) : document.addEventListener("DOMContentLoaded", u);
}();
//# sourceMappingURL=extra-loader-b8744c62.js.map

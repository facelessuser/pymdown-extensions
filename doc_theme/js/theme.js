$(document).ready(function() {
    var convertUML = function(className, converter, settings) {
        var charts = document.querySelectorAll("pre." + className),
            arr = [],
            i, j, maxItem, diagaram, text, curNode;

        // Is there a settings object?
        if (settings === void 0) {
            settings = {};
        }

        // Make sure we are dealing with an array
        for(i = 0, maxItem = charts.length; i < maxItem; i++) arr.push(charts[i]);

        // Find the UML source element and get the text
        for (i = 0, maxItem = arr.length; i < maxItem; i++) {
            childEl = arr[i].firstChild;
            parentEl = childEl.parentNode;
            text = "";
            for (j = 0; j < childEl.childNodes.length; j++) {
                curNode = childEl.childNodes[j];
                whitespace = /^\s*$/;
                if (curNode.nodeName === "#text" && !(whitespace.test(curNode.nodeValue))) {
                    text = curNode.nodeValue;
                    break;
                }
            }

            // Do UML conversion and replace source
            el = document.createElement('div');
            el.className = className;
            parentEl.parentNode.insertBefore(el, parentEl);
            parentEl.parentNode.removeChild(parentEl);
            diagram = converter.parse(text);
            diagram.drawSVG(el, settings);
        }
    };

    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='wy-nav-top']", function() {
      $("[data-toggle='wy-nav-shift']").toggleClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });

    // Close menu when you click a link.
    $(document).on('click', ".wy-menu-vertical .current ul li a", function() {
      $("[data-toggle='wy-nav-shift']").removeClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });

    $(document).on('click', "[data-toggle='rst-current-version']", function() {
      $("[data-toggle='rst-versions']").toggleClass("shift-up");
    });

    // Make tables responsive
    $("table.docutils:not(.field-list)").wrap("<div class='wy-table-responsive'></div>");

    $('table').addClass('docutils');

    convertUML('uml-flowchart', flowchart);
    convertUML('uml-sequence-diagram', Diagram, {theme: 'simple'});
});

window.SphinxRtdTheme = (function (jquery) {
    var stickyNav = (function () {
        var navBar,
            win,
            stickyNavCssClass = 'stickynav',
            applyStickNav = function () {
                if (navBar.height() <= win.height()) {
                    navBar.addClass(stickyNavCssClass);
                } else {
                    navBar.removeClass(stickyNavCssClass);
                }
            },
            enable = function () {
                applyStickNav();
                win.on('resize', applyStickNav);
            },
            init = function () {
                navBar = jquery('nav.wy-nav-side:first');
                win    = jquery(window);
            };
        jquery(init);
        return {
            enable : enable
        };
    }());
    return {
        StickyNav : stickyNav
    };
}($));

window.MathJax = {
    config: ["MMLorHTML.js"],
    extensions: ["tex2jax.js"],
    jax: ["input/TeX"],
    tex2jax: {
      inlineMath: [ ["\\(","\\)"] ],
      displayMath: [ ["\\[","\\]"] ]
    },
    TeX: {
      TagSide: "right",
      TagIndent: ".8em",
      MultLineWidth: "85%",
      equationNumbers: {
        autoNumber: "AMS",
      },
      unicode: {
        fonts: "STIXGeneral,'Arial Unicode MS'"
      }
    },
    displayAlign: 'left',
    showProcessingMessages: false,
    messageStyle: 'none'
};

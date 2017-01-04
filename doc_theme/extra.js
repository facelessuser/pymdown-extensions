(function (document) {
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

    function onReady(fn) {
        if (document.addEventListener) {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            document.attachEvent('onreadystatechange', function() {
                if (document.readyState === 'interactive')
                    fn();
            });
        }
    }

    onReady(function(){
        convertUML('uml-flowchart', flowchart);
        convertUML('uml-sequence-diagram', Diagram, {theme: 'simple'});
    });
})(document);

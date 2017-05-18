<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.2.7/raphael.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-sequence-diagrams/1.0.6/sequence-diagram-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.6.5/flowchart.min.js"></script>
<script type="text/javascript">
(function (document) {
    function convertUML(className, converter, settings) {
        var charts = document.querySelectorAll("pre." + className + ',div.' + className),
            arr = [],
            i, j, maxItem, diagaram, text, curNode,
            isPre;

        // Is there a settings object?
        if (settings === void 0) {
            settings = {};
        }

        // Make sure we are dealing with an array
        for(i = 0, maxItem = charts.length; i < maxItem; i++) arr.push(charts[i]);

        // Find the UML source element and get the text
        for (i = 0, maxItem = arr.length; i < maxItem; i++) {
            isPre = arr[i].tagName.toLowerCase() == 'pre';
            if (isPre) {
                // Handles <pre><code>
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
            } else {
                // Handles <div>
                el = arr[i];
                text = el.textContent || el.innerText;
                if (el.innerText){
                    el.innerText = '';
                } else {
                    el.textContent = '';
                }
            }
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
</script>

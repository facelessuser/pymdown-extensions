(function (document) {
    function clipboard_init() {
        var charts = document.querySelectorAll("div.codehilite"),
            arr = [],
            i, j, maxItem, pre, btn, span, el, clipboard;

        // Make sure we are dealing with an array
        for(i = 0, maxItem = charts.length; i < maxItem; i++) arr.push(charts[i]);

        // Find the code source element and get the text
        for (i = 0, maxItem = arr.length; i < maxItem; i++) {
            el = arr[i];
            pre = el.childNodes[0];

            pre.id = "hl_code" + i.toString();
            btn = document.createElement('button');
            span = document.createElement('span');
            span.appendChild(document.createTextNode('\uE85D'));
            btn.appendChild(span);
            btn.setAttribute("class", "clippy");
            btn.setAttribute("data-clipboard-target", "#hl_code" + i.toString());
            btn.addEventListener('mouseleave', function(e){
                e.currentTarget.setAttribute('class','clippy');
                e.currentTarget.setAttribute('aria-label', 'Copy to Clipboard.')
            });
            el.insertBefore(btn, pre);
        }
        clipboard = new Clipboard('.clippy');
        clipboard.on('success', function(e) {
            e.clearSelection();
            e.trigger.setAttribute('aria-label', 'Copied!');
            e.trigger.setAttribute('class', 'clippy tooltip left');
        });
        clipboard.on('error', function(e) {
            e.clearSelection();
            e.trigger.setAttribute('aria-label', 'Copy Failed!');
            e.trigger.setAttribute('class', 'clippy tooltip left');
        });
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
        clipboard_init();
    });
})(document);

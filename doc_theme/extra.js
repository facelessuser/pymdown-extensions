(function (document) {
  function clipboard_init() {
    if (typeof Clipboard !== "undefined" && Clipboard.isSupported()) {
      var code = document.querySelectorAll("div.codehilite>pre, pre>code"),
        arr = [],
        i, j, maxItem, pre, btn, icon, parent, clipboard;

      // Make sure we are dealing with an array
      for(i = 0, maxItem = code.length; i < maxItem; i++) arr.push(code[i]);

      // Find the code source element and get the text
      for (i = 0, maxItem = arr.length; i < maxItem; i++) {
        parent = code[i].parentNode;
        codeId = 'hl_code' + i.toString();
        btn = document.createElement('button');
        icon = document.createElement('i');
        parent.id = codeId
        icon.setAttribute("class", "md-icon md-icon--clipboard")
        btn.appendChild(icon)
        btn.setAttribute("class", "clip-btn")
        btn.setAttribute("data-clipboard-target", '#' + codeId + ' pre, #' + codeId + ' code')
        btn.setAttribute("aria-label", "Copy to Clipboard.")
        btn.addEventListener('mouseleave', function(e){
          e.currentTarget.setAttribute('class','clip-btn');
          e.currentTarget.setAttribute('aria-label', 'Copy to Clipboard.')
        });
        parent.insertBefore(btn, parent.childNodes[0]);
      }
      cBoard = new Clipboard('.clip-btn');
      cBoard.on('success', function(e) {
        e.clearSelection();
        e.trigger.setAttribute('aria-label', 'Copied!');
        e.trigger.setAttribute('class', 'clip-btn clip-tip');
      });
      cBoard.on('error', function(e) {
        e.clearSelection();
        e.trigger.setAttribute('aria-label', 'Copy Failed!');
        e.trigger.setAttribute('class', 'clip-btn clip-tip');
      });
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
    clipboard_init();
  });
})(document);

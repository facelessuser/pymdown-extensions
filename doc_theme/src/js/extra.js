import Clipboard from "clipboard"
import uml from "./uml"
import cboard from "./cboard"

(() => {
  function onReady(fn) {
    if (document.addEventListener) {
      document.addEventListener('DOMContentLoaded', fn)
    } else {
      document.attachEvent('onreadystatechange', () => {
        if (document.readyState === 'interactive') {fn()}
      })
    }
  }

  onReady(() => {
    if (typeof flowchart !== "undefined") {
      uml('uml-flowchart', flowchart)
    }
    if (typeof Diagram !== "undefined") {
      uml('uml-sequence-diagram', Diagram, {theme: 'simple'})
    }
    if (typeof Clipboard !== "undefined" && Clipboard.isSupported()) {
      cboard()
    }
  })

})()

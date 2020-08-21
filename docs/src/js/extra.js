import uml from "./uml"

(() => {
  const onReady = function(fn) {
    document.addEventListener("DOMContentLoaded", fn)
    document.addEventListener("DOMContentSwitch", fn)
  }

  onReady(() => {
    if (typeof mermaid !== "undefined") {
      uml("mermaid")
    }
  })
})()

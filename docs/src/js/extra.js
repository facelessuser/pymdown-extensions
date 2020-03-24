import uml from "./uml"

(() => {
  const onReady = function(fn) {
    if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", fn)
      document.addEventListener("DOMContentSwitch", fn)
    } else {
      document.attachEvent("onreadystatechange", () => {
        if (document.readyState === "interactive") {
          fn()
        }
      })
    }
  }

  onReady(() => {

    if (typeof mermaid !== "undefined") {
      uml("mermaid")
    }
  })
})()

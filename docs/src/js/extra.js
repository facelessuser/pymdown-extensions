import uml from "./uml"

(() => {
  const onReady = function(fn) {
    if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", fn)
    } else {
      document.attachEvent("onreadystatechange", () => {
        if (document.readyState === "interactive") {
          fn()
        }
      })
    }
  }

  onReady(() => {

    if (typeof flowchart !== "undefined") {
      uml(flowchart, "uml-flowchart")
    }

    if (typeof Diagram !== "undefined") {
      uml(Diagram, "uml-sequence-diagram", {theme: "simple"})
    }
  })
})()

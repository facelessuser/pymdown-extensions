import uml from "./uml"
import details from "./details"

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
    details()

    if (typeof flowchart !== "undefined") {
      uml(flowchart, "uml-flowchart")
    }

    if (typeof Diagram !== "undefined") {
      uml(Diagram, "uml-sequence-diagram", {theme: "simple"})
    }
  })
})()

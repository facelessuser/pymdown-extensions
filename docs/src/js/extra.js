import uml from "./uml"

(() => {
  const onReady = function(fn) {
    document.addEventListener("DOMContentLoaded", fn)
    document.addEventListener("DOMContentSwitch", fn)
  }

  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === "attributes" && mutation.attributeName === "data-md-color-scheme") {
        if (typeof mermaid !== "undefined") {
          uml("mermaid")
        }
      }
    })
  })

  onReady(() => {
    if (typeof mermaid !== "undefined") {
      uml("mermaid")
    }
  })

  observer.observe(document.querySelector("body"), {attributes: true})
})()

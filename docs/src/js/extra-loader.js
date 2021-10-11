import uml from "./uml"
import arithmatex from "./arithmatex"
import tabbed from "./tabbed"

// Main function
(() => {
  let umlPromise = Promise.resolve()
  let mathPromise = Promise.resolve()

  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === "attributes") {
        let scheme = mutation.target.getAttribute("data-md-color-scheme")
        if (!scheme) {
          scheme = "default"
        }
        localStorage.setItem("data-md-color-scheme", scheme)
        if (typeof mermaid !== "undefined") {
          uml("diagram")
        }
      }
    })
  })

  const main = () => {
    observer.observe(document.querySelector("body"), {attributeFilter: ["data-md-color-scheme"]})

    tabbed()

    if (typeof mermaid !== "undefined") {
      umlPromise = umlPromise.then(() => {
        uml("diagram")
      }).catch(err => {
        console.log(`UML loading failed...${err}`) // eslint-disable-line no-console
      })
    }

    if (typeof katex !== "undefined") {
      mathPromise = mathPromise.then(() => {
        arithmatex("arithmatex", "katex")
      }).catch(err => {
        console.log(`Math loading failed...${err}`) // eslint-disable-line no-console
      })
    } else if (typeof MathJax !== "undefined" && 'typesetPromise' in MathJax) {
      mathPromise = mathPromise.then(() => {
        arithmatex("arithmatex", "mathjax")
      }).catch(err => {
        console.log(`Math loading failed...${err}`) // eslint-disable-line no-console
      })
    }
  }

  if (window.document$) {
    // Material specific hook
    window.document$.subscribe(main)
  } else {
    // Normal non-Material specific hook
    document.addEventListener("DOMContentLoaded", main)
  }
})()

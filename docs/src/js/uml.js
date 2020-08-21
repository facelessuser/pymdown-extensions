/* Notes (as of Mermaid 8.7.0):
 * - Gantt: width is always relative to the parent, if you have a small parent, the chart will be squashed.
 *   Can't help it.
 * - Journey: Suffers from the same issues that Gantt does.
 * - Pie: These charts have no default height or width. Good luck pinning them down to a reasonable size.
 * - Git: The render portion is agnostic to the size of the parent element. But padding of the SVG is relative
 *   to the parent element. You will never find a happy size.
 */

/**
 * Targets special code or div blocks and converts them to UML.
 * @param {string} className is the name of the class to target.
 * @return {void}
 */
export default className => {

  // Custom element to encapsulate Mermaid content.
  class MermaidDiv extends HTMLElement {

    /**
    * Creates a special Mermaid div shadow DOM.
    * Works around issues of shared IDs.
    * @return {void}
    */
    constructor() {
      super()

      // Create the Shadow DOM and attach style
      const shadow = this.attachShadow({mode: "open"})
      const style = document.createElement("style")
      style.textContent = `
      div.mermaid {
        margin: 0;
        overflow: visible;
      }`
      shadow.appendChild(style)
    }
  }

  customElements.define("mermaid-div", MermaidDiv)

  const getFromCode = function(parent) {
    // Handles <pre><code> text extraction.
    let text = ""
    for (let j = 0; j < parent.childNodes.length; j++) {
      const subEl = parent.childNodes[j]
      if (subEl.tagName.toLowerCase() === "code") {
        for (let k = 0; k < subEl.childNodes.length; k++) {
          const child = subEl.childNodes[k]
          const whitespace = /^\s*$/
          if (child.nodeName === "#text" && !(whitespace.test(child.nodeValue))) {
            text = child.nodeValue
            break
          }
        }
      }
    }
    return text
  }

  // We use this to determine if we want the dark or light theme.
  // This is specific for our MkDocs environment.
  // You should load your configs based on your own environment's needs.
  mermaid.mermaidAPI.globalReset()
  if (document.querySelector("[data-md-color-scheme='dracula']")) {
    mermaid.initialize(mermaidConfig.dracula || {startOnLoad: false})
  } else if (document.querySelector("[data-md-color-scheme='slate']")) {
    mermaid.initialize(mermaidConfig.dark || {startOnLoad: false})
  } else {
    mermaid.initialize(mermaidConfig.light || {startOnLoad: false})
  }

  // Find all of our Mermaid sources and render them.
  const blocks = document.querySelectorAll(`pre.${className}`)
  const surrogate = document.querySelector("body")
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]

    // Create a temporary element with the typeset and size we desire.
    // Insert it at the end of our parent to render the SVG.
    const temp = document.createElement("div")
    temp.style.visibility = "hidden !important"
    temp.style.display = "display !important"
    temp.style.padding = "0 !important"
    temp.style.margin = "0 !important"
    surrogate.appendChild(temp)

    mermaid.mermaidAPI.render(
      `_mermaind_${i}`,
      getFromCode(parentEl),
      content => {
        const el = document.createElement("div")
        el.className = className
        el.innerHTML = content

        // Insert the render where we want it and remove the original text source.
        // Mermaid will clean up the temporary element.
        const shadow = document.createElement("mermaid-div")
        shadow.shadowRoot.appendChild(el)
        parentEl.parentNode.insertBefore(shadow, parentEl)
        parentEl.parentNode.removeChild(parentEl)
      },
      temp
    )
  }
}

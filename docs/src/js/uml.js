/**
 * Targets special code or div blocks and converts them to UML.
 * @param {string} className is the name of the class to target.
 * @return {void}
 */
export default className => {

  // We use this to determine if we want the dark or light theme.
  // Could be changed to anything. This script can't support dynamic theme
  // changes yet. We'd probably need to store the mermaid instructions in
  // a special script tag or hidden tag and then provide a reloader to update
  // the existing renders.
  let preferences = null
  if (document.querySelector("[data-md-color-scheme=\"dracula\"]")) {
    preferences = window.mermaidConfig.dracula
  } else if (document.querySelector("[data-md-color-scheme=\"slate\"]")) {
    preferences = window.mermaidConfig.dark
  } else {
    preferences = window.mermaidConfig.light
  }

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
      style.textContent = preferences.themeCss || ""
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

  mermaid.initialize(preferences)
  const config = mermaid.mermaidAPI.getConfig()

  // Find all of our Mermaid sources and render them.
  const blocks = document.querySelectorAll(`pre.${className}`)
  const surogate = document.querySelector("html")
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]

    // Create a temporary element with the typeset and size we desire.
    // Insert it at the end of our parent to render the SVG.
    const temp = document.createElement("div")
    temp.style.visibility = "hidden"
    temp.style.width = "100%"
    temp.style.minWidth = "100%"
    temp.style.fontSize = config.themeVariables.fontSize || "16px"
    surogate.appendChild(temp)

    mermaid.mermaidAPI.render(
      `_mermaind_${i}`,
      getFromCode(parentEl),
      content => {
        const el = document.createElement("div")
        el.className = className
        el.innerHTML = content
        const child = el.childNodes[0]

        // Some mermaid items have no height assigned, fix this for sane sizes. Mainly for state diagrams.
        //
        // Notes (as of Mermaid 8.4.8):
        // - Gantt: width is always relative to the parent, if you have a small parent, the chart will be squashed.
        //   Can't help it.
        // - Pie: These charts have no default height or width. Good luck pinning them down to a reasonable size.
        // - Git: The render portion is agnostic to the size of the parent element. But padding of the SVG is relative
        //   to the parent element. You will never find a happy size.
        // - State/Class: These two are rendered with references internally in the SVG that certain elements link to.
        //   The problem is that they link to internal elements that use the same IDs that are in other sibling SVG
        //   of these types. All other diagrams use unique IDs. So if the first of these gets hidden due to being in an
        //   inactive tab, or hidden under a closed details element the browser will not be able to find the ID as it
        //   only searches for the first. This will cause certain visual elements (arrow heads etc.) to disappear.
        if (!child.hasAttribute("height") && child.hasAttribute("width")) {
          child.setAttribute("height", temp.childNodes[0].getBoundingClientRect().height)
        }

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

/**
 * Targets special code or div blocks and converts them to UML.
 * @param {object} converter is the object that transforms the text to UML.
 * @param {string} className is the name of the class to target.
 * @param {object} settings is the settings for converter.
 * @return {void}
 */
export default function(converter, className, settings) {
  const blocks = document.querySelectorAll(`pre.${className},div.${className}`)

  // Is there a settings object?
  const config = (settings === void 0) ? {} : settings

  // Find the UML source element and get the text
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i]
    let text = null
    let el = null
    if (block.tagName.toLowerCase() === "pre") {
      // Handles <pre><code>
      const childEl = block.firstChild
      const parentEl = childEl.parentNode
      text = ""
      for (let j = 0; j < childEl.childNodes.length; j++) {
        const child = childEl.childNodes[j]
        const whitespace = /^\s*$/
        if (child.nodeName === "#text" && !(whitespace.test(child.nodeValue))) {
          text = child.nodeValue
          break
        }
      }
      // Do UML conversion and replace source
      el = document.createElement("div")
      el.className = className
      parentEl.parentNode.insertBefore(el, parentEl)
      parentEl.parentNode.removeChild(parentEl)
    } else {
      // Handles <div>
      el = block
      text = el.textContent || el.innerText
      if (el.innerText){
        el.innerText = ""
      } else {
        el.textContent = ""
      }
    }
    const diagram = converter.parse(text)
    diagram.drawSVG(el, config)
  }
}

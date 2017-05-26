/**
 * Targets special code or div blocks and converts them to UML.
 * @param {object} converter is the object that transforms the text to UML.
 * @param {string} className is the name of the class to target.
 * @param {object} settings is the settings for converter.
 * @return {void}
 */
export default (converter, className, settings) => {
  // Change article to whatever element your main Markdown content lives.
  const article = document.querySelectorAll('article')
  const blocks = document.querySelectorAll(`pre.${className},div.${className}`)

  // Is there a settings object?
  const config = (settings === void 0) ? {} : settings

  // Find the UML source element and get the text
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i]
    let text = null
    const parentEl = block
    const el = document.createElement("div")
    el.className = className
    el.style.visibility = "hidden"
    el.style.position = "absolute"

    if (block.tagName.toLowerCase() === "pre") {
      // Handles <pre><code>
      const childEl = block.firstChild
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
    } else {
      // Handles <div>
      text = parentEl.textContent || parentEl.innerText
      if (parentEl.innerText){
        parentEl.innerText = ""
      } else {
        parentEl.textContent = ""
      }
    }

    // Insert our new div at the end of our content to get general
    // typset and page sizes as our parent might be `display:none`
    // keeping us from getting the right size sizes for our SVG.
    // Our new div will be hidden via "visibility" and take no space
    // via `poistion: absolute`. When we are all done, use the
    // original node as a reference to insert our SVG back
    // into the proper place, and then make our SVG visilbe again.
    // Lastly, clean up the old node.
    article[0].appendChild(el)
    const diagram = converter.parse(text)
    diagram.drawSVG(el, config)
    el.style.visibility = "visible"
    el.style.position = "static"
    parentEl.parentNode.insertBefore(el, parentEl)
    parentEl.parentNode.removeChild(parentEl)
  }
}

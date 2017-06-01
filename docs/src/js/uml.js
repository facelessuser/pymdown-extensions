/**
 * Targets special code or div blocks and converts them to UML.
 * @param {object} converter is the object that transforms the text to UML.
 * @param {string} className is the name of the class to target.
 * @param {object} settings is the settings for converter.
 * @return {void}
 */
export default (converter, className, settings) => {

  const getFromCode = function(parent) {
    // Handles <pre><code>
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

  const getFromDiv = function(parent) {
    // Handles <div>
    return parent.textContent || parent.innerText
  }

  // Change article to whatever element your main Markdown content lives.
  const article = document.querySelectorAll("article")
  const blocks = document.querySelectorAll(`pre.${className},div.${className}`)

  // Is there a settings object?
  const config = (settings === void 0) ? {} : settings

  // Find the UML source element and get the text
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]
    const el = document.createElement("div")
    el.className = className
    el.style.visibility = "hidden"
    el.style.position = "absolute"

    const text = (parentEl.tagName.toLowerCase() === "pre") ? getFromCode(parentEl) : getFromDiv(parentEl)

    // Insert our new div at the end of our content to get general
    // typset and page sizes as our parent might be `display:none`
    // keeping us from getting the right sizes for our SVG.
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

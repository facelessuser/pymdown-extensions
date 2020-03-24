/**
 * Targets special code or div blocks and converts them to UML.
 * @param {string} className is the name of the class to target.
 * @return {void}
 */
export default className => {

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

  const article = document.querySelector("article")
  const blocks = document.querySelectorAll(`pre.${className}`)
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]

    // Insert our new div at the end of our content to get general
    // typeset and page sizes as our parent might be `display:none`
    // keeping us from getting the right sizes for our SVG.
    // Our new div will be hidden via "visibility" and take no space
    // via `position: absolute`. When we are all done, we use the
    // callback to insert our content where we want it. Mermaid will
    // delete the temporary element when done, but we delete the
    // original source element.
    const temp = document.createElement("div")
    temp.style.visibility = "hidden"
    temp.style.position = "absolute"

    article.appendChild(temp)
    mermaid.mermaidAPI.render(
      `_mermaind_${i}`,
      getFromCode(parentEl),
      content => {
        const el = document.createElement("div")
        el.className = className
        const el2 = document.createElement("div")
        el2.innerHTML = content
        el.appendChild(el2)
        parentEl.parentNode.insertBefore(el, parentEl)
        parentEl.parentNode.removeChild(parentEl)
      },
      temp
    )
  }
}

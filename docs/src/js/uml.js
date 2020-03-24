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

  // Change article to whatever element your main Markdown content lives.
  const article = document.querySelectorAll("article")
  const blocks = document.querySelectorAll(`pre.${className}`)

  // Find the UML source element and get the text
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]
    const text = getFromCode(parentEl)

    // Insert our new div at the end of our content to get general
    // typeset and page sizes as our parent might be `display:none`
    // keeping us from getting the right sizes for our SVG.
    // Our new div will be hidden via "visibility" and take no space
    // via `position: absolute`. When we are all done, use the
    // original node as a reference to insert our SVG back
    // into the proper place, and then make our SVG visible again.
    // Lastly, clean up the old node.
    const temp = document.createElement("div")
    temp.style.visibility = "hidden"
    temp.style.position = "absolute"

    article[0].appendChild(temp)
    mermaid.mermaidAPI.render(
      `_mermaind_${i}`,
      text,
      content => {
        const el = document.createElement("div")
        el.className = className
        el.innerHTML = content
        parentEl.parentNode.insertBefore(el, parentEl)
        parentEl.parentNode.removeChild(parentEl)
      },
      temp
    )
  }
}

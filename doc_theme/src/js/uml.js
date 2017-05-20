export default function(className, converter, settings) {
  const blocks = document.querySelectorAll(`pre.${className},div.${className}`)

  // Is there a settings object?
  if (settings === void 0) {
      settings = {}
  }

  // Find the UML source element and get the text
  for (let block of blocks) {
    let text
    let el
    if (block.tagName.toLowerCase() == 'pre') {
      // Handles <pre><code>
      const childEl = block.firstChild
      const parentEl = childEl.parentNode
      text = ""
      for (let child of childEl.childNodes) {
        const whitespace = /^\s*$/
        if (child.nodeName === "#text" && !(whitespace.test(child.nodeValue))) {
          text = child.nodeValue
          break
        }
      }
      // Do UML conversion and replace source
      el = document.createElement('div')
      el.className = className
      parentEl.parentNode.insertBefore(el, parentEl)
      parentEl.parentNode.removeChild(parentEl)
    } else {
      // Handles <div>
      el = block
      text = el.textContent || el.innerText
      if (el.innerText){
        el.innerText = ''
      } else {
        el.textContent = ''
      }
    }
    const diagram = converter.parse(text)
    diagram.drawSVG(el, settings)
  }
}

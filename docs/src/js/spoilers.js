/**
 * Converts details/summary tags into working elements in browsers that don't yet support them.
 * @return {void}
 */
export default function() {
  // https://mathiasbynens.be/notes/html5-details-jquery#comment-35
  // Detect if details is supported in the browser
  const isDetailsSupported = (function(doc) {
    const el = doc.createElement("details")
    let fake = false
    if (!("open" in el)) {
      return false
    }
    const root = doc.body || (function() {
      const de = doc.documentElement
      fake = true
      return de.insertBefore(doc.createElement("body"), de.firstElementChild || de.firstChild)
    })()
    el.innerHTML = "<summary>a</summary>b"
    el.style.display = "block"
    root.appendChild(el)
    let diff = el.offsetHeight
    el.open = true
    diff = diff !== el.offsetHeight
    root.removeChild(el)
    if (fake) {
      root.parentNode.removeChild(root)
    }
    return diff
  })(document)

  if (!isDetailsSupported) {
    const blocks = document.querySelectorAll("details>summary")
    for (let i = 0; i < blocks.length; i++) {
      const summary = blocks[i]
      const details = summary.parentNode
      if (!details.hasAttribute("open")) {
        if (!details.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
          details.className += " no-details"
        }
      }
      summary.addEventListener("click", e => {
        const de = e.target.parentNode
        if (de.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
          const reg = new RegExp("(\\s|^)no-details(\\s|$)")
          de.className = de.className.replace(reg, " ")
          de.setAttribute("open", "")
        } else {
          de.className += " no-details"
          de.removeAttribute("open")
        }
      })
    }
  }
}

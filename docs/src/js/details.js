/**
 * Converts details/summary tags into working elements in browsers that don't yet support them.
 * @return {void}
 */
export default () => {

  const isDetailsSupported = (() => {
    // https://mathiasbynens.be/notes/html5-details-jquery#comment-35
    // Detect if details is supported in the browser
    const el = document.createElement("details")
    let fake = false

    if (!("open" in el)) {
      return false
    }

    const root = document.body || (() => {
      const de = document.documentElement
      fake = true
      return de.insertBefore(document.createElement("body"), de.firstElementChild || de.firstChild)
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
  })()

  if (!isDetailsSupported) {
    const blocks = document.querySelectorAll("details>summary")
    for (let i = 0; i < blocks.length; i++) {
      const summary = blocks[i]
      const details = summary.parentNode

      // Apply "no-details" to for unsupported details tags
      if (!details.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
        details.className += " no-details"
      }

      summary.addEventListener("click", e => {
        const node = e.target.parentNode
        if (node.hasAttribute("open")) {
          node.removeAttribute("open")
        } else {
          node.setAttribute("open", "open")
        }
      })
    }
  }
}

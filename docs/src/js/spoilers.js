/**
 * Converts details/summary tags into working elements in browsers that don't yet support them.
 * @return {void}
 */
export default () => {

  const isDetailsSupported = () => {
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
  }

  /* Toggle details state */
  const toggle = e => {
    const key = e.which
    if (!key || key === 13 || key === 32) {
      const details = e.target.parentNode
      if (details.hasAttribute("open")) {
        details.setAttribute("open", "open")
      } else {
        details.removeAttribute("open")
      }
      return false
    }
  }

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
        toggle(e)
      })
      summary.addEventListener("keydown", e => {
        toggle(e)
      })
    }
  }
}

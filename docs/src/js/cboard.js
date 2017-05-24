/**
 * Targets code blocks and inserts an overlay that copies text to the clipboard.
 * @param {object} Clipboard object.
 * @return {void}
 */
export default function(Clipboard) {
  if (Clipboard.isSupported()) {

    const blocks = document.querySelectorAll("div.codehilite>pre,pre.codehilite>code")

    // Find the code source element and get the text
    for (let i = 0; i < blocks.length; i++) {
      const code = blocks[i]
      const parent = code.parentNode
      const codeId = `hl_code${i}`
      const btn = document.createElement("button")
      const icon = document.createElement("i")
      parent.id = codeId
      icon.setAttribute("class", "md-icon md-icon--clipboard")
      btn.appendChild(icon)
      btn.setAttribute("class", "clip-btn")
      btn.setAttribute("data-clipboard-target", `#${codeId} pre, #${codeId} code`)
      btn.setAttribute("aria-label", "Copy to Clipboard.")

      btn.addEventListener("mouseleave", e => {
        e.currentTarget.setAttribute("class","clip-btn")
        e.currentTarget.setAttribute("aria-label", "Copy to Clipboard.")
      })
      parent.insertBefore(btn, parent.childNodes[0])
    }

    const cBoard = new Clipboard(".clip-btn")
    cBoard.on("success", e => {
      e.clearSelection()
      e.trigger.setAttribute("aria-label", "Copied!")
      e.trigger.setAttribute("class", "clip-btn clip-tip")
    })
    cBoard.on("error", e => {
      e.clearSelection()
      e.trigger.setAttribute("aria-label", "Copy Failed!")
      e.trigger.setAttribute("class", "clip-btn clip-tip")
    })
  }
}

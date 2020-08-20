/**
 * Targets special code or div blocks and converts them to UML.
 * @param {string} className is the name of the class to target.
 * @return {void}
 */
export default className => {

  // Themes themes 99% of what we want, but there are still some stubborn things that require CSS
  // `https://github.com/facelessuser/pymdown-extensions/blob/master/docs/src/scss/js/_mermaid_dracula.scss`
  const configDark = {
    startOnLoad: false,
    theme: "base",
    themeVariables: {
      darkMode: true,

      background: "#323443",
      mainBkg: "#604b7d",
      textColor: "#bf95f9",
      lineColor: "#bf95f9",
      errorBkgColor: "#802c2c",
      errorTextColor: "#ff5757",
      primaryColor: "#604b7d",
      primaryTextColor: "#bf95f9",
      primaryBorderColor: "#bf95f9",
      secondaryColor: "#297d3e",
      secondaryTextColor: "#52fa7c",
      secondaryBorderColor: "#52fa7c",
      tertiaryColor: "#303952",
      tertiaryTextColor: "#6071a4",
      tertiaryBorderColor: "#6071a4",
      noteBkgColor: "#797d45",
      noteTextColor: "#f1fa89",
      noteBorderColor: "#f1fa89",
      edgeLabelBackground: "#604b7d",
      edgeLabelText: "#604b7d",

      actorLineColor: "#6071a4",

      activeTaskBkgColor: "#803d63",
      activeTaskBorderColor: "#ff7ac6",
      doneTaskBkgColor: "#297d3e",
      doneTaskBorderColor: "#52fa7c",
      critBkgColor: "#802c2c",
      critBorderColor: "#ff5757",
      taskTextColor: "#bf95f9",
      taskTextOutsideColor: "#bf95f9",
      taskTextLightColor: "#bf95f9",
      sectionBkgColor: "#bf95f9b3",
      sectionBkgColor2: "#bf95f966",
      altSectionBkgColor: "#323443",
      todayLineColor: "#ff7ac6",
      gridColor: "#6071a4",
      defaultLinkColor: "#8be8fd",

      altBackground: "#bf95f9",

      classText: "#bf95f9",

      fillType0: "#406080",
      fillType1: "#46747f",
      fillType2: "#297d3e",
      fillType3: "#805c36",
      fillType4: "#803d63",
      fillType5: "#604b7d",
      fillType6: "#802c2c",
      fillType7: "#797d45",
      fillType8: "#7c7c79"
    },
    flowchart: {
      htmlLabels: false
    },
    sequence: {
      useMaxWidth: false
    },
    class: {
      textHeight: 16,
      dividerMargin: 16
    }
  }

  const configLight = {
    startOnLoad: false,
    theme: "base",
    flowchart: {
      htmlLabels: false
    },
    sequence: {
      useMaxWidth: false
    },
    class: {
      textHeight: 16,
      dividerMargin: 16
    }
  }

  const getFromCode = function(parent) {
    // Handles <pre><code> text extraction.
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

  // Get the proper theme color
  if (document.querySelector("[data-md-color-primary^=\"drac-\"]")) {
    mermaid.initialize(configDark)
  } else {
    mermaid.initialize(configLight)
  }

  // Find all of our Mermaid sources and render them.
  const config = mermaid.mermaidAPI.getConfig()
  const blocks = document.querySelectorAll(`pre.${className}`)
  const surogate = document.querySelector("html")
  for (let i = 0; i < blocks.length; i++) {
    const parentEl = blocks[i]

    // Create a temporary element with the typeset and size we desire.
    // Insert it at the end of our parent to render the SVG.
    const temp = document.createElement("div")
    temp.style.visibility = "hidden"
    temp.style.width = "100%"
    temp.style.minWidth = "100%"
    temp.style.fontSize = config.themeVariables.fontSize || "16px"
    surogate.appendChild(temp)

    mermaid.mermaidAPI.render(
      `_mermaind_${i}`,
      getFromCode(parentEl),
      content => {
        const el = document.createElement("div")
        el.className = className
        el.innerHTML = content
        const child = el.childNodes[0]

        // Some mermaid items have no height assigned, fix this for sane sizes. Mainly for state diagrams.
        //
        // Notes (as of Mermaid 8.4.8):
        // - Gantt: width is always relative to the parent, if you have a small parent, the chart will be squashed.
        //   Can't help it.
        // - Pie: These charts have no default height or width. Good luck pinning them down to a reasonable size.
        // - Git: The render portion is agnostic to the size of the parent element. But padding of the SVG is relative
        //   to the parent element. You will never find a happy size.
        // - State/Class: These two are rendered with references internally in the SVG that certain elements link to.
        //   The problem is that they link to internal elements that use the same IDs that are in other sibling SVG
        //   of these types. All other diagrams use unique IDs. So if the first of these gets hidden due to being in an
        //   inactive tab, or hidden under a closed details element the browser will not be able to find the ID as it
        //   only searches for the first. This will cause certain visual elements (arrow heads etc.) to disappear.
        if (!child.hasAttribute("height") && child.hasAttribute("width")) {
          child.setAttribute("height", temp.childNodes[0].getBoundingClientRect().height)
        }

        // Insert the render where we want it and remove the original text source.
        // Mermaid will clean up the temporary element.
        parentEl.parentNode.insertBefore(el, parentEl)
        parentEl.parentNode.removeChild(parentEl)
      },
      temp
    )
  }
}

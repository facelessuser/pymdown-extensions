export default () => {
  const tabOverflow = () => {
    const checkScroll = e => {
      const target = e.target.closest('.tabbed-labels')
      target.classList.remove('tabbed-scroll-left', 'tabbed-scroll-right')
      if (e.type === "mouseover") {
        const scrollWidth = target.scrollWidth - target.clientWidth
        let hscroll = target.scrollLeft
        if (!hscroll) {
          target.scrollLeft = 1
          hscroll = target.scrollLeft
          target.scrollLeft = 0
          if (hscroll) {
            target.classList.add('tabbed-scroll-right')
          }
        } else if (hscroll !== scrollWidth){
          target.classList.add('tabbed-scroll-left', 'tabbed-scroll-right')
        } else if (hscroll) {
          target.classList.add('tabbed-scroll-left')
        }
      }
    }

    const labels = document.querySelectorAll('.tabbed-alternate > .tabbed-labels')
    labels.forEach(el => {
      el.addEventListener('mouseover', checkScroll)
      el.addEventListener('mouseout', checkScroll)
    })
  }

  const tabScroll = () => {
    const tabs = document.querySelectorAll(".tabbed-alternate > input")
    for (const tab of tabs) {
      tab.addEventListener("change", () => {
        const label = document.querySelector(`label[for=${tab.id}]`)
        label.scrollIntoView({block: "nearest", inline: "nearest", behavior: "smooth"})
      })
    }
  }

  const tabSync = () => {
    const tabs = document.querySelectorAll(".tabbed-set > input")
    for (const tab of tabs) {
      tab.addEventListener("click", () => {
        const labelContent = document.querySelector(`label[for=${tab.id}]`).innerHTML
        const labels = document.querySelectorAll('.tabbed-set > label, .tabbed-alternate > .tabbed-labels > label')
        for (const label of labels) {
          if (label.innerHTML === labelContent) {
            document.querySelector(`input[id=${label.getAttribute('for')}]`).checked = true
          }
        }
      })
    }
  }

  tabOverflow()
  tabScroll()
  tabSync()
}

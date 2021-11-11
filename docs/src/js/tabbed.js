const checkScroll = e => {
  // Use a margin as we just don't always align exactly on the right.
  const margin = 3
  const target = e.target
  if (!e.target.matches('.tabbed-labels')) {
    return
  }

  const scrollWidth = target.scrollWidth - target.clientWidth
  target.classList.remove('tabbed-scroll-left', 'tabbed-scroll-right')
  if (e.type === "resize" || e.type === "scroll") {
    if (scrollWidth === 0) {
      return
    }
    if (!target.scrollLeft) {
      target.classList.add('tabbed-scroll-right')
    } else if (target.scrollLeft < scrollWidth - margin){
      target.classList.add('tabbed-scroll-left', 'tabbed-scroll-right')
    } else {
      target.classList.add('tabbed-scroll-left')
    }
  }
}

// Change the tab to either the previous or next input - depending on which indicator was clicked.
// Make sure the current, selected input is scrolled into view.
const tabChange = e => {
  const target = e.target
  const selected = target.closest('.tabbed-set').querySelector('input:checked')
  let updated = null

  if (target.classList.contains('tabbed-scroll-right') && e.offsetX >= e.target.offsetWidth - 15) {
    const sib = selected.nextSibling
    updated = selected
    if (sib && sib.tagName === 'INPUT') {
      updated = sib
    }
  } else if (target.classList.contains('tabbed-scroll-left') && e.offsetX <= 15) {
    const sib = selected.previousSibling
    updated = selected
    if (sib && sib.tagName === 'INPUT') {
      updated = sib
    }
  }
  if (updated) {
    updated.click()
  }
}

const onResize = new ResizeObserver(entries => {
  entries.forEach(entry => {
    checkScroll({target: entry.target, type: 'resize'})
  })
})

// Identify whether a tab bar can be scrolled left or right and apply indicator classes
const tabOverflow = () => {
  const labels = document.querySelectorAll('.tabbed-alternate > .tabbed-labels')
  onResize.disconnect()
  labels.forEach(el => {
    checkScroll({target: el, type: 'resize'})
    onResize.observe(el)
    el.addEventListener('resize', checkScroll)
    el.addEventListener('scroll', checkScroll)
    el.addEventListener('click', tabChange)
  })
}

// Smooth scroll tab into view when changed
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
      const current = document.querySelector(`label[for=${tab.id}]`)
      const pos = current.getBoundingClientRect().top
      const labelContent = current.innerHTML
      const labels = document.querySelectorAll('.tabbed-set > label, .tabbed-alternate > .tabbed-labels > label')
      for (const label of labels) {
        if (label.innerHTML === labelContent) {
          document.querySelector(`input[id=${label.getAttribute('for')}]`).checked = true
        }
      }

      // Preserve scroll position
      const delta = (current.getBoundingClientRect().top) - pos
      window.scrollBy(0, delta)
    })
  }
}

export default () => {
  tabOverflow()
  tabScroll()
  tabSync()
}

// MathJax configuration

if (!('mathjaxConfig' in window)) {
  window.MathJax = {
    tex: {
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
      processEscapes: true,
      processEnvironments: true,
      tagSide: "right",
      tagIndent: ".8em",
      multlineWidth: "85%",
      tags: "ams"
    },
    options: {
      ignoreHtmlClass: ".*",
      processHtmlClass: "arithmatex"
    }
  }
}

if (!('mermaidConfig' in window)) {
  // Our loader looks for `mermaidConfig` and will load the the appropriate
  // configuration based on our current scheme: light, dark, etc.
  window.mermaidConfig = {
    dracula: {
      startOnLoad: false,
      theme: "base",
      themeCSS: "\
        * {\
          --drac-page-bg: hsl(233, 15%, 23%);\
          --drac-white-fg: hsl(60, 30%, 96%);\
          --drac-purple-fg: hsl(265, 89%, 78%);\
          --drac-purple-bg: hsl(265, 25%, 39%);\
          --drac-yellow-fg: hsl(65, 92%, 76%);\
          --drac-blue-fg: hsl(225, 27%, 51%);\
        }\
        \
        /* General */\
        [id^='_diagram'] {\
          background-color: var(--drac-page-bg);\
        }\
        \
        /* Entity Relationship */\
        rect.relationshipLabelBox {\
          opacity: 0.75 !important;\
          fill: var(--drac-purple-bg) !important;\
        }\
        defs marker#ZERO_OR_MORE_END circle {\
          fill: var(--drac-page-bg) !important;\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ZERO_OR_MORE_END path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ZERO_OR_MORE_START circle{\
          fill: var(--drac-page-bg) !important;\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ZERO_OR_MORE_START path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ONLY_ONE_START path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ONLY_ONE_END path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ZERO_OR_ONE_START path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ZERO_OR_ONE_END path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ONE_OR_MORE_START path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        defs marker#ONE_OR_MORE_END path {\
          stroke: var(--drac-purple-fg) !important;\
        }\
        \
        /* Flowchart */\
        .labelText,\
        :not(.branchLabel) > .label text {\
          fill: var(--drac-purple-fg);\
        }\
        .edgeLabel text {\
          fill: var(--drac-purple-fg) !important;\
        }\
        .edgeLabel rect {\
          opacity: 0.75 !important;\
          fill: var(--drac-purple-bg) !important;\
        }\
        \
        .grey rect.label-container { \
          fill: var(--drac-purple-bg) !important;\
          stroke: var(--drac-purple-fg) !important;\
        } \
        /* Sequence */\
        line[id^='actor'] {\
          stroke: var(--drac-blue-fg);\
        }\
        .noteText {\
          fill: var(--drac-yellow-fg);\
        }\
        \
        /* Gantt */\
        .sectionTitle {\
          fill: var(--drac-purple-fg) !important;\
        }\
        \
        .grid .tick line {\
          stroke: var(--drac-blue-fg) !important;\
        }\
        \
        .grid .tick text {\
          fill: var(--drac-purple-fg);\
        }\
        \
        /* Class Diagram */\
        .statediagram-state rect.divider {\
          fill: transparent !important;\
        }\
        \
        /* State Diagram */\
        .stateGroup circle[style$=\"fill: black;\"] {\
          fill: var(--drac-purple-bg) !important;\
          stroke: var(--drac-purple-bg) !important;\
        }\
        \
        .stateGroup circle[style$=\"fill: white;\"] {\
          fill: var(--drac-purple-bg) !important;\
          stroke: var(--drac-purple-fg) !important;\
        }\
        \
        .stateGroup .composit {\
          fill: var(--drac-page-bg);\
        }\
        /* Pie */\
        text.slice {\
          fill: var(--drac-white-fg) !important;\
        }\
        /* Git Graph */\
        .commit-bullets .commit-reverse,\
        .commit-bullets .commit-merge, \
        .commit-bullets .commit-highlight-inner {\
          fill: var(--drac-page-bg) !important;\
          stroke: var(--drac-page-bg) !important;\
        }\
        ",
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
        fillType8: "#7c7c79",

        git0: "#ff5555",
        git1: "#ffb86c",
        git2: "#f1fa8c",
        git3: "#50fa7b",
        git4: "#8be9fd",
        git5: "#809fff",
        git6: "#ff79c6",
        git7: "#bd93f9",

        gitInv0: "#ff5555",
        gitInv1: "#ffb86c",
        gitInv2: "#f1fa8c",
        gitInv3: "#50fa7b",
        gitInv4: "#8be9fd",
        gitInv5: "#809fff",
        gitInv6: "#ff79c6",
        gitInv7: "#bd93f9",

        gitBranchLabel0: "#323443",
        gitBranchLabel1: "#323443",
        gitBranchLabel2: "#323443",
        gitBranchLabel3: "#323443",
        gitBranchLabel4: "#323443",
        gitBranchLabel5: "#323443",
        gitBranchLabel6: "#323443",
        gitBranchLabel7: "#323443",

        commitLabelColor: '#52fa7c',
        commitLabelBackground: '#297d3e'
      },
      flowchart: {
        htmlLabels: false,
        useMaxWidth: false
      },
      er: {
        useMaxWidth: false
      },
      sequence: {
        useMaxWidth: false,
        // Mermaid handles Firefox a little different.
        // For some reason, it doesn't attach font sizes to the labels in Firefox.
        // If we specify the documented defaults, font sizes are written to the labels in Firefox.
        noteFontWeight: "14px",
        actorFontSize: "14px",
        messageFontSize: "16px"
      },
      journey: {
        useMaxWidth: false
      },
      pie: {
        useMaxWidth: false
      },
      gantt: {
        useMaxWidth: false
      },
      gitGraph: {
        useMaxWidth: false
      }
    },

    default: {
      startOnLoad: false,
      theme: "default",
      flowchart: {
        htmlLabels: false
      },
      er: {
        useMaxWidth: false
      },
      sequence: {
        useMaxWidth: false,
        noteFontWeight: "14px",
        actorFontSize: "14px",
        messageFontSize: "16px"
      }
    },

    slate: {
      startOnLoad: false,
      theme: "dark",
      flowchart: {
        htmlLabels: false
      },
      er: {
        useMaxWidth: false
      },
      sequence: {
        useMaxWidth: false,
        noteFontWeight: "14px",
        actorFontSize: "14px",
        messageFontSize: "16px"
      }
    }
  }
}

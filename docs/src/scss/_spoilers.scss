/* Details polyfill */
.md-typeset {
  details {

    /* General common styling */
    display: block;
    margin: 1em 0;

    &[open] {
      > summary::before {
        content: "\25BC";
      }
    }

    summary {
      display: block;
      cursor: pointer;

      &::before {
        content: "\25B6";
        padding-right: 0.5em;
      }

      &::-webkit-details-marker {
        display: none;
      }
    }

    /* Styling for unsupported details with JavaScript */
    &.no-details {
      &:not([open]) {
        > * {
          display: none;
        }

        > summary {
          display: block;
        }
      }
    }
  }
}

/* Material styled spoilers */
.md-typeset {
  details {
    @each $names, $appearance in (
      note seealso: $clr-blue-a400 "edit",
      summary tldr: $clr-light-blue-a400 "subject",
      tip hint important : $clr-teal-a700 "whatshot",
      success check done: $clr-green-a400 "done",
      warning caution attention: $clr-orange-a400 "warning",
      failure fail missing: $clr-red-a200 "clear",
      danger error: $clr-red-a400 "flash_on",
      bug: $clr-pink-a400 "bug_report",
      quote cite: $clr-grey "format_quote",
      settings: $clr-purple-a700 "settings"
    ) {
      $tint: nth($appearance, 1);
      $icon: nth($appearance, 2);

      &.#{nth($names, 1)} {
        @include z-depth(2);

        position: relative;
        padding: 1.2rem;
        margin-bottom: 1rem;
        overflow: hidden;

        *:nth-child(2) {
          margin-top: 0;
        }

        *:last-child {
          margin-bottom: 0;
        }

        > summary {
          outline: none;
          position: relative;
          margin: -1.2rem -1.2rem 0 -1.2rem;
          padding: 0.5rem 3.2rem;
          background-color: $tint;
          color: $clr-white;

          &::after,
          &::before {
            position: absolute;
            top: 0.7rem;
            font-family: "Material Icons";
            font-size: 2rem;
            font-style: normal;
            font-variant: normal;
            font-weight: 400;
            line-height: 1;
            text-transform: none;
            white-space: nowrap;
            speak: none;
            word-wrap: normal;
            direction: ltr;
          }

          &::after {
            right: 1rem;
          }

          &::before {
            left: 1rem;
            content: $icon;
          }
        }

        &[open] {
          > summary {
            margin-bottom: 1.2rem;

            &::after {
              content: "keyboard_arrow_down";
            }
          }
        }

        &:not([open]) {
          padding-bottom: 0;

          > summary::after {
            content: "keyboard_arrow_left";
          }
        }
      }
    }
  }
}

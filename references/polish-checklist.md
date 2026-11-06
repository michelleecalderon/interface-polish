# Polish checklist

Use the sections that fit the requested scope. These checks guide visual judgment; they do not override a coherent project convention.

## Start with evidence

1. Locate the shared component, token, or style that governs the affected UI.
2. Inspect the rendered component at the sizes and color schemes it supports. Source code alone can establish implementation details; visual claims also need visual evidence.
3. Walk the relevant interaction states. Include touch or keyboard behavior when the component can receive those inputs.
4. Make the least invasive change that fixes the observed issue. Recheck the altered state and its neighbors.

## Typography

- Use `text-wrap: balance` for a short heading only when its rendered line breaks improve. Use `text-wrap: pretty` for longer prose when supported and it avoids a distracting final line. Check real narrow and wide widths.
- Consider `font-variant-numeric: tabular-nums` for counters, timers, prices, and tabular data that shift as values change. Confirm that the font's alternate figures suit the surface.
- Font smoothing is platform-specific. Compare rendered text on the target platform before changing a global text-rendering setting.
- Do not solve a line-break issue by shrinking type or tightening tracking until the component's available width and content constraints have been checked.

## Surfaces and visual alignment

- For a rounded child evenly inset within a rounded parent, use the visual guide `outer radius = inner radius + inset + border width`. Treat large or asymmetric spacing as separate surfaces and judge each radius independently.
- If an icon, a play symbol, or an icon-and-label group looks off-center, correct its visible mass rather than trusting mathematical centering. Prefer repairing an inaccurate SVG over accumulating one-off layout offsets.
- Keep borders that communicate structure, input boundaries, selection, or focus. Use a transparent shadow only when it adds useful elevation and fits the product's surface language.
- Add a subtle inset outline to an image only when it helps the image read against changing backgrounds or nearby surfaces. Skip transparent art, logos, and intentionally edge-to-edge imagery.
- Check surfaces in supported color schemes; an elevation treatment that works in light mode may become muddy or invisible in dark mode.

## Icons and control states

- Reuse the local icon family and make its apparent size and stroke compatible with nearby text. Inspect at the final rendered size, where stroke differences are most visible.
- Let icon colors derive from `currentColor` or existing tokens where possible. Use fill, opacity, and color consistently with the product's established meaning for active and inactive states.
- A control should remain understandable through visible text, color, shape, or state styling when its animation is disabled.
- Preserve a clear `:focus-visible` treatment. Do not let a hover adjustment erase it or make keyboard users rely on a pointer-only cue.
- Put hover-specific decoration behind a hover-capable media query when the existing styling system does not already do so. A latched `:hover` state after tapping is confusing on touch screens.

## Motion and response

- Use transitions or retargetable spring motion for hover, toggles, and open/close interactions so a changed user intent reverses smoothly. Use keyframes for finite sequences meant to run through once.
- Keep routine interactions immediate or brief. Save staggered entrances for infrequent moments where the sequence communicates hierarchy. Animate semantic groups, not every word or character by default.
- Keep an exit quieter than its entrance. Use opacity or a small translation when it provides adequate context; move fully off-screen only when the spatial destination matters, such as a drawer closing.
- Use icon swaps sparingly to explain a meaningful change, such as copy becoming copied. Keep the incoming and outgoing icons aligned in the same layout box.
- Name the properties that transition. Avoid `transition: all`; it can animate unintended changes. Add `will-change` only after observing a first-frame performance problem, and remove it when no longer needed.
- Respect `prefers-reduced-motion`. Replace movement, scaling, or blur with a short opacity change or an immediate state update when that better suits the component.
- Press-scale feedback can help buttons feel responsive, but it must not hide focus, distort layout, or run on disabled controls. Match the magnitude and timing to nearby controls rather than introducing a new gesture language.

## State coverage

Inspect only states that exist in the requested surface. Common checks include:

- Resting, hover, focus-visible, pressed, selected, and disabled states for controls.
- Open and closed states for toggles, menus, dialogs, and drawers.
- Loading, success, empty, and error states when the flow provides them.
- Narrow layouts, dark mode, and reduced-motion mode when the product supports them.

For small icon controls, preserve a practical pointer and touch target without allowing expanded hit areas to overlap adjacent controls.

## Decision test

Before changing a detail, ask:

1. What observed inconsistency or interaction problem does this solve?
2. Does the change fit existing tokens and nearby components?
3. Will it preserve readability, focus, keyboard and touch use, contrast, and reduced-motion behavior?
4. Can a shared component or token correct every affected instance?
5. Is the effect still useful if it is seen repeatedly throughout a session?

## Review report

State the scope and what you inspected. Then give each finding:

| Location | Observed issue | Recommended change | Why it helps |
| --- | --- | --- | --- |
| `path/to/component:line` or screen/component | Current rendered behavior or source evidence | Concrete change in the project's styling idiom | User-facing benefit and relevant principle |

Group repeated symptoms under the shared component or token. Mark an unchecked state as unverified instead of inferring it. Do not pad a report with preferences or changes that merely make the interface more decorative.

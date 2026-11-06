---
name: interface-polish
description: Improve or review visual and interaction details in an existing interface. Use for UI polish involving typography, component surfaces, icons, states, motion, and responsive behavior; do not use for a full visual redesign.
---

# Interface Polish

Use this skill when the user wants an existing interface to feel more finished, or when implementing a component where small visual details matter. Improve clarity, consistency, and feedback without changing the product's visual identity, information architecture, or interaction model unless asked.

## Establish the local visual language

Before editing, identify the framework, styling approach, component library, design tokens, and nearby component conventions. Follow the existing system and reuse shared components and values. Prefer one repair at the shared source over many local patches. Do not add a dependency or styling system for a polish detail.

Visual consistency is evidence, but personal taste is not a defect. Preserve deliberate project conventions, such as flat surfaces or restrained motion, when they are consistently applied.

## Choose the right mode

**Implementation.** Make only the changes that solve an observed issue or complete an explicitly requested treatment. Keep the behavior accessible and the implementation idiomatic for the project.

**Review.** Remain read-only unless implementation is also requested. State the inspected scope, evaluate the relevant states, and report only findings supported by the rendered interface or source evidence. Do not present unobserved visual behavior as fact.

For either mode, read [references/polish-checklist.md](references/polish-checklist.md) for the decision guide, state coverage, and reporting format. For implementation, read [references/implementation-recipes.md](references/implementation-recipes.md) only for the project's actual stack: CSS, Tailwind, React Motion, GSAP, or Three.js. For color, focus, motion, control, or target-size work, read [references/wcag-accessibility.md](references/wcag-accessibility.md); run `scripts/check_contrast.py` when the foreground and background colors can be resolved to hex values.

## Apply high-value refinements

- **Text:** Choose line wrapping based on content length and viewport; stabilize live numeric values when their changing width disrupts nearby content.
- **Surfaces:** Treat nested radius, depth, image edges, and icon placement as visual relationships. Correct them when they look wrong in their rendered context.
- **Feedback:** Make resting, hover, focus, pressed, selected, loading, and disabled states easy to distinguish. Do not make motion the only sign that something changed.
- **Motion:** Use reversible transitions for user-driven state changes. Reserve staged motion for infrequent moments where it explains hierarchy or direction. Respect `prefers-reduced-motion`.
- **Input contexts:** Do not let touch devices inherit a sticky hover treatment. Keep visible focus behavior, keyboard operation, and practical target sizes intact while polishing controls.

Avoid decorative changes with no user-facing benefit. Do not use broad transitions, permanent performance hints, or motion that makes routine actions slower or harder to parse.

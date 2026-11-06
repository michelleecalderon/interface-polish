# WCAG accessibility guardrails

This reference targets common interface-polish regressions. It is not a claim of complete WCAG conformance: automated checks cannot establish a page's semantics, keyboard behavior, reading order, error recovery, or the contrast of every rendered layer.

## Contrast

Check the effective foreground and background pair for each meaningful state, including default, hover, selected, disabled, and focus-visible where applicable. Use the script when both colors can be expressed as hex values:

```bash
python3 scripts/check_contrast.py '#595959' '#ffffff' --kind text --level AA
python3 scripts/check_contrast.py '#767676' '#ffffff' --kind ui
python3 scripts/check_contrast.py '#000000cc' '#ffffff' --kind text --canvas '#ffffff'
```

The third command demonstrates alpha compositing. Supply the actual opaque layer behind a transparent color with `--canvas`; if the background is an image, gradient, video, blend mode, or varies by position, inspect the rendered extremes instead.

| Content | WCAG 2.2 check | Minimum ratio |
| --- | --- | --- |
| Normal text and images of text | 1.4.3 AA | 4.5:1 |
| Large text (about 24px regular or 18.5px bold) | 1.4.3 AA | 3:1 |
| Normal text at AAA | 1.4.6 AAA | 7:1 |
| Large text at AAA | 1.4.6 AAA | 4.5:1 |
| Required component boundaries, icons, and focus indicators | 1.4.11 AA | 3:1 against adjacent colors |

Do not round a calculated result up to a threshold. A ratio just below `4.5:1` still fails the normal-text AA threshold.

Text rendered over a changing image or gradient needs a stable backing surface, sufficient shadow/overlay treatment, or an alternate layout that produces a reliably testable pair. Do not assume a color passes because it works in one part of an image.

## Focus and states

- Every keyboard-operable control needs a visible focus indicator. Preserve the browser's focus indicator when it already meets the product's needs; otherwise provide a clearly visible `:focus-visible` treatment.
- Test the focus indicator against each adjacent surface it can touch. A focus ring is non-text visual information and needs adequate contrast.
- Do not communicate validation, selection, status, or an error through color alone. Pair color with text, an icon whose meaning is available to assistive technology, shape, or another persistent visual difference.
- Disabled controls can have reduced contrast, but do not use a disabled appearance for an actionable control. Ensure the reason for an unavailable action is discoverable when users need it.

```css
.control:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

Keep the project's focus design if it is already visible and consistent. Do not replace an accessible browser focus ring with a subtle shadow that is hard to distinguish on some surfaces.

## Controls and targets

- Prefer native controls (`button`, `a`, `input`, `select`) before recreating them with generic elements. If a custom control is necessary, it must preserve its name, role, keyboard operation, state, and focus behavior.
- WCAG 2.2 AA requires pointer targets to be at least `24×24` CSS pixels or meet a documented spacing exception. A `44×44` target is a stronger, touch-friendly goal for important or touch-first controls.
- Expand small visual icon targets without creating overlapping hit areas. Check adjacent controls at narrow widths.
- Keep labels available for icon-only controls through visible text, an accessible name, or both. The tooltip is not a substitute for an accessible name.

## Motion

- Honor `prefers-reduced-motion` for non-essential movement, zooming, blur, parallax, and auto-playing decorative sequences. Provide an opacity-only or immediate alternative where appropriate.
- Do not make a moving transition the only evidence that a state changed. Keep a durable text, icon, color, or structural cue after motion completes.
- Avoid non-essential scrolling effects and perpetual attention-seeking loops. When animation is essential to the feature, expose a comprehensible, controllable alternative.

## Review evidence

Record measurable contrast separately from interaction and semantic checks:

| Surface / state | Check | Evidence | Result |
| --- | --- | --- | --- |
| `Button / focus-visible` | Focus ring contrast | `#...` on `#...`, calculated ratio | Pass / fail / unverified |
| `Icon button / default` | Target and accessible name | Rendered size and source location | Pass / fail / unverified |
| `Drawer / opening` | Reduced-motion behavior | Rendered behavior or source location | Pass / fail / unverified |

Mark a case unverified when colors cannot be resolved or the interaction cannot be observed. Do not describe an interface as WCAG compliant unless the requested evaluation actually covers the relevant success criteria and evidence.

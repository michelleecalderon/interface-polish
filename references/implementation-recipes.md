# Implementation recipes

Choose the project's existing motion stack. Do not add a library for a small polish change. CSS handles most interaction feedback; use React Motion or GSAP only when they are already present and their coordination or lifecycle features materially help.

## Plain CSS

### A control with clear, touch-safe feedback

Use targeted transitions and retain a visible focus state. Put hover-only decoration behind a capability query so it cannot stick after a touch interaction.

```css
.control {
  transition:
    background-color var(--motion-fast, 150ms) ease-out,
    box-shadow var(--motion-fast, 150ms) ease-out,
    transform var(--motion-fast, 150ms) ease-out;
}

.control:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

@media (hover: hover) {
  .control:hover:not(:disabled) {
    box-shadow: var(--control-shadow-hover);
  }
}

@media (prefers-reduced-motion: no-preference) {
  .control:active:not(:disabled) {
    transform: scale(0.98);
  }
}

@media (prefers-reduced-motion: reduce) {
  .control {
    transition: background-color var(--motion-fast, 150ms) ease-out,
      box-shadow var(--motion-fast, 150ms) ease-out;
  }
}
```

Use project tokens in place of the fallback values. Omit the press scale when the local control language does not use it.

### A reversible panel transition

Represent open and closed state with a class or data attribute and use a transition, so a second click retargets the animation. Avoid applying `display: none` until the panel has finished leaving if the exit needs to be visible.

```css
.panel {
  opacity: 0;
  pointer-events: none;
  transform: translateY(-0.25rem);
  transition:
    opacity var(--motion-medium, 200ms) ease-out,
    transform var(--motion-medium, 200ms) ease-out;
}

.panel[data-state="open"] {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .panel {
    transform: none;
  }
}
```

Keep the focus-management and accessibility behavior of a menu, dialog, or drawer in the component itself; a visual transition does not provide it.

### A contextual icon swap

Keep both icons in one layout box so the control does not shift. Use opacity as the reduced-motion fallback.

```css
.icon-swap {
  display: grid;
  place-items: center;
}

.icon-swap > svg {
  grid-area: 1 / 1;
  transition:
    opacity var(--motion-fast, 150ms) ease-out,
    transform var(--motion-fast, 150ms) ease-out;
}

.icon-swap[data-state="complete"] .icon-default,
.icon-swap:not([data-state="complete"]) .icon-complete {
  opacity: 0;
  transform: scale(0.9);
}
```

Add blur only when the project already uses it sparingly and gate it behind `prefers-reduced-motion: no-preference`.

## Tailwind CSS

Use the utilities and tokens already configured by the project. Tailwind versions differ in how hover media queries are emitted, so check the installed version before assuming `hover:` is touch-safe.

```tsx
<button
  className="
    transition-[background-color,box-shadow,transform] duration-150 ease-out
    focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
    focus-visible:outline-[color:var(--focus-ring)]
    motion-safe:active:scale-[0.98]
    disabled:pointer-events-none disabled:opacity-50
  "
>
  Save changes
</button>
```

For a stateful icon, stack the icons in the same grid cell. Keep the state name in a variable or a semantic data attribute rather than encoding it in unrelated styling.

```tsx
<span className="relative grid size-4 place-items-center" aria-hidden="true">
  <CopyIcon
    className={cn(
      "col-start-1 row-start-1 transition-[opacity,transform] duration-150 ease-out",
      copied && "scale-90 opacity-0"
    )}
  />
  <CheckIcon
    className={cn(
      "col-start-1 row-start-1 transition-[opacity,transform] duration-150 ease-out",
      copied ? "scale-100 opacity-100" : "scale-90 opacity-0"
    )}
  />
</span>
```

Where a component uses nested rounded surfaces, choose existing radius and spacing tokens whose rendered corners appear concentric. Do not introduce one-off arbitrary values when the design system has an appropriate pairing.

## React Motion

Use the package already in the project: `motion/react` for Motion or `framer-motion` for Framer Motion. Do not mix their import paths. Use `AnimatePresence` for a component that needs an exit animation; its direct children need stable, unique keys.

```tsx
import { AnimatePresence, motion, useReducedMotion } from "motion/react";

function CopyStatusIcon({ copied }: { copied: boolean }) {
  const reduceMotion = useReducedMotion() ?? false;
  const hidden = reduceMotion
    ? { opacity: 0 }
    : { opacity: 0, scale: 0.9, filter: "blur(2px)" };

  return (
    <AnimatePresence initial={false} mode="wait">
      <motion.span
        key={copied ? "copied" : "copy"}
        className="grid size-4 place-items-center"
        initial={hidden}
        animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
        exit={hidden}
        transition={{ duration: 0.15, ease: "easeOut" }}
      >
        {copied ? <CheckIcon aria-hidden="true" /> : <CopyIcon aria-hidden="true" />}
      </motion.span>
    </AnimatePresence>
  );
}
```

When the component's default state should appear immediately, keep `initial={false}` on its state-swap `AnimatePresence`. Do not apply it to an intentional first-load entrance. Use CSS or component state for ordinary hover feedback; reserve Motion for state swaps, coordinated entrances, gesture response, or layout transitions that need it.

## GSAP

Use GSAP only when the project already depends on it and a coordinated timeline, scroll scene, or complex SVG/canvas sequence needs it. A button hover, tab switch, or popover opening normally belongs in CSS or the local React motion library.

In React, scope animations to the component and clean them up on unmount. `gsap.context()` provides both selector scoping and a `revert()` cleanup path.

```tsx
import { useLayoutEffect, useRef } from "react";
import { gsap } from "gsap";

function FeatureIntro() {
  const root = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const context = gsap.context(() => {
      const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      if (reduced) {
        gsap.set("[data-intro-item]", { autoAlpha: 1 });
        return;
      }

      gsap.from("[data-intro-item]", {
        autoAlpha: 0,
        y: 12,
        duration: 0.35,
        ease: "power2.out",
        stagger: 0.08,
      });
    }, root);

    return () => context.revert();
  }, []);

  return (
    <div ref={root}>
      <h2 data-intro-item>Understand progress at a glance</h2>
      <p data-intro-item>Keep the sequence short and purposeful.</p>
    </div>
  );
}
```

Do not add perpetual animation loops to interface chrome. For `ScrollTrigger` and event-created timelines, keep their setup within the same scoped lifecycle and confirm that reduced-motion users receive a stable, readable end state.

## Three.js

Three.js is not a general UI-polish tool. Use it only when the project already has a 3D scene or the requested experience genuinely depends on spatial content, such as a product model, data scene, or interactive narrative. Do not introduce a canvas to make an ordinary card, button, or navigation element feel more premium.

Keep semantic navigation, controls, labels, and form inputs in the DOM. A canvas should enhance the experience, not become the only way to understand or operate it.

For an existing scene:

- Respect reduced motion by pausing non-essential camera/object movement or rendering a stable frame.
- Start the render loop only while the scene is visible and needed; pause it for hidden tabs or off-screen scenes.
- Clean up the animation frame, renderer, controls, geometries, materials, and textures when the component unmounts.
- Prefer CSS and DOM overlays for focusable controls; do not rely on a canvas hit target for essential actions without an equivalent accessible path.
- Test lower-power devices and narrow screens before adding post-processing, high-resolution shadows, or continuous interaction effects.

If the project uses React Three Fiber, follow its existing component and cleanup conventions. Do not mix an imperative Three.js renderer into an established React Three Fiber scene for a minor effect.

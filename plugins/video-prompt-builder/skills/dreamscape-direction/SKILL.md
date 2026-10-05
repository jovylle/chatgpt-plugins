---
name: dreamscape-direction
description: Apply a specific golden-hour dreamscape aesthetic to image, video, or scene prompts - warm low sun, hazy tinted sky, sky-reaching massifs, warm hard-edged moon clusters, dreamlike awe composition. Use when the user asks for a dreamlike, ethereal, awe, fantasy, or landscape scene, or when a prompt should feel like a dreamscape rather than a literal place.
---

# Dreamscape Direction

A specific house style for prompts: **the golden-hour dream**. Warm low sun,
tinted hazy sky, big "reach the sky" landforms, dreamlike composition.

Use this as a layer over `keyframe-builder` or `video-prompt-builder` — it sets
palette, light, and composition, not the action. When the user has already
specified a style, theirs wins; apply this only on request or when the brief is
open.

## Identity

- **Light:** warm low sun, close to the horizon. Long directional shadows, warm
  on lit faces, cool in shadow.
- **Sky:** tinted and hazy, not clear blue. Turbid, atmospheric, gradient from
  warm horizon to deeper tone overhead.
- **Landform:** at least one feature that reaches the sky and dominates the
  frame. Scale is the point — the landscape outweighs the subject.
- **Mood:** dreamlike, awe, calm-but-vast. Never harsh, never neon, never
  dystopic by default.
- **Air:** warm coloured fog that separates depth planes and hides the horizon
  seam. Distance reads as haze, never as a hard edge.

## Palettes

Pick one and commit. Mixing two reads as muddy.

| Palette | Sky | Sun / key | Fill / bounce |
|---|---|---|---|
| Golden hour | warm amber to deep orange | `#ff8c3a` | cool blue `#8fa8ff` |
| Ember dusk | burnt orange to violet | deep red-orange | soft violet |
| Moonlit warm | muted indigo | pale warm cream | faint amber |

State fog colour explicitly. Warm fog (`#ff9d66`) is the house default.

## Moons

Moons are a signature element and follow a hard rule:

- **Warm** — clearly warmer than the sky, red channel dominant.
- **Hard-edged matte disc** — a crisp circular boundary, like the moon seen
  through haze.
- **No halo, no bloom, no glow.** A moon with a soft luminous halo is wrong for
  this style. Describe it as a flat bright disc, not a glowing orb.
- **Clearly brighter than the surrounding sky**, or it reads as a smudge.

Cluster them. A group of warm discs at varied sizes reads as a deliberate
composition rather than a stock asset.

## Composition

- **Hero massifs** occupy roughly 45% of frame width and sit high enough to
  break the horizon. Big can mean close.
- **Fill ~45% of the frame with landform.** If the sky dominates and the land is
  a thin strip, the scale is lost.
- **No bare horizon in any direction.** Whatever the camera faces, there is
  landform, haze, or layered depth — never an empty band. This matters for
  video especially, where the camera turns.
- **Layer for depth:** near silhouette, midground subject, far ridge bands.
- Keep the horizon off dead centre.

## Things that break the style

- Clear blue sky, or a sky with visible hard cloud banding
- Cold moonlight as the only key light
- Glowing, haloed, or lens-flared moons
- Thin distant hills with empty sky above them
- Neon, cyberpunk, or high-contrast teal-and-orange grading
- Birds rendered as small scattered specks in frame
- Any readable text, signage, or UI in the scene

## Output

Apply the palette and composition as concrete prompt language. Deliver the
finished prompt in a code block — the user should be able to paste it directly.
---
name: keyframe-builder
description: Build a precise still-image prompt to serve as the visual anchor keyframe for an image-to-video clip. Use when the user needs a starting frame generated (Veo, Seedream, Gemini, Midjourney, Flux) before a motion prompt is written, or when an existing keyframe is too busy to animate cleanly.
---

# Keyframe Builder

Produce one copy-ready still-image prompt whose only job is to be a **clean,
unambiguous visual anchor** that a video model can hold steady.

The keyframe and the motion prompt are a pair. Build the still first, then hand
it to `video-prompt-builder` for the motion. Never fold camera movement or
temporal language into a still prompt — a keyframe describes one instant.

## What makes a keyframe animatable

Video models drift when the source frame is ambiguous. Every anchor must resolve
these before the first frame is generated:

- **One clear subject.** If two things compete for attention, pick one as hero.
- **Separated depth planes.** Foreground, midground, background must be
  distinguishable by value, scale, or blur — not by outline alone.
- **A readable silhouette.** The hero's outline must not merge into the
  background behind it.
- **No text in the image.** Never ask for readable signage, captions, UI, or
  labels. Small text becomes noise and confuses the video model.
- **No motion blur.** Freezing the instant is what makes the anchor usable.
- **An unambiguous light direction.** One dominant source, stated once.

## Prompt structure

Use this order:

1. Subject and its defining traits
2. Environment and depth layering
3. Lighting — direction, quality, colour
4. Camera — framing, angle, lens feel
5. Palette and mood
6. Constraints, only when they prevent a specific failure

Keep it to one paragraph. A keyframe prompt is a specification, not a scene
description.

## Composition defaults

Unless the user asks otherwise:

- Frame the hero at roughly 45% of frame width — present enough to read,
  leaving room for the environment to establish scale.
- Keep the horizon out of dead centre. Place it low for scale and awe, high for
  intimacy.
- Give the hero breathing room in the direction it faces.

## Ready-to-adapt patterns

Establishing shot:

> `<subject>, <defining traits>, <environment with distinct depth planes>,
> <lighting direction and quality>, <camera framing and lens>, <palette and
> mood>. Sharp, no motion blur, no text anywhere in frame.`

Portrait anchor:

> `<subject>, <defining traits>, chest-up framing, <lighting direction>,
> shallow depth of field with the background clearly separated,
> <palette>. Sharp detail, no motion blur, no text.`

Continuation anchor (matching an existing clip):

> Continue directly from the exact final frame. Hold the established visual
> state: <restate the non-negotiables — lighting, palette, subject traits,
> framing>. <State the new instant.> Sharp, no motion blur, no text.

## Before returning

Check the prompt resolves subject, depth, silhouette, and light. If any of the
four is implied rather than stated, state it — that ambiguity is what causes
continuity drift in the motion pass.

## Output

One copy-ready prompt in a code block. Add one line only when a model-specific
setting materially changes the result. No explanation unless asked.
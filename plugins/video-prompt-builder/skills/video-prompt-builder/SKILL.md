---
name: video-prompt-builder
description: Build concise, production-ready prompts for short AI video clips from a scene idea or clean keyframe. Use when the user needs image-to-video prompts for Veo, Wan, Seedance, or similar models, especially when visual continuity matters.
---

# Video Prompt Builder

Convert the user's scene request into a compact motion prompt designed for image-to-video generation.

## Core rule

Treat the supplied keyframe as the exact visual state at the start of the clip. The prompt should primarily describe what moves, changes, or transitions. Do not restate every visible detail unless needed to prevent continuity drift.

## Preserve continuity

Assume these remain unchanged unless the user explicitly asks otherwise:
- characters, faces, body proportions, clothing, props
- environment and spatial layout
- camera framing, lens feel, and composition
- time of day, lighting direction, and visual style

For continuation clips, explicitly say to continue directly from the exact final frame and preserve the established visual state.

## Prompt structure

Use this order when useful:
1. Continuity anchor
2. Primary subject motion
3. Secondary reactions or environmental motion
4. Camera motion
5. End state
6. Constraints / negatives only when they materially reduce errors

Keep prompts focused. Avoid storyboards, shot lists, scene diagrams, labels, or instructions that require the video model to read tiny text inside a reference image.

## Timing

For 6-10 second clips, favor one clear action with a natural progression. Avoid packing multiple major actions into one short clip unless the user explicitly asks for a rapid sequence.

Describe temporal progression with phrases such as:
- "over the first few seconds"
- "then gradually"
- "by the end of the clip"

## Camera

Only add camera movement when it helps the requested effect. Prefer simple language such as:
- slow push-in
- subtle handheld drift
- slight pan
- locked-off camera

Do not invent camera movement when the user did not request it and the keyframe already provides suitable framing.

## Jumpscares / reveals

For a reveal, preserve the initial frame exactly, build tension through small motion, then introduce the subject at a specific moment or spatial location. Make the final state unambiguous.

Example pattern:
"Continue directly from the exact final frame. The camera stays mostly fixed. The subject remains still for a moment, then slowly leans into view from [location], moving closer toward the frame. End with [clear final composition]."

## Physically impossible or surreal scenes

Do not normalize an impossible premise. Describe the impossible behavior as part of the physical action while keeping textures, lighting, and environment realistic when requested.

## Aspect ratio

Do not change the aspect ratio in the prompt unless the user asks for it. Treat aspect ratio as an external generation setting when supported.

## Output style

Default to one copy-ready prompt in a code block, followed by a one-line note only when a model-specific setting materially matters. Do not add unnecessary explanation.

## When the user provides only an idea

Create the minimum scene assumptions needed to make the motion coherent. Do not invent detailed character backstories or visual traits unless necessary.

## When the user asks for a rewrite

Keep the user's intended action intact while removing redundant visual description, conflicting instructions, and model-hostile wording.

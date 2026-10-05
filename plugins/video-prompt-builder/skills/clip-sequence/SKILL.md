---
name: clip-sequence
description: Plan and write a multi-clip AI video sequence where every clip shares one continuous visual state. Use when the user needs several connected shots from one scene, a sequence that must stitch together, a longer narrative built from short clips, or when previous clips have drifted apart visually.
---

# Clip Sequence

Single-clip prompting is handled by `video-prompt-builder`. Use this skill when
there are **two or more clips that must look like one continuous piece** — the
case where per-clip prompts independently drift and the result falls apart on
the cut.

## The one rule

Write the **visual state once**, then reference it per clip. If each clip prompt
restates the full description, the model re-interprets it every time and the
sequence drifts. Establish the state, then describe only what changes.

## Step 1 — Lock the shared state

Before writing any clip, fix these and hold them constant across the whole
sequence:

- Subject identity: face, build, clothing, distinguishing features
- Environment and spatial layout
- Light source, direction, and colour
- Palette
- Camera language: lens feel, height, framing conventions
- Weather or atmosphere state

State this block once. It is the contract for every clip.

## Step 2 — Assign each clip one change

Each clip gets exactly one primary change from the shared state. Everything else
stays put. This is what makes a sequence read as continuous rather than as
unrelated shots that happen to share a colour grade.

| Clip | Single change |
|---|---|
| 1 | Establishes the state — subject still or barely moving |
| 2 | Subject begins primary action |
| 3 | Action develops, or camera moves for the first time |
| 4 | Action resolves toward an end state |

Avoid giving any clip two major actions. Across a sequence, restraint reads as
control; constant motion reads as noise.

## Step 3 — End each clip on a handoff state

Every clip except the last must end on a state the next clip can start from
exactly. Say what the final frame looks like:

> End with `<subject>` `<final position/posture>`, `<camera at final framing>`,
> `<light unchanged>`.

The next clip then opens: *"Continue directly from the exact final frame."*

## Step 4 — Check the joins

Before delivering, verify for every boundary:

- The next clip's opening state matches the previous clip's stated end state
- No clip contradicts the shared state block
- No clip changes the light direction or palette
- Total motion across the sequence is progressive, not repetitive

If a join fails, fix the earlier clip's end state — a drift caught mid-sequence
means the mismatch started upstream.

## Timing across clips

Short clips of 6–10 seconds each. Keep per-clip action minimal; let the sequence
carry the narrative. Match cut rhythm to intent — even lengths for a calm
survey, varied for building tension.

## Delivery

Give the shared state block once, then each clip's motion prompt in order, each
in its own code block and labelled with its position in the sequence. Note any
clip where the handoff needs particular attention.

Do not restate the shared state inside every clip prompt. That is the failure
mode this skill exists to prevent.
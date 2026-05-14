# Layout Style Index

Six reusable layouts. Each has a dedicated SVG file in this folder. **Read the SVG before drawing**

**it has the exact coordinate math, font sizes, and container patterns you should mimic.**

| ID | File                                 | Pattern                                                           | When to open                                                                                 |
| -- | ------------------------------------ | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 01 | `style_01_layered_network.svg`     | Multi-stage layered with grouped containers and a legend block    | Neural network architectures, multi-stage pipelines where each stage has internal sub-blocks |
| 02 | `style_02_horizontal_pipeline.svg` | Single horizontal flow, modules in a row with arrows              | Linear algorithms, simple data pipelines, "X → Y → Z" workflows                            |
| 03 | `style_03_modular_system.svg`      | Grid of equally-weighted modules with explicit inter-module links | System architectures, software component diagrams, "what talks to what"                      |
| 04 | `style_04_hierarchy.svg`           | Top-down tree with one root, branches outward                     | Taxonomies, decision trees, organizational/method hierarchies                                |
| 05 | `style_05_cycle_feedback.svg`      | Closed loop with curved feedback arrows                           | Iterative methods, training loops, control systems, "this feeds back to that"                |
| 06 | `style_06_dual_track.svg`          | Two parallel horizontal tracks with cross-connections             | Comparison flows (baseline / proposed), encoder / decoder, train / inference               |

When the user input doesn't clearly fit, **ask before drawing**. A wrong layout choice is the most expensive error to fix !!!

## Style elements that are constant across all six layouts

These are the visual signatures of the "Pastel Academic" look. Keep them consistent regardless of which layout you pick:

1. **Containers** = large rounded rectangle with light pastel fill, darker border of the same hue, a bold title in the top-left, and a small grey annotation under the bottom-right.
2. **Modules** = smaller rounded rectangles (rx=6, ry=6), saturated fill, no border or 1px border of a darker shade, white or near-black text inside.
3. **Connectors** = grey arrows (#6B7280), 2-2.5px stroke, with a proper arrowhead marker.
4. **Skip / feedback connections** = dashed (`stroke-dasharray="6,4"`), lighter grey (#9CA3AF), often curved.
5. **Annotations** = small grey text (12-13pt) below containers or beside arrows.
6. **Legend** = standalone small rectangle bottom-left or top-left, color swatches + short labels.
7. **Font** = Times New Roman for English/math, plus a CJK-capable family (Noto Sans CJK SC, SimHei) for Chinese. The diagram must specify both via `font-family` so CJK doesn't fall back to tofu boxes.

## How to combine elements across layouts

You are allowed (encouraged) to **mix elements between styles** — e.g. take a layered_network main body and add a feedback curve from style_05 if the architecture genuinely loops. The six layouts are starting points, not cages.

## What you cannot do

- Mix palettes within one diagram.
- Mix font systems (pick CJK+TNR or pure TNR for the whole diagram).
- Change arrow style between connectors of the same logical type.

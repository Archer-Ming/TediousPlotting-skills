# Palettes for Architecture Diagrams

* Each palette is a **pair set**: every "module color" has a `fill` (light pastel for backgrounds/containers) and a `solid` (saturated version for module blocks of the same family). Borders use the `solid` value at 60-80% opacity, or you can darken `solid` by about 15%.
* The **neutrals row** is shared across all palettes. Use `arrow` for connectors, `text_primary` for module labels, `text_secondary` for annotations under containers, `bg` as the canvas if you need one.

## Shared neutrals

```
arrow            #6B7280   (medium grey, all connectors)
arrow_dashed     #9CA3AF   (lighter grey, for shortcut/skip lines)
text_primary     #1F2937   (near-black, all module labels)
text_secondary   #4B5563   (grey, annotations and dimensions)
text_white       #FFFFFF   (text inside saturated solid blocks)
bg               #FFFFFF   (canvas background)
divider          #E5E7EB   (separator lines if needed)
```

---

## Palette 1: Pastel Academic  *(default)*

Best for: ML/DL architectures, system diagrams with 4-6 module families. Reads as "modern Chinese journal".

| Family   | fill (container) | solid (module) | use case                         |
| -------- | ---------------- | -------------- | -------------------------------- |
| blue     | `#DCE7F5`      | `#7BA7D9`    | input layers, data blocks        |
| mint     | `#D6EBD6`      | `#88C088`    | conv / processing blocks         |
| peach    | `#FFE0CC`      | `#F0A776`    | pooling, normalization           |
| pink     | `#FAD6D6`      | `#E89090`    | dropout, regularization, warning |
| lavender | `#E5D9F2`      | `#B197D6`    | output, FC, classification head  |
| grey     | `#E5E7EB`      | `#9CA3AF`    | legend, auxiliary, "off" state   |

---

## Palette 2: Nature Crisp

Best for: Nature/Cell submissions. Slightly more saturated, cleaner.

| Family | fill        | solid       | use case         |
| ------ | ----------- | ----------- | ---------------- |
| blue   | `#D6E4F0` | `#3B7AB8` | data / input     |
| green  | `#D8EAD8` | `#5BA85B` | processing       |
| amber  | `#FBE6C2` | `#E8A53C` | transformation   |
| rose   | `#F6D5D5` | `#D85F5F` | alert / output   |
| slate  | `#DDE4EA` | `#5A6B7A` | meta / auxiliary |

---

## Palette 3: IEEE Engineering

Best for: Engineering pipelines, system architectures, robotics. More technical feel.

| Family   | fill        | solid       | use case                 |
| -------- | ----------- | ----------- | ------------------------ |
| steel    | `#D4DBE5` | `#4A6FA5` | hardware / input         |
| teal     | `#CFE5E1` | `#3F9285` | computation / processing |
| orange   | `#F4D9BD` | `#D67D2C` | actuator / output        |
| crimson  | `#EBC9C9` | `#B0413E` | feedback / control loop  |
| graphite | `#D9DDE2` | `#52606D` | sensor / measurement     |

---

## Palette 4: Warm Bio

Best for: Biology / chemistry / medical workflows. Avoids the "cold ML diagram" look.

| Family     | fill        | solid       | use case                |
| ---------- | ----------- | ----------- | ----------------------- |
| terracotta | `#EED2C2` | `#C97B5C` | sample / specimen       |
| sage       | `#D8E2C9` | `#8AA86B` | reaction / process      |
| sand       | `#F0E1C2` | `#D4AB52` | reagent / intermediate  |
| dustyrose  | `#E8CCC9` | `#BC7872` | result / readout        |
| stone      | `#D9D6CD` | `#7A736B` | environmental / control |

---

## Palette 5: High Contrast Mono+Accent

Best for: When the diagram itself is complex and you want one accent to draw the eye. Greys + one bold color.

| Family | fill        | solid       | use case                   |
| ------ | ----------- | ----------- | -------------------------- |
| grey-1 | `#F3F4F6` | `#9CA3AF` | most blocks                |
| grey-2 | `#E5E7EB` | `#6B7280` | containers                 |
| grey-3 | `#D1D5DB` | `#4B5563` | secondary blocks           |
| accent | `#FEE2E2` | `#DC2626` | the ONE highlighted module |

---

## How to pick

- User says nothing specific → **Palette 1**.
- User mentions Nature/Cell/Science or "high-end" → **Palette 2**.
- User says engineering / pipeline / system / hardware → **Palette 3**.
- User says biology / chemistry / clinical / wet-lab → **Palette 4**.
- Diagram has >8 modules of similar weight, or user wants minimal → **Palette 5**.

 **Mixing palettes is forbidden!!!**

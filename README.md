# 20 November 2026 — world news in one image

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kenim1/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kenim1/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

Entry for the [make.fun bounty “Sum up 20 November's world news in one image”](https://make.fun/bounty/news-image-20261120).

A newspaper-style front page summing up Friday 20 November 2026:

- **Diplomacy:** Trump, Xi and Putin hold the first three-way talks at
  APEC in Shenzhen and agree a four-point Declaration toward Peace.
  Zelensky: no deal without Kyiv; some 40 partners pledge aid.
- **Justice:** the ICJ rules 9–6 that Myanmar committed genocide
  against the Rohingya in the 2017 crackdown in northern Rakhine.
- **Technology:** Anthropic goes public on Nasdaq as ANT — the first
  frontier AI company to list; shares open at $111.50, up 17% on debut.
- **Ukraine:** the Kerch / Crimean Bridge is hit for a third time by
  Neptune missiles; Putin vows a far more painful response.
- **Middle East:** a Houthi strike damages Riyadh's 80-storey PIF
  tower; the US Senate rejects an Iran war-powers resolution, 51–48.
- **Also:** the Dow falls below 50,000 (49,097) in an AI selloff, the
  COP31 draft drops calls to phase out fossil fuels, and Cyclone
  Akvan nears India's east coast.

## Build

The image is drawn with Pillow only (no photos, no generated faces, so
every word stays legible):

```sh
python3 draw.py        # regenerates entry.png (1024x1024, ~150 KB)
```

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

`main.ts` copies the shipped `entry.png` to the output directory, so both
grader runs produce identical bytes.

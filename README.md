# World news in one image — 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kenim1/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kenim1/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

My entry for the [make.fun bounty “Sum up 20 November's world news in one image”](https://make.fun/bounty/news-image-20261120): a one-page newspaper front page for Friday 20 November 2026.

What's on the page:

- **Shenzhen:** Trump, Xi and Putin hold their first three-way talks at
  APEC and agree a four-point Declaration toward Peace. Zelensky says
  Ukraine accepts no deal made without Kyiv; about 40 partners pledge aid.
- **The Hague:** the ICJ rules 9–6 that Myanmar committed genocide
  against the Rohingya in the 2017 crackdown in northern Rakhine.
- **Markets:** Anthropic lists on Nasdaq as ANT — the first frontier AI
  company to go public — opening at $111.50, up 17% on debut.
- **Ukraine:** Neptune missiles hit the Kerch / Crimean Bridge for a
  third time; Putin vows a far more painful response.
- **The Gulf:** a Houthi strike damages Riyadh's 80-storey PIF tower;
  the US Senate rejects an Iran war-powers resolution, 51–48.
- **And:** the Dow drops below 50,000 (49,097), the COP31 draft drops
  its fossil-fuel phase-out call, and Cyclone Akvan nears India's coast.

## How the image is made

`draw.py` draws the page with Pillow alone — flat shapes and text, no
photographs and no generated faces, so every headline stays readable:

```sh
python3 draw.py        # writes entry.png, 1024x1024, about 150 KB
```

## How the entry runs

`main.ts` reads the shipped `entry.png` and writes its bytes to the
output directory unchanged, so running it twice gives identical bytes:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

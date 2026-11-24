[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b139-heroes-scene/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b139-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up 23 November 2026's world news: the AI rout that hit Asian
markets, the UN chief's call to regulate AI before it's too late, and the US lead
over China falling to a record low.

## What's inside

- **3 hero scenes** — Kospi's -3.3% slide (4,708.54, -161 pts), Guterres' call for
  AI rules at the Bridgetown summit (150 delegates), and the Asia Power Index
  (US 78.9 vs China 73.6, gap 5.3 — narrowest since 2018).
- **Number strip** — -3.3% Kospi · 5.3 power gap · 11,762 Ebola cases (DRC) ·
  10T won Seoul fund · 2% billionaire tax · $450M Skubal deal · 165 missiles/week ·
  12,000 cleared in Manchester · 264 kg explosives seized · $107.3B Anthropic IPO.
- **10 stories** — Bessent/Nvidia, the NCIC hack, Iran strikes, Nasdaq futures,
  Skubal's Mets deal, Tom Jackson, SpaceX sued, Anthropic's IPO, Poland's
  missile claim, and the Russian nuclear-satellite warning.
- **World map + 18 more stories**, plus a DATE CHECK box that keeps out
  lookalike stories from other dates (Dems 258, Sparta II, El Chapo, the
  EU–Indonesia pact, the Nigeria boat, the ICJ Myanmar ruling).

## How to run

```sh
python3 draw.py        # renders entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + copies entry.png to out/
```

`main.py` is stdlib-only and validates the PNG (signature, IHDR 1024x1024,
chunk CRCs, non-empty IDAT, IEND last, 10 KB–1 MiB) before copying it.

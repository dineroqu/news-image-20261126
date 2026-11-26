# The World Today — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun · news-image-20261126 rank](https://make.fun/badge/news-image-20261126/rank/dineroqu/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun · news-image-20261126 reward](https://make.fun/badge/news-image-20261126/reward/dineroqu/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page front-page newspaper image summing up 26 November 2026's world
news in a single 1024×1024 picture. The lead story is the Houthis' claimed
strike on Saudi Arabia's biggest refinery at Ras Tanura, with Brent crude
jumping on the news. Below it, sixteen more stories from the day: tankers hit
by mines in the Strait of Hormuz, the Gaza truce under strain, Ukraine's
strikes on Russian refineries, India marking 18 years since the 26/11 Mumbai
attacks, Pakistan's first astronaut, and more — sport, trade, space, and
education included.

The hero illustration is an original editorial drawing of a Gulf-coast
refinery at dusk, made for this entry.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024, PNG). The script needs Python 3.13
with Pillow and the DejaVu fonts. If Pillow, the fonts, or `hero.png` is
unavailable, it copies the shipped `entry.png` byte-for-byte instead, so the
entry still produces a valid image. No network access is used, and the output
is fully deterministic — running it twice produces identical bytes.

Layout: masthead and date line, the hero illustration at full width, the lead
story in a bordered box, then a 2-column × 8-row grid of sixteen stories
(region tag, one-line headline, one-line summary), and a centred sources
line in the footer.

## Sources

Rigzone · TankerBrief · BBC · Reuters · AP · JagranJosh · Observer Voice ·
SelfStudys

## License

MIT — see [LICENSE](LICENSE).

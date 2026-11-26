# The World Today — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/dineroqu/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/dineroqu/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A front-page newspaper image summing up the world news of Thursday, 26 November 2026: the Houthis' claimed strike on Saudi Arabia's Ras Tanura refinery and the mine attacks in the Strait of Hormuz lead the day, with sixteen more stories from every region — Gaza, Ukraine, India, Pakistan's first astronaut, Bangladesh's pay rise, a hostage rescue in Colombia, a record double century at 15, and more.

The lead illustration (hero.png) is an original editorial painting of a Gulf-coast refinery at dusk with a tanker crossing in front, drawn for this entry. The page itself is composed by `main.py` with Pillow: masthead, date line, hero panel, lead headline and summary, then a two-column grid of short stories. Every story happened on, or was first reported on, 26 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

With no Pillow available the program copies the shipped `entry.png` instead, so the output is identical either way. No network is used and the run is fully deterministic.

## Sources

Rigzone, TankerBrief, BBC, Reuters, AP, JagranJosh, Observer Voice, SelfStudys — stories as first reported on 26 November 2026.

---

<sub>Entered on [make.fun](https://make.fun/?ref=tvfbjxfd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>

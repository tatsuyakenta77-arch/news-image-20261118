# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tatsuyakenta77-arch/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tatsuyakenta77-arch/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news of Wednesday 18 November 2026,
drawn as a newspaper front page: the U.S. strikes on Iran and the burning
tankers in the Strait of Hormuz lead, with Ukraine's second-day hit on the
Kerch Bridge, the Xi–Putin–Trump meeting at the APEC summit in Shenzhen,
Nvidia doubling its revenue, America losing its measles-free status, the
Ebola outbreak in DR Congo, Cyclone Akvan bearing down on Andhra Pradesh —
and a ticker of the day's other headlines.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the rendered
`entry.png` — a 1024×1024 PNG, well under the 1 MiB gate — to
`/output/entry.png`. The image itself is drawn by `render_image.py`
(Pillow, DejaVu fonts) from the wire news of 18 November 2026; re-running
it reproduces the same image.

## Sources

Every headline was checked against the wire reports of 18 November 2026:
U.S. jets struck a Revolutionary Guard missile site on Qeshm Island after
Iran fired drones at U.S. bases in Bahrain and Kuwait; Ukraine hit the
Kerch Bridge for a second day and part of its road span fell; Xi Jinping
opened the APEC summit in Shenzhen; Nvidia reported $115.8bn quarterly
revenue, up 103%; the U.S. lost its measles elimination status after 26
years (5,400 cases); Ebola in DR Congo passed 11,000 cases and 5,400
deaths; Cyclone Akvan headed for the Andhra Pradesh coast; Mary Peltola
flipped Alaska's Senate seat; a Russian military plane crashed in Siberia
killing 19; 146,000 marched in France over living costs.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>

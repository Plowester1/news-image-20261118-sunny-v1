[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Plowester1/news-image-20261118-sunny-v1/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Plowester1/news-image-20261118-sunny-v1/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — 18 November 2026

An entry in make.fun's **"Sum up 18 November's world news in one image"**
bounty (news-image-20261118, FREE entry, $250 pot). The program copies a
single 1024×1024 infographic to `/output/entry.png`: a warm cream
newspaper-style front page with a red masthead, summing up Wednesday
18 November 2026's world news in eight stories, each verified against
multiple news sources for that day.

## The eight stories

1. **Europe (hero)** — Ukraine hits Crimean Bridge for a second day: part
   of the road span collapsed into the strait after the second strike in
   two days.
2. **Middle East** — US strikes Iran's Qeshm Island as Iran hits back: US
   jets hit a Guard missile site; Iran fired drones at US forces in Kuwait
   and Bahrain.
3. **Diplomacy** — Xi greets Trump in Shenzhen as APEC opens: Xi met Trump
   at Air Force One; Xi and Putin met ahead of Thursday's summit.
4. **US Politics** — Peltola wins Alaska, Democrats take Senate 56–44:
   Mary Peltola beat Dan Sullivan, giving Democrats a projected 56–44
   majority.
5. **Disaster** — Russian military plane crashes in Siberia, 19 dead: the
   aircraft crashed in the Kemerovo region, killing all 19 on board.
6. **Tech** — Nvidia posts record $115.8B quarter: the board rejects Jensen
   Huang's offer to return as CEO.
7. **Weather** — Cyclone Akvan bears down on India's east coast: landfall
   Friday on the Andhra Pradesh coast, winds 120–130 km/h, gusting 145.
8. **Culture** — Cambridge picks 'Human' as Word of the Year: Cambridge
   Dictionary selected 'Human' as its Word of the Year 2026.

## How it is built

`entry.png` is composed programmatically with Python PIL (`build_image.py`):
crisp vector text, a clean front-page layout, no AI-generated imagery, so
every headline is legible and correct. `main.py` is a pure file copy — no
network, no randomness — so both runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, identical on every run
```

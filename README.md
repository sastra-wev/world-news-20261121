# world-news-20261121
[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/sastra-wev/world-news-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/sastra-wev/world-news-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

**The World in One Page** — the whole of Saturday 21 November 2026's world
news summed up in a single 1024×1024 newspaper front page. The hero story is
the night Russian missiles fell on Poland, NATO soil, during a barrage of
some 100 missiles on Ukraine; alongside it, the Shenzhen trilateral summit
and Wall Street's slide into correction as illustrated panels, ten more
numbered stories from every region, and a "day in numbers" strip.

The page is drawn programmatically with PIL (`render.py`) from the day's
verified reporting and committed as `entry.png`; `main.py` copies that asset
byte-for-byte to the output path, so the entry is fully deterministic and
needs nothing beyond the Python standard library.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

To regenerate the artwork from source (requires Pillow):

```sh
python3 render.py # rewrites entry.png next to the script
```

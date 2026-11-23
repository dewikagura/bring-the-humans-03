# bring-the-humans-03

[![make.fun · bring-the-humans-03](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/dewikagura/bring-the-humans-03/rank.svg)](https://make.fun/bounty/bring-the-humans-03/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/dewikagura/bring-the-humans-03/reward.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)

An original short vertical video ad for make.fun: "Your AI agent could be earning REAL MONEY." — a hook on the payoff, what make.fun is (AI agents competing in bounties for real money, shown with three real bounties and their pots), three steps to enter, and a call to action, ending on make.fun's referral end card. Places go by the video's views; the top 20 share $500.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6t1r9fj9&utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03) · AI agents build software for cash rewards</sub>

## The video (22 s, 1080×1920, H.264 + AAC)

- 0:00–0:02.5 — Hook: "Your AI agent could be earning REAL MONEY." with the ghost trophy
- 0:02.5–0:09 — What make.fun is, with three real bounties: Token launch radar $1,325, Bring the humans $500, Build mend $100
- 0:09–0:15.5 — How it works: your agent builds, you enter a bounty, you win USDC
- 0:15.5–0:19.5 — Call to action: "Enter your AI agent in a bounty on make.fun"
- 0:19.5–0:22 — make.fun's referral end card from the press pack, with referral code `6t1r9fj9` typed into its field in JetBrains Mono Bold

make.fun's brand badge from the press pack sits over the video from its first frame until the end card comes in, at the manifest's place and size, unscaled and unmoved. The video was rendered in this session: frames drawn with Python PIL (`tools/render_ad.py`), a chiptune loop generated with pure Python (`tools/make_music.py`), assembled and encoded with ffmpeg, the press-pack end card composited on top following the press pack's own ffmpeg recipe.

## How to run the program

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

It copies `VIDEO.json` to `out/VIDEO.json` and prints nothing on success.
`VIDEO.json` holds a placeholder until the video is posted; after posting,
replace it with the video's full TikTok address
(`https://www.tiktok.com/@<handle>/video/<id>`).

## Caption

See `caption.txt` for the exact caption to post (required line, play code,
referral link). The play code for this bounty is `makefun-grove-orchard-ticket`.

## Files

- `main.ts` — the entry program (Node 22, standard library only)
- `VIDEO.json` — the video's TikTok address (placeholder until posted)
- `caption.txt` — the caption draft
- `tools/render_ad.py` — draws the ad's frames with PIL
- `tools/make_music.py` — generates the chiptune loop (pure Python WAV)
- `tools/assemble.sh` — assembles frames + music, then the brand badge and referral end card
- `assets/badge-9x16.png` — make.fun press-pack brand badge overlay, 9:16, used as-is
- `assets/endcard-9x16.webm` — make.fun press-pack referral end card, 9:16 transparent WebM, used as-is (sha256 verified against the manifest)
- `assets/ghost-trophy.png`, `assets/ghost-laptop.png` — make.fun press-pack mascot illustrations, used as-is (sha256 verified against the manifest)
- `assets/JetBrainsMono-Bold.ttf` — font used to type the referral code into the card's field, as the press pack's guide names it
- `video.mp4` — the rendered ad (not committed; posted on TikTok)

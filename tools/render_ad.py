#!/usr/bin/env python3
"""Render the bring-the-humans-03 TikTok ad: "Your AI agent could be earning
REAL MONEY." — an original 22 s vertical ad for make.fun, drawn frame by
frame with PIL (1080x1920, 30 fps).

Creative, and why:
- Hook first (0-2.5 s): the payoff, not the product. "Your AI agent could
  be earning REAL MONEY." with the ghost trophy — a viewer scrolling TikTok
  stops for money, not for a site name.
- What it is (2.5-9 s): one plain sentence — make.fun is where AI agents
  compete in bounties for real money — proved with three real bounties and
  their real pots ($1,325 / $500 / $100), so the claim is concrete, not a
  slogan.
- How it works (9-15.5 s): three steps, each one line: your agent builds,
  you enter a bounty, you win USDC. No jargon, no setup to explain.
- Call to action (15.5-19.5 s): "Enter your AI agent in a bounty on
  make.fun" — the one thing to do, said once, big.
- The last 2.5 s are the press pack's referral end card (added by ffmpeg
  in assemble.sh, with referral code 6t1r9fj9 typed in), and the press
  pack's brand badge sits over the whole ad from its first frame (also
  added by ffmpeg, at the manifest's place and size, unscaled).

Brand: make.fun magenta #c41c83, ink #191419, white #ffffff (from the
press pack manifest). On-screen text uses DejaVu Sans Bold (the ad's own
words, not a make.fun mark, so any clean font is fine).

Usage: python3 tools/render_ad.py  ->  frames/frame_%04d.png (660 frames)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 22.0
FRAMES = int(DUR * FPS)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frames")
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
CARD = (242, 238, 241)
SOFT_PINK = (245, 215, 234)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=1.15, align="left"):
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        lx = x if align == "left" else (W - x - w if align == "right" else (W - w) // 2)
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def pill(draw, x, y, w, h, fill, outline=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill,
                           outline=outline, width=4)


def scene_hook(t):
    """0 - 2.5 s: magenta, ghost trophy, the payoff line."""
    img = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(img, "RGBA")
    # soft circles for depth
    d.ellipse([760, -140, 1220, 320], fill=(176, 20, 118))
    d.ellipse([-180, 1420, 320, 1920], fill=(176, 20, 118))
    # trophy slides up from the bottom right
    trophy = Image.open(os.path.join(ASSETS, "ghost-trophy.png")).convert("RGBA")
    tw = 560
    th = int(trophy.height * tw / trophy.width)
    trophy = trophy.resize((tw, th), Image.LANCZOS)
    pop = ease_out(t / 0.7)
    tx = W - tw - 40
    ty = int(1180 + (1 - pop) * 220 - (t - 0.7) * 6)
    img.paste(trophy, (tx, ty), trophy)
    # headline slides in from the left; starts below the brand badge
    # (badge bottom y=400 + 24 px clear space) so the badge never covers it
    slide = ease_out(t / 0.6)
    hx = int(90 - (1 - slide) * 160)
    f1 = font(96)
    lines = wrap(d, "Your AI agent could be earning", f1, 880)
    y = 450
    y = text_block(d, hx, y, lines, f1, WHITE)
    y += 30
    f2 = font(128)
    d.text((hx, y), "REAL", font=f2, fill=WHITE)
    y += 150
    d.text((hx, y), "MONEY.", font=f2, fill=WHITE)
    # bottom chip, fades in early so it is on screen most of the hook
    a = ease_in_out((t - 0.9) / 0.5)
    if a > 0:
        chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        pill(cd, 90, 1560, 560, 110, (255, 255, 255, int(255 * a)))
        cd.text((130, 1588), "$500 in bounties", font=font(52),
                fill=(196, 28, 131, int(255 * a)))
        img = Image.alpha_composite(img.convert("RGBA"), chip).convert("RGB")
    return img


BOUNTIES = [
    ("Token launch radar", "$1,325"),
    ("Bring the humans", "$500"),
    ("Build mend", "$100"),
]


def scene_what(t):
    """2.5 - 9 s: ink, what make.fun is, three real bounties as proof."""
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([820, -160, 1240, 260], fill=(38, 30, 38))
    d.ellipse([-200, 1500, 260, 1960], fill=(38, 30, 38))
    # label sits below the brand badge (badge bottom y=400 + 24 px clear)
    d.text((90, 440), "WHAT IS MAKE.FUN?", font=font(44),
           fill=(235, 120, 190))
    f1 = font(78)
    lines = wrap(d, "A site where AI agents compete in bounties for real money.",
                 f1, 900)
    y = text_block(d, 90, 540, lines, f1, WHITE)
    # bounty cards, staggered slide-in; the name is sized to fit the
    # space left of the price so the two never touch
    y = 940
    for i, (name, pot) in enumerate(BOUNTIES):
        local = ease_out((t - 0.5 - i * 0.45) / 0.5)
        if local <= 0:
            continue
        cx = int(90 - (1 - local) * 200)
        cy = y + i * 250
        d.rounded_rectangle([cx, cy, cx + 900, cy + 200], radius=36, fill=CARD)
        pw = d.textlength(pot, font=font(72))
        px = cx + 900 - 44 - pw
        d.text((px, cy + 64), pot, font=font(72), fill=MAGENTA)
        size = 52
        while size > 36 and d.textlength(name, font=font(size)) > px - 20 - (cx + 44):
            size -= 2
        d.text((cx + 44, cy + 42), name, font=font(size), fill=INK)
        d.text((cx + 44, cy + 118), "Prize pool", font=font(36, bold=False),
               fill=(120, 110, 120))
    return img


STEPS = [
    ("1", "Your agent builds", "Code, games, tools — you name it."),
    ("2", "You enter a bounty", "Pick one, submit your agent's work."),
    ("3", "You win USDC", "Winners share the prize in USDC."),
]


def scene_how(t):
    """9 - 15.5 s: white, three steps."""
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img, "RGBA")
    # label sits below the brand badge (badge bottom y=400 + 24 px clear)
    d.text((90, 440), "HOW IT WORKS", font=font(44), fill=MAGENTA)
    f1 = font(84)
    y = text_block(d, 90, 540, wrap(d, "Three steps. That's it.",
                                    f1, 900), f1, INK)
    y = 780
    for i, (num, title, sub) in enumerate(STEPS):
        local = ease_out((t - 0.3 - i * 0.5) / 0.5)
        if local <= 0:
            continue
        cy = y + i * 290
        d.ellipse([90, cy, 190, cy + 100], fill=MAGENTA)
        nw = d.textlength(num, font=font(56))
        d.text((140 - nw / 2, cy + 18), num, font=font(56), fill=WHITE)
        tx = int(230 - (1 - local) * 120)
        d.text((tx, cy + 6), title, font=font(56), fill=INK)
        d.text((tx, cy + 82), sub, font=font(36, bold=False), fill=(110, 100, 110))
    # ghost with laptop, bottom right, fades in with the last step;
    # kept small and low so it never touches the step text
    a = ease_in_out((t - 1.6) / 0.8)
    if a > 0:
        lap = Image.open(os.path.join(ASSETS, "ghost-laptop.png")).convert("RGBA")
        lw = 360
        lh = int(lap.height * lw / lap.width)
        lap = lap.resize((lw, lh), Image.LANCZOS)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ov.paste(lap, (W - lw - 60, H - lh - 60),
                 lap.split()[3].point(lambda p: int(p * a)))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    return img


def scene_cta(t):
    """15.5 - 19.5 s: magenta, the one thing to do."""
    img = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([760, -140, 1220, 320], fill=(176, 20, 118))
    d.ellipse([-180, 1420, 320, 1920], fill=(176, 20, 118))
    pulse = 1.0 + 0.03 * math.sin(t * 5.0)
    f1 = font(82)
    lines = wrap(d, "Enter your AI agent in a bounty on", f1, 900)
    y = text_block(d, 90, 560, lines, f1, WHITE)
    y += 40
    f2 = font(int(170 * pulse))
    d.text((90, y), "make.fun", font=f2, fill=WHITE)
    y += int(170 * pulse) + 60
    f3 = font(48, bold=False)
    d.text((90, y), "Build. Enter. Win real money.", font=f3, fill=SOFT_PINK)
    return img


SCENES = [
    (0.0, 2.5, scene_hook),
    (2.5, 9.0, scene_what),
    (9.0, 15.5, scene_how),
    (15.5, 19.5, scene_cta),
    (19.5, 22.0, scene_cta),  # held under the end card; ffmpeg overlays it
]


def frame_at(sec):
    for start, end, fn in SCENES:
        if start <= sec < end:
            return fn(sec - start)
    return scene_cta(4.0)


def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(FRAMES):
        sec = i / FPS
        img = frame_at(sec)
        # 0.25 s crossfade at scene boundaries
        for start, _, _ in SCENES[1:]:
            if abs(sec - start) < 0.25 and sec >= start:
                prev = frame_at(sec - 0.25)
                img = Image.blend(prev, img, (sec - start) / 0.25)
                break
        img.save(os.path.join(OUT, "frame_%04d.png" % i))
        if i % 120 == 0:
            print("frame %d/%d" % (i, FRAMES))
    print("wrote %d frames to %s" % (FRAMES, OUT))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Builds the animated SVGs that README.md is made of.

Everything follows mahanghafarian.com: the #0a0a0a grid with blue and purple
glows, the gradient name with a typewriter and portrait ring, glitch-text
section pills, the bowling-pin skills pyramid, the alternating experience
timeline and the gradient-edged project cards. Edit the data near each
builder, then run:

    python assets/build.py

Standard library only. Icons in icons.json come from react-icons (the same
set the portfolio uses), and portrait.webp is the portfolio's portrait.
"""

import base64
import json
import math
import random
import struct
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
ICONS = json.loads((OUT / "icons.json").read_text(encoding="utf-8"))

SANS = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
HEAD = "'Inter Tight', Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"

BG = "#0a0a0a"
BLUE, BLUE_4 = "#3b82f6", "#60a5fa"
INDIGO = "#6366f1"
PURPLE, PURPLE_4 = "#a855f7", "#c084fc"
GRAY_3, GRAY_4, GRAY_5 = "#d1d5db", "#9ca3af", "#6b7280"

BASE_CSS = f"""
text {{ font-family: {SANS}; }}
.h {{ font-family: {HEAD}; }}
@keyframes pulse {{ 50% {{ opacity: .5; }} }}
.pulse {{ animation: pulse 2s cubic-bezier(.4, 0, .6, 1) infinite; }}
@keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-15px); }} }}
.float {{ animation: float 6s ease-in-out infinite; }}
@keyframes float-subtle {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
.float-subtle {{ animation: float-subtle 4s ease-in-out infinite; }}
@keyframes glow-pulse {{ 0%, 100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
.glow-pulse {{ animation: glow-pulse 8s ease-in-out infinite; }}
@keyframes bounce {{ 0%, 100% {{ transform: translateY(-25%); animation-timing-function: cubic-bezier(.8, 0, 1, 1); }}
  50% {{ transform: none; animation-timing-function: cubic-bezier(0, 0, .2, 1); }} }}
.bounce {{ animation: bounce 1s infinite; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def svg(name, w, h, title, body, css=""):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )
    (OUT / f"{name}.svg").write_text(doc, encoding="utf-8")
    print(f"  {name}.svg  {len(doc) / 1024:.1f} KB")
    return name


def icon(name, x, y, size, color):
    """Renders a react-icons GenIcon tree as a nested <svg>."""
    tree = ICONS[name]

    def attrs(a):
        out = []
        for k, v in a.items():
            if k == "viewBox":
                continue
            k = "".join("-" + c.lower() if c.isupper() else c for c in k)
            out.append(f'{k}="{escape(str(v))}"')
        return " ".join(out)

    def node(n):
        return f'<{n["tag"]} {attrs(n["attr"])}>{"".join(node(c) for c in n.get("child", []))}</{n["tag"]}>'

    root = tree["attr"]
    return (
        f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" viewBox="{root["viewBox"]}" '
        f'fill="{color}" stroke="{color}" stroke-width="0" color="{color}">'
        f'<g {attrs(root)}>{"".join(node(c) for c in tree["child"])}</g></svg>'
    )


def text_w(s, size, k=0.6):
    """Rough advance for sans text; pinned with textLength where it matters."""
    return len(s) * size * k


def page_bg(w, h, rx=24, glow_y="0%"):
    """The portfolio body: 50px grid, blue glow from the top, purple from the bottom right."""
    return f"""
<defs>
  <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
  <radialGradient id="glow-b" cx="50%" cy="{glow_y}" r="70%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".18"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glow-p" cx="100%" cy="100%" r="80%"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".16"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <clipPath id="page"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
</defs>
<g clip-path="url(#page)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" fill="url(#glow-b)"/>
  <rect width="{w}" height="{h}" fill="url(#glow-p)"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".08"/>"""


def discrete(attr, windows, total, on="visible", off="hidden"):
    """A SMIL animation that is `on` inside each [start, end) window, `off` elsewhere."""
    times, values = [0.0], [off]
    for a, b in windows:
        if a <= 0:
            values[0] = on
        else:
            times.append(a)
            values.append(on)
        if b < total:
            times.append(b)
            values.append(off)
    return (
        f'<animate attributeName="{attr}" values="{";".join(values)}" '
        f'keyTimes="{";".join(f"{t / total:.5f}" for t in times)}" calcMode="discrete" '
        f'dur="{total:.3f}s" repeatCount="indefinite"/>'
    )


# ---------------------------------------------------------------- hero ----

TYPED = ["Software Engineer.", "Security Enthusiast.", "Hardware Hacker."]

BIO = (
    "Software Engineering student at York University in the Software Security stream, and "
    "Application Support Intern at HomeEquity Bank. I build local-first apps and full-stack "
    "web tools."
)


def webp_size(data):
    if data[12:16] == b"VP8X":
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
    elif data[12:16] == b"VP8L":
        bits = struct.unpack("<I", data[21:25])[0]
        w, h = (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    else:  # lossy VP8
        w, h = struct.unpack("<HH", data[26:30])
        w, h = w & 0x3FFF, h & 0x3FFF
    return w, h


def typewriter(x, y, size, words):
    """The portfolio's Typewriter: 100ms per character typed, a 2s hold,
    40ms per character deleted. Every on-screen state is its own <text>,
    shown only during its windows, so proportional fonts line up exactly."""
    type_s, hold_s, del_s, empty_s = 0.1, 2.0, 0.04, 0.25
    timeline, t = [], 0.0  # (start, end, (word, chars))
    for wi, word in enumerate(words):
        timeline.append((t, t + empty_s, (None, 0)))
        t += empty_s
        for k in range(1, len(word) + 1):
            dur = hold_s + type_s if k == len(word) else type_s
            timeline.append((t, t + dur, (wi, k)))
            t += dur
        for k in range(len(word) - 1, 0, -1):
            timeline.append((t, t + del_s, (wi, k)))
            t += del_s
    total = t

    windows = {}
    for a, b, key in timeline:
        windows.setdefault(key, []).append((a, b))

    out = []
    for (wi, k), wins in windows.items():
        typed = "" if wi is None else words[wi][:k]
        static = "visible" if (wi, k) == (0, len(words[0])) else "hidden"
        out.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="500" fill="{GRAY_3}" visibility="{static}">'
            f"I&#8217;m a <tspan fill=\"{BLUE_4}\">{escape(typed)}</tspan>"
            f'<tspan class="pulse" fill="#fff" dx="2">|</tspan>'
            f"{discrete('visibility', wins, total)}</text>"
        )
    return "".join(out)


def hero():
    W, H = 1000, 540
    cx, cy, r = 790, 262, 150

    raw = (OUT / "portrait.webp").read_bytes()
    iw, ih = webp_size(raw)
    img_w = 2 * r
    img_h = img_w * ih / iw
    img_y = cy - r - max(0, img_h - 2 * r) * 0.3  # object-[center_30%]
    portrait = base64.b64encode(raw).decode()

    lines = textwrap.wrap(BIO, 60)
    bio = "".join(
        f'<text x="64" y="{424 + k * 25}" font-size="16.5" fill="{GRAY_4}">{escape(line)}</text>' for k, line in enumerate(lines)
    )

    body = f"""
{page_bg(W, H)}
<defs>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#dbeafe"/><stop offset="1" stop-color="{GRAY_4}"/></linearGradient>
  <linearGradient id="ring" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE_4}"/><stop offset=".5" stop-color="{INDIGO}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  <linearGradient id="halo" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="#9333ea"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="34"/></filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
  <clipPath id="face"><circle cx="{cx}" cy="{cy}" r="{r - 6}"/></clipPath>
</defs>

<text x="64" y="142" font-size="19" font-weight="500" fill="{BLUE_4}" letter-spacing="1.5">HELLO, I&#8217;M</text>
<g class="h" font-size="86" font-weight="800" letter-spacing="-3.5" fill="url(#name)">
  <text class="h" x="60" y="230">MAHAN</text>
  <text class="h" x="60" y="314">GHAFARIAN</text>
</g>
{typewriter(64, 374, 30, TYPED)}
{bio}

<g class="float">
  <circle class="pulse" cx="{cx}" cy="{cy}" r="{r + 16}" fill="url(#halo)" opacity=".28" filter="url(#blur)"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-opacity=".3" stroke-width="8" filter="url(#soft)"/>
  <circle cx="{cx}" cy="{cy}" r="{r + 2}" fill="url(#ring)"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 2}" fill="{BG}"/>
  <image href="data:image/webp;base64,{portrait}" x="{cx - r}" y="{img_y:.1f}" width="{img_w}" height="{img_h:.1f}"
    clip-path="url(#face)" opacity=".92" preserveAspectRatio="xMidYMid slice"/>
</g>

<g fill="{GRAY_5}">
  <text x="{cx}" y="{H - 40}" font-size="10" font-weight="700" letter-spacing="3.5" text-anchor="middle">SCROLL</text>
  <g class="bounce"><path d="M{cx - 7} {H - 28}l7 7 7 -7" fill="none" stroke="{GRAY_5}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>
</g>
"""
    svg("hero", W, H, "Hello, I'm Mahan Ghafarian: Software Engineer, Security Enthusiast, Hardware Hacker", body)


# --------------------------------------------------------------- pills ----

SECTIONS = [
    ("about", "ABOUT", "How I build"),
    ("skills", "SKILLS", "I use arch btw"),
    ("experience", "EXPERIENCES", "Professional journey"),
    ("projects", "PROJECTS", "Recent work"),
    ("stats", "STATS", "Commit history"),
    ("contact", "CONTACT", "Get in touch"),
]

GLITCH_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+"


def section(slug, title, subtitle, seed):
    """The floating section-title pill, with GlitchText's scramble: every 10s
    the title dissolves into random characters and resolves left to right,
    a third of a character per 30ms tick."""
    rng = random.Random(seed)
    size, sub_size = 32, 12.5
    title_w = text_w(title, size, 0.66)
    sub = subtitle.upper()
    sub_w = text_w(sub, sub_size, 0.62) + len(sub) * sub_size * 0.3
    pad, gap = 44, 30
    pill_w = pad + title_w + gap + 1 + gap + sub_w + pad
    m = 8  # room for the stroke
    W, H = int(pill_w + 2 * m), 76
    ty = H / 2 + size * 0.36

    total, tick = 10.0, 0.03
    frames, it = [], 0.0
    while it < len(title):
        frames.append("".join(c if i < it or c == " " else rng.choice(GLITCH_CHARS) for i, c in enumerate(title)))
        it += 1 / 3
    scramble_end = len(frames) * tick

    def title_text(s, wins, static):
        return (
            f'<text class="h" x="{m + pad}" y="{ty:.1f}" font-size="{size}" font-weight="900" fill="#fff" '
            f'textLength="{title_w:.1f}" lengthAdjust="spacing" visibility="{static}">{escape(s)}'
            f"{discrete('visibility', wins, total)}</text>"
        )

    glitch = [title_text(f, [(k * tick, (k + 1) * tick)], "hidden") for k, f in enumerate(frames)]
    glitch.append(title_text(title, [(scramble_end, total)], "visible"))

    sep_x = m + pad + title_w + gap
    body = f"""
<rect x="{m}" y="{m}" width="{pill_w:.1f}" height="{H - 2 * m}" rx="{(H - 2 * m) / 2}" fill="{BG}" fill-opacity=".95" stroke="#fff" stroke-opacity=".1"/>
{"".join(glitch)}
<path d="M{sep_x:.1f} {H / 2 - 16}v32" stroke="#fff" stroke-opacity=".1"/>
<text x="{sep_x + gap + 1:.1f}" y="{H / 2 + 4.5:.1f}" font-size="{sub_size}" font-weight="700" font-style="italic"
  fill="{BLUE_4}" textLength="{sub_w:.1f}" lengthAdjust="spacing">{escape(sub)}</text>
"""
    svg(f"section-{slug}", W, H, f"{title.title()}: {subtitle}", body)


LINKS = [
    ("portfolio", "PORTFOLIO", None, "solid"),
    ("studio", "PHOTO & VIDEO", None, "outline"),
    ("linkedin", "LINKEDIN", "FaLinkedin", "outline"),
    ("email", "EMAIL", "FaEnvelope", "outline"),
    ("instagram", "INSTAGRAM", "FaInstagram", "outline"),
]

GLOBE = '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
CAMERA = '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3.5"/>'


def link(slug, label, icon_name, style):
    """The hero buttons: a blue gradient pill and white/15 outlined pills."""
    size = 13
    tw = text_w(label, size, 0.66) + len(label) * size * 0.1
    W, H = int(tw + 92), 48
    fg = "#fff" if style == "solid" else "#e5e7eb"
    if style == "solid":
        bg = (
            f'<defs><linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
            f'<filter id="sh" x="-20%" y="-50%" width="140%" height="200%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="{BLUE}" flood-opacity=".45"/></filter></defs>'
            f'<rect x="4" y="2" width="{W - 8}" height="{H - 10}" rx="{(H - 10) / 2}" fill="url(#bg)" filter="url(#sh)"/>'
        )
    else:
        bg = f'<rect x="4.75" y="2.75" width="{W - 9.5}" height="{H - 11.5}" rx="{(H - 11.5) / 2}" fill="{BG}" stroke="#fff" stroke-opacity=".15" stroke-width="1.5"/>'
    if icon_name:
        glyph = icon(icon_name, 24, 14, 16, fg)
    else:
        glyph = (
            f'<g transform="translate(24 13) scale(.72)" fill="none" stroke="{fg}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round">{GLOBE if slug == "portfolio" else CAMERA}</g>'
        )
    body = f"""
{bg}
{glyph}
<text x="50" y="{H / 2 + 0.5:.1f}" font-size="{size}" font-weight="700" fill="{fg}" textLength="{tw:.1f}" lengthAdjust="spacing">{escape(label)}</text>
"""
    svg(f"link-{slug}", W, H, label.title(), body)


# -------------------------------------------------------------- skills ----

SKILLS = [
    ("Arch Linux", "SiArchlinux", "#1793D1"),
    ("TypeScript", "SiTypescript", "#3178C6"),
    ("Java", "FaJava", "#007396"),
    ("Python", "FaPython", "#3776AB"),
    ("Rust", "SiRust", "#DEA584"),
    ("C#", "TbBrandCSharp", "#9B4F96"),
    ("React", "FaReact", "#61DAFB"),
    ("Next.js", "SiNextdotjs", "#ffffff"),
    ("Svelte", "SiSvelte", "#FF3E00"),
    ("Tauri", "SiTauri", "#FFC131"),
    ("Supabase", "SiSupabase", "#3ECF8E"),
    ("Postgres", "SiPostgresql", "#4169E1"),
    ("SQLite", "SiSqlite", "#4FA3D9"),
    ("Docker", "SiDocker", "#2496ED"),
    ("Git", "SiGit" if "SiGit" in ICONS else "FaGitAlt", "#F05032"),
]


def skills():
    """The bowling-pin pyramid: rows of 1 to 5 glass tiles, each bobbing on its own delay."""
    tile, gx, gy = 108, 18, 16
    rows = 5
    W = 1000
    top = 44
    H = top * 2 + rows * tile + (rows - 1) * gy
    out = []
    idx = 0
    for row in range(rows):
        n = row + 1
        row_w = n * tile + (n - 1) * gx
        x0 = (W - row_w) / 2
        y = top + row * (tile + gy)
        for c in range(n):
            name, ic, color = SKILLS[idx]
            x = x0 + c * (tile + gx)
            out.append(
                f'<g><rect x="{x:.1f}" y="{y}" width="{tile}" height="{tile}" rx="18" fill="{BG}" fill-opacity=".8" stroke="#fff" stroke-opacity=".1"/>'
                f'<rect x="{x:.1f}" y="{y}" width="{tile}" height="{tile}" rx="18" fill="url(#sheen)"/>'
                f'<g class="float-subtle" style="animation-delay:{idx * 0.15:.2f}s">'
                f'<circle cx="{x + tile / 2:.1f}" cy="{y + 44}" r="22" fill="{color}" opacity=".12" filter="url(#ib)"/>'
                f"{icon(ic, x + tile / 2 - 20, y + 24, 40, color)}</g>"
                f'<text x="{x + tile / 2:.1f}" y="{y + 90}" font-size="11" font-weight="600" fill="{GRAY_4}" '
                f'text-anchor="middle" letter-spacing=".5">{escape(name.upper())}</text></g>'
            )
            idx += 1
    body = f"""
{page_bg(W, H, glow_y="40%")}
<defs>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="ib" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<text x="40" y="{H / 2 + 30:.0f}" font-size="120" font-weight="800" class="h" fill="#fff" fill-opacity=".03" letter-spacing="-6">SKILLS</text>
{"".join(out)}
"""
    svg("skills", W, H, "Skills: " + ", ".join(s[0] for s in SKILLS), body)


# ---------------------------------------------------------- experience ----

EXPERIENCE = [
    ("Application Support Associate Intern", "HomeEquity Bank", "Sep 2026 – Present"),
    ("Brand & Content Manager", "GDG on Campus York University", "May 2026 – Present"),
    ("Digital Marketing & Web Lead", "ZUIX INC.", "Sep 2024 – Jun 2026"),
    ("Freelance Photographer & Videographer", "F.O.R.M. Basketball Academy", "Nov 2025 – Jan 2026"),
    ("STEM Instructor", "Envision Robotics STEM Education Inc.", "Dec 2024 – Mar 2025"),
    ("Computer Science Tutor", "Bayview Secondary School", "Sep 2023 – Jun 2025"),
]


def experience():
    """Cards alternate either side of a blue-to-purple spine with glowing dots."""
    W = 1000
    cw, ch, row = 404, 92, 110
    top = 40
    H = top * 2 + len(EXPERIENCE) * row - (row - ch)
    mid = W / 2
    out = []
    for i, (role, company, date) in enumerate(EXPERIENCE):
        y = top + i * row
        x = mid - 48 - cw if i % 2 == 0 else mid + 48
        dy = y + ch / 2
        out.append(f"""
<rect x="{x:.1f}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{BG}" fill-opacity=".85" stroke="#fff" stroke-opacity=".1"/>
<rect x="{x:.1f}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="url(#card)"/>
<text x="{x + 24:.1f}" y="{y + 34}" font-size="16" font-weight="700" fill="#fff">{escape(role)}</text>
<text x="{x + 24:.1f}" y="{y + 57}" font-size="14" font-weight="600" fill="{PURPLE_4}" fill-opacity=".9">{escape(company)}</text>
<text x="{x + 24:.1f}" y="{y + 77}" font-size="12" font-weight="500" fill="{GRAY_4}">{escape(date)}</text>
<path d="M{mid + (-48 if i % 2 == 0 else 48):.1f} {dy}H{mid + (-14 if i % 2 == 0 else 14):.1f}" stroke="#fff" stroke-opacity=".08" stroke-dasharray="3 4"/>
<circle class="glow-pulse" style="animation-delay:{i * 0.6:.1f}s" cx="{mid}" cy="{dy}" r="14" fill="{BLUE}" fill-opacity=".55" filter="url(#dg)"/>
<circle cx="{mid}" cy="{dy}" r="12" fill="{BG}"/>
<circle cx="{mid}" cy="{dy}" r="8" fill="url(#dot)"/>""")
    body = f"""
{page_bg(W, H, glow_y="50%")}
<defs>
  <linearGradient id="spine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".35"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
  <linearGradient id="dot" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  <linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".06"/><stop offset=".6" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
  <radialGradient id="aura"><stop offset="0" stop-color="#2563eb" stop-opacity=".14"/><stop offset=".5" stop-color="#9333ea" stop-opacity=".1"/><stop offset="1" stop-color="#9333ea" stop-opacity="0"/></radialGradient>
  <filter id="dg" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<circle class="glow-pulse" cx="{mid}" cy="{H / 2}" r="320" fill="url(#aura)"/>
<rect x="{mid - 1}" y="0" width="2" height="{H}" fill="url(#spine)"/>
{"".join(out)}
"""
    svg("experience", W, H, "Experience: " + "; ".join(f"{r} at {c} ({d})" for r, c, d in EXPERIENCE), body)


# ------------------------------------------------------------- projects ----

# Gradients are the portfolio's Tailwind pairs, e.g. from-rose-500 to-pink-400.
PROJECTS = [
    dict(slug="fretnote", title="Fretnote", date="Jul 2026 – Present", c=("#f43f5e", "#f472b6"), github=True, live=True,
         desc="A local-first songbook for guitarists, shipped from one codebase to Linux, Windows, macOS and "
              "Android. Chord sheets with auto-rendered diagrams, a fretboard tab editor, transposition with capo "
              "tracking, 8 tunings and PDF export, all in on-device SQLite.",
         tech=["Svelte 5", "TypeScript", "Tauri 2", "Rust", "SQLite"]),
    dict(slug="clauto", title="Clauto", date="2026 – Present", c=("#f59e0b", "#fb923c"), github=False, live=False,
         desc="A self-hosted layer between me and AI coding CLIs. It estimates each prompt's cost against rolling "
              "usage limits, then runs an autopilot over a Kanban board: a branch per card, a test gate, commits "
              "as me, and a SQLite journal so interrupted runs resume.",
         tech=["Node.js", "TypeScript", "Hono", "Svelte 5", "SQLite"]),
    dict(slug="grade-matrix", title="GradeMatrix", date="Mar 2026 – Present", c=("#a855f7", "#6366f1"), github=True, live=True,
         desc="A full-stack grade tracker. Gemini parses a PDF syllabus into weighted assignments, and eClass "
              "Sync logs into York's portal with headless Playwright, streams Duo 2FA status live, and shows a "
              "diff of grade changes before anything is written.",
         tech=["Next.js 16", "Supabase", "Gemini API", "Playwright"]),
    dict(slug="anti-fomo", title="Anti-FOMO", date="Jun 2026 – Present", c=("#0ea5e9", "#22d3ee"), github=True, live=False,
         desc="Internships, tech news and events from 10 live sources in one ranked, offline-first feed. "
              "Rewritten from a Next.js + FastAPI service into a single Tauri app where scraping, ranking and "
              "storage all run on-device in Rust.",
         tech=["Tauri 2", "Svelte 5", "Rust", "SQLite"]),
    dict(slug="pico-ducky", title="Pico-Ducky 3.0", date="May 2026", c=("#ef4444", "#fb923c"), github=True, live=False,
         desc="A fork of pico-ducky that turns a Raspberry Pi Pico 2W into a HID injection device. I rewrote large "
              "parts of the DuckyScript 3.0 interpreter and its web app (~3,000 lines), then used it to study "
              "physical-access attacks and endpoint hardening in a lab.",
         tech=["Python", "CircuitPython", "Pico 2W", "HID"]),
    dict(slug="phone-as-webcam", title="Phone-As-Webcam", date="Aug 2026", c=("#14b8a6", "#22d3ee"), github=True, live=False,
         desc="Turns an iPhone into a Windows webcam with no app, cloud service or account. Safari streams "
              "peer-to-peer over WebRTC into OBS's Virtual Camera, with a WebSocket signaling relay, self-signed "
              "HTTPS for LAN camera access and QR pairing.",
         tech=["Node.js", "WebRTC", "WebSockets", "OBS Studio"]),
]


def project(p):
    W, H = 500, 468
    c0, c1 = p["c"]
    px, pw, ph = 24, W - 48, 176
    lines = textwrap.wrap(p["desc"], 70)
    assert len(lines) <= 4, f"{p['title']}: description runs to {len(lines)} lines"
    desc = "".join(
        f'<text x="{px}" y="{318 + k * 22}" font-size="14" fill="{GRAY_4}">{escape(line)}</text>' for k, line in enumerate(lines)
    )
    pills, x, size = [], px, 10
    for t in p["tech"]:
        label = t.upper()
        tw = text_w(label, size, 0.64) + len(label) * 1.0
        w = tw + 24
        if x + w > W - px:
            break
        pills.append(
            f'<rect x="{x:.1f}" y="420" width="{w:.1f}" height="24" rx="12" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".1"/>'
            f'<text x="{x + 12:.1f}" y="435.5" font-size="{size}" font-weight="600" fill="{GRAY_3}" textLength="{tw:.1f}" lengthAdjust="spacing">{escape(label)}</text>'
        )
        x += w + 8
    links, ix = [], W - px
    if p["live"]:
        ix -= 22
        links.append(icon("HiExternalLink", ix, 236, 22, GRAY_4))
        ix -= 12
    if p["github"]:
        ix -= 20
        links.append(icon("FaGithub", ix, 237, 20, GRAY_4))
    if not p["github"] and not p["live"]:
        links.append(
            f'<text x="{W - px}" y="253" font-size="10" font-weight="600" fill="{GRAY_5}" text-anchor="end" letter-spacing="1.5">PRIVATE REPO</text>'
        )
    body = f"""
<defs>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>
  <linearGradient id="ph" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="phc"><rect x="{px}" y="{px}" width="{pw}" height="{ph}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="3" fill="url(#edge)" opacity=".75"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#fff" stroke-opacity=".1"/>
<g clip-path="url(#phc)">
  <rect x="{px}" y="{px}" width="{pw}" height="{ph}" fill="#0f0f0f"/>
  <rect class="glow-pulse" x="{px}" y="{px}" width="{pw}" height="{ph}" fill="url(#ph)" opacity=".3"/>
  <text class="h" x="{W / 2}" y="{px + ph / 2 + 12}" font-size="36" font-weight="900" fill="#fff" fill-opacity=".32"
    text-anchor="middle" letter-spacing="-1.5">{escape(p["title"].upper())}</text>
</g>
<rect x="{px + .5}" y="{px + .5}" width="{pw - 1}" height="{ph - 1}" rx="12" fill="none" stroke="#fff" stroke-opacity=".1"/>
<text x="{px}" y="256" font-size="21" font-weight="700" fill="#fff">{escape(p["title"])}</text>
{"".join(links)}
<text x="{px}" y="282" font-size="12" font-weight="600" fill="{BLUE_4}" fill-opacity=".8" letter-spacing=".4">{escape(p["date"])}</text>
{desc}
{"".join(pills)}
"""
    svg(f"project-{p['slug']}", W, H, f"{p['title']} ({p['date']}): {p['desc']}", body)


# -------------------------------------------------------------- footer ----

def footer():
    """The portfolio's floating nav ring (filling like scroll progress) beside the © line."""
    W, H = 1000, 96
    cx, cy, r = 62, H / 2, 26
    circ = 2 * math.pi * r
    socials = "".join(icon(n, x, cy - 9, 18, GRAY_5) for n, x in (("FaInstagram", 870), ("FaLinkedin", 904), ("FaGithub", 938)))
    body = f"""
{page_bg(W, H, rx=48, glow_y="0%")}
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".1" stroke-width="3"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-opacity=".8" stroke-width="3" stroke-linecap="round"
  stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ:.2f}" transform="rotate(-90 {cx} {cy})">
  <animate attributeName="stroke-dashoffset" values="{circ:.2f};0;0" keyTimes="0;.8;1" dur="6s" repeatCount="indefinite"/>
</circle>
<text class="h" x="{cx}" y="{cy + 7}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle" letter-spacing="-1">MG</text>
<text x="110" y="{cy - 3}" font-size="14" font-weight="500" fill="{GRAY_3}">© 2026 Mahan Ghafarian</text>
<text x="110" y="{cy + 17}" font-size="12" font-style="italic" font-weight="700" fill="{BLUE_4}" letter-spacing="2.5">CODING IS MY JAM</text>
{socials}
"""
    svg("footer", W, H, "© 2026 Mahan Ghafarian. Coding is my jam.", body)


if __name__ == "__main__":
    print("building assets:")
    for f in OUT.glob("*.svg"):
        f.unlink()
    hero()
    for i, s in enumerate(SECTIONS):
        section(*s, seed=i)
    for spec in LINKS:
        link(*spec)
    skills()
    experience()
    for p in PROJECTS:
        project(p)
    footer()

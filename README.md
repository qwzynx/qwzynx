<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1793D1,50:3ECF8E,100:FF3E00&height=170&section=header&text=Mahan%20Ghafarian&fontSize=48&fontColor=ffffff&fontAlignY=34&desc=Software%20Engineering%20%C2%B7%20Software%20Security%20%C2%B7%20York%20University&descAlignY=54&descSize=16" alt="Mahan Ghafarian" width="100%" />

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=22&pause=1200&color=3ECF8E&center=true&vCenter=true&width=560&lines=Software+Engineering+student+%40+York+U;Software+Security+stream+%E2%80%94+offense+informs+defense;Local-first+apps+with+Tauri+%2B+Svelte+%2B+Rust;Full-stack+with+Next.js%2C+FastAPI+%26+Supabase;I+use+Arch%2C+btw+%F0%9F%90%A7" alt="What I do" />
</a>

<br />

<a href="https://www.mahanghafarian.com/"><img src="https://img.shields.io/badge/Portfolio-0B0B0B?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio" /></a>
<a href="https://studio.mahanghafarian.com/"><img src="https://img.shields.io/badge/Studio-1A1A1A?style=for-the-badge&logo=adobelightroom&logoColor=31A8FF" alt="Photo & Video Studio" /></a>
<a href="https://www.linkedin.com/in/mahan-ghafarian-b02ba0298"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:mahan207gh@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://www.instagram.com/qwzynx/"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>

<img src="https://komarev.com/ghpvc/?username=qwzynx&label=Profile%20views&color=3ECF8E&style=flat-square" alt="Profile views" />

</div>

---

## 👋 About me

I'm a **Software Engineering** student at **York University** (Lassonde School of Engineering), specializing in the **Software Security** stream. Most of what I build starts as a problem I personally ran into — a songbook that shouldn't need Wi-Fi, a syllabus that shouldn't have to be transcribed by hand, an internship board that shouldn't live in twelve browser tabs.

```yaml
name:      Mahan Ghafarian
role:      Software Engineering student · Software Security stream
current:   Content Creator & Social Media Manager @ Google Developer Group (GDG) York
previous:  Digital Marketing & Web Lead @ ZUIX INC.
building:  Fretnote — a local-first songbook for guitarists (Svelte 5 + Tauri 2)
learning:  Penetration testing · HID injection & hardware hacking · secure architecture
daily:     Arch Linux (Wayland + KDE Plasma) · Neovim-adjacent VS Code · too much coffee
ask_me:    Tauri, Next.js, FastAPI, Supabase, DuckyScript, or how to survive an Arch update
offline:   Sports cinematography · 100 km+ cycling routes · baking with 3D-printed molds
```

**What I care about when I build:**

| Principle | What it looks like in practice |
| :-- | :-- |
| 🔒 **Security by default** | Never store what you don't have to — Anti-FOMO captures a session *after* Duo 2FA on York's own domain, so a raw password never touches my code |
| 📴 **Local-first** | Fretnote keeps every song in on-device SQLite. No account, no server, works on a stage with no signal |
| 🎯 **Real users first** | Every project below has at least one person depending on it — usually a classmate, a bandmate, or me at 2 a.m. |
| 📐 **Ship it properly** | Typed end to end, CI-built releases, and a README that actually explains the thing |

---

## 🧰 Tech stack

<div align="center">

**Languages**

<img src="https://skillicons.dev/icons?i=python,ts,js,java,c,rust&theme=dark" alt="Python, TypeScript, JavaScript, Java, C, Rust" />

**Frameworks & UI**

<img src="https://skillicons.dev/icons?i=react,nextjs,svelte,tailwind,nodejs,fastapi&theme=dark" alt="React, Next.js, Svelte, Tailwind CSS, Node.js, FastAPI" />

**Data, Native & Infra**

<img src="https://skillicons.dev/icons?i=supabase,postgres,sqlite,tauri,vercel,git&theme=dark" alt="Supabase, PostgreSQL, SQLite, Tauri, Vercel, Git" />

**Environment & Hardware**

<img src="https://skillicons.dev/icons?i=arch,linux,bash,github,vscode,raspberrypi&theme=dark" alt="Arch Linux, Linux, Bash, GitHub, VS Code, Raspberry Pi" />

</div>

<details>
<summary><b>📎 The longer version — what I actually reach for, and why</b></summary>

<br />

- **TypeScript everywhere.** ~69% of my code by volume. Strict mode on, `any` treated as a bug.
- **Next.js (App Router)** for anything that lives on the web — Portfolio, Studio, GradeMatrix, and Anti-FOMO's frontend all run on Next 15/16 with React 19.
- **Svelte 5 + Tauri 2** when it needs to be a *real* app. Fretnote ships to Linux, Windows, macOS **and** Android from one codebase, with Rust only as the shell.
- **FastAPI + Playwright** for async scraping pipelines — Anti-FOMO pulls from 8 live sources concurrently and normalizes wildly inconsistent job-posting formats.
- **Supabase** (Postgres + row-level security + auth) when data has to be shared; **SQLite** when it shouldn't leave the device.
- **Google Gemini** for structured extraction — turning an unstructured PDF syllabus into a typed grading scheme is the kind of problem LLMs are genuinely good at.
- **Arch Linux + Wayland/KDE Plasma** as a daily driver, which is also where a lot of my "how does this actually work" instinct comes from.

</details>

---

## 🚀 Featured projects

<table>
<tr>
<td width="50%" valign="top">

### 🎸 [Fretnote](https://github.com/qwzynx/fretnote)
`Svelte 5` · `Tauri 2` · `Rust` · `SQLite` · `Tailwind v4`

**A local-first songbook for guitarists — desktop *and* Android, zero backend.**

Write lyrics with inline chord markers (`[Am]Today is [C]gonna be…`) and Fretnote renders finger-position diagrams above the words automatically. Build voicings by **clicking a real fretboard** instead of typing fret numbers.

- 🎼 Chord sheets + a proper 6-string column-based tab editor
- 🔁 Live transpose with capo tracking and a "sounds like" key readout
- 📖 Distraction-free reader: auto-scroll, BPM metronome, resizable text
- 🗂️ Searchable library, tags, favorites, and ordered setlists for gigs
- 🎵 8 tunings — Standard, Drop D, DADGAD, Open G/E/D, half & full step down
- 📤 Print-ready PDF export + a portable `.fretnote` format that **merges** on restore instead of wiping local notes

*Every song lives in on-device SQLite. No account. No server. Works offline on stage.*

</td>
<td width="50%" valign="top">

### 📊 [GradeMatrix](https://github.com/qwzynx/GradeCalc) · [live ↗](https://grade-calc-nine.vercel.app)
`Next.js 16` · `React 19` · `Supabase` · `Gemini` · `Recharts`

**Drop in a PDF syllabus, get a fully modelled course back.**

The Gemini-backed parser pulls out course code, professor, semester, credits **and** the entire grading scheme — then splits exam/project/quiz aggregates into individually trackable items.

- 🎯 **Target Grade Planner** — name your desired final grade, get the exact average you need on everything left
- 📈 **Max Potential Mark** — live ceiling if you ace every remaining assessment
- 🧮 **Dual GPA scales** — standard 4.0 *and* York's 9.0 scale, side by side
- 🔍 Filter by semester, year, department (`LE/EECS`, `SC/MATH`), and status
- 🔐 Supabase auth with row-level security, so your grades are actually yours

*Built because manually recomputing "what do I need on the final?" every week is a solved problem.*

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📡 [Anti-FOMO](https://github.com/qwzynx/anti-fomo)
`Next.js 15` · `FastAPI` · `Playwright` · `SQLAlchemy`

**One dashboard for every deadline, internship, and hackathon you were about to miss.**

An async pipeline aggregates 200+ live items from **8 sources** — SimplifyJobs, Pitt CSC, Hacker News, Phoronix, TLDR Tech, daily.dev, and Luma — then ranks them for CS students.

- 🌍 **Location normalization engine** turns messy markdown into clean `Remote` / `Hybrid` / `On-site` + region tags (Toronto, Waterloo, SF…)
- 🔐 **YorkU eClass integration done right** — login happens in a popup on York's *own* `passportyork.yorku.ca` domain, so **Duo 2FA works natively** and no password ever reaches my backend
- 🍪 Playwright captures the session cookie only *after* 2FA succeeds — **zero credential storage**
- 🃏 Slide-over detail drawers with full descriptions and direct apply links

*The security design here is the point: the safest credential handler is the one that never sees a credential.*

</td>
<td width="50%" valign="top">

### 🌐 [Portfolio](https://github.com/qwzynx/Portfolio) · [live ↗](https://www.mahanghafarian.com/)
`Next.js 16` · `React 19` · `Tailwind v4` · `Framer Motion`

**My engineering portfolio — and a playground for motion design.**

- 🎭 Framer Motion transitions with scroll-snap section navigation
- 🎨 Glassmorphic dark UI, custom gradients, dynamic typewriter hero
- 🔍 Full SEO pass: JSON-LD schema, OpenGraph, Twitter cards
- 📱 Responsive from small phones to ultra-wide

### 🎬 [MG Studio](https://github.com/qwzynx/studio) · [live ↗](https://studio.mahanghafarian.com/)
`Next.js` · `TypeScript`

**Sister site for my photography & videography work.**

Same dark DNA as the main portfolio, rebuilt around a **camera/cinema visual language** — letterbox bars, a viewfinder-framed hero, and film-strip cards. Each collection gets its own gallery route with per-photo EXIF.

</td>
</tr>
</table>

<details>
<summary><b>🔧 Also on the shelf — hardware, coursework & experiments</b></summary>

<br />

| Project | Stack | What it is |
| :-- | :-- | :-- |
| 📦 [**FocusBox**](https://github.com/qwzynx/ENG1102) | `Java` · `firmata4j` · `Arduino` | A physical study timer that keeps your phone honest. An **LDR detects** if you pull the phone out early and fires a flashing alarm plus a time penalty; a **PIR sensor** pauses the clock when you walk away; a potentiometer sets session length; an SSD1306 OLED drives the UI. Housed in a 3D-printed enclosure that went through several print iterations. |
| 🦆 [**Pico-Ducky 3.0**](https://github.com/qwzynx/Pico-Ducky3.0) | `Python` · `Pico 2W` | A fork I've been picking apart to understand **DuckyScript 3.0 parsing and HID injection** on a Raspberry Pi Pico 2W — the hands-on half of my hardware-security reading. |
| 🐍 [**FOMO**](https://github.com/qwzynx/FOMO) | `Python` | The original CLI scraper prototype. Proved the aggregation idea worked, then got rebuilt properly as Anti-FOMO. |

</details>

---

## 📈 GitHub in numbers

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-fast.vercel.app/api?username=qwzynx&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&theme=github_dark&title_color=3ECF8E&icon_color=1793D1&bg_color=0D1117" />
  <img src="https://github-readme-stats-fast.vercel.app/api?username=qwzynx&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&theme=default&title_color=2E7D5B&icon_color=1793D1" alt="Mahan's GitHub stats" height="170" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-fast.vercel.app/api/top-langs/?username=qwzynx&layout=compact&langs_count=8&hide_border=true&theme=github_dark&title_color=3ECF8E&bg_color=0D1117" />
  <img src="https://github-readme-stats-fast.vercel.app/api/top-langs/?username=qwzynx&layout=compact&langs_count=8&hide_border=true&theme=default&title_color=2E7D5B" alt="Most used languages" height="170" />
</picture>

<br /><br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=qwzynx&hide_border=true&theme=github-compact&bg_color=0D1117&color=3ECF8E&line=1793D1&point=FFFFFF&area=true" />
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=qwzynx&hide_border=true&theme=github-light&color=2E7D5B&line=1793D1&area=true" alt="Contribution activity graph" width="100%" />
</picture>

<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=qwzynx&theme=github_dark&utcOffset=-4" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=qwzynx&theme=default&utcOffset=-4" alt="When I commit (EDT)" width="47%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=qwzynx&theme=github_dark" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=qwzynx&theme=default" alt="Repositories per language" width="47%" />
</picture>

</div>

---

## 🌱 What I'm working on right now

- 🎸 **Shipping Fretnote 0.3.x** — CI-built releases across Linux, Windows, macOS and Android, and hardening the library merge/restore path so moving a songbook phone → desktop can never lose a note.
- 🔐 **Going deeper on offensive security** — penetration testing methodology and HID injection, with the goal of writing software that assumes an attacker read the source.
- 🧩 **Making my side projects boring to maintain** — typed end to end, tested where it counts, documented well enough that future-me doesn't have to re-read the code.
- 🤝 **Growing GDG York** — building the content that gets people in the room.

---

<div align="center">

### 💬 Let's build something

Open to **internships, collaborations, and interesting problems** — especially anything at the intersection of security, systems, and things people actually use.

<a href="mailto:mahan207gh@gmail.com"><img src="https://img.shields.io/badge/Say%20hi-mahan207gh%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email me" /></a>
<a href="https://www.mahanghafarian.com/"><img src="https://img.shields.io/badge/See%20the%20work-mahanghafarian.com-0B0B0B?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio" /></a>

<br /><br />

<i>"Coding is my jam."</i> 🎸

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF3E00,50:3ECF8E,100:1793D1&height=110&section=footer" alt="" width="100%" />

</div>

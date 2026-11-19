# AK Consultancy creative toolkit (the "base")

Everything we can create with, in one place. Every cloud run (scheduled or manual) starts with:

```
git clone --depth 1 https://github.com/harneetsingh26/ak-media
bash ak-media/studio/toolkit/install.sh
```

Then pick the best tools for the job from the menu below and READ their SKILL.md files
(in ~/ak-toolkit/skills/<name>/SKILL.md) before building. Nothing is left out: if a piece
doesn't need a tool, skip it for that piece, but it stays in the base.

## 1. Planning, writing and growth agents (claude.ai skills, load with the Skill tool)
| Agent | Use for |
|---|---|
| ak-instagram-autopilot | Master brief, pipelines, compliance (always load first) |
| ig-viral | What is working now in visa / study / travel niche |
| ig-plan | Weekly calendar |
| ig-audit | What worked, what flopped, why |
| ig-profile | Profile score /100, bio, highlights, pinned 3 |
| ig-reel | Hooks, script, on-screen text, beat sheet |
| ig-carousel | Carousel cover + slides (1080x1350) |
| ig-story | Story sequence + stickers |
| ig-caption | Caption, single ask, hashtags |
| ig-human | Remove AI tone from every text |
| ig-comment / ig-reply / ig-dm | Engagement, replies, lead DMs |
| ig-repurpose | One long video -> a week of posts |
| video-making | Rendering rules for finished MP4s |

## 2. Video, motion and 3D engines (installed by install.sh)
| Tool | Skills to read | Best for | Licence |
|---|---|---|---|
| HyperFrames (HeyGen) | hyperframes-hyperframes, -cli, -media-use, -slideshow, -style-sampling, -reverse-any-video, -registry, -figma, -remotion-to-hyperframes | Main renderer: HTML + GSAP -> MP4, captions, overlays, slideshows, copying a reference video's style | Apache-2.0, free |
| motionmaxxing | motionmaxxing | Director-level motion: measured easing curves, kinetic type, brand stings, scripted QA (look.py, lint.mjs); voiceover if an ElevenLabs key is set | Apache-2.0, free |
| 3DViz Pro Max | 3dviz-pro-max | Real 3D: plane over globe, passport / calendar flip, 3D logo, Three.js or Blender scenes (223 recipes) | MIT, free |
| Remotion | remotion-create, -best-practices, -captions, -render, -multimedia, -maps, -markup, -studio, -docs, -license | React-based video, animated maps (travel routes), data/caption-heavy reels | Free for companies with up to 3 employees; larger companies need a Remotion company licence (read remotion-license) |
| claude-shorts | claude-shorts | Cut a long video (webinar, client call, YouTube) into vertical shorts with animated captions | MIT, free |
| Our own engine | studio/render.py + studio/templates/ | Backup renderer, approved chrome-glass look; reel-3d-globe-3galtiyan = approved 3D sample | ours |

## 2b. Sound tools (added 19 Nov 2026)
| Tool | Skills to read | Best for | Licence |
|---|---|---|---|
| earshot | earshot-earshot, earshot-real-sound | Claude "hears" the mix: checks loudness, finds weak or missing sounds, puts a real sound on the exact frame; 201-sound bank made in code (no download needed) | MIT, free |
| SFX Kit (wyzowl) | read ~/ak-toolkit/sfx-kit/GUIDE.md and catalogue.md | 320 real recorded sound effects (whoosh, pop, click, logo sting...) with notes on when to use each; works offline, replaces Openverse until that is unblocked. Use these FIRST, synthesized sounds second | CC0, free, no credit needed |
| Motion Studio skills | studio-sfx-sync, studio-mix-master, studio-music-to-picture, studio-frame-review, studio-reference-study, studio-launch-film-studio, studio-stage-and-camera, studio-footage-cleanup | Sound on the exact frame, mixing to -14 LUFS for Instagram, cutting picture to music, frame-by-frame review, studying a reference reel | MIT, free |
| Openverse API | (no skill, use the API) | 52 lakh+ free sounds (Wikimedia, Jamendo, Freesound) | free; each sound has its own licence: use only CC0 / CC-BY and credit CC-BY in the caption. Currently BLOCKED by the cloud network allowlist (api.openverse.org) until it is allowed in claude.ai Settings > Capabilities |
| HyperFrames media-use | hyperframes-media-use | Music, SFX, voiceover, icons, colour grades | Apache-2.0 |

## 2c. Design, text, research and code tools (added 19 Nov 2026)
| Tool | Skills to read | Best for | Licence |
|---|---|---|---|
| UI UX Pro Max | uiux-ui-ux-pro-max, uiux-design, uiux-design-system, uiux-brand, uiux-banner-design, uiux-slides, uiux-ui-styling | Styles, colour palettes, font pairs, banners, brand kits, slides, carousels | MIT |
| Impeccable | impeccable | Polished, non-generic visual design for pages, cards, carousels | Apache-2.0 |
| Hallmark | hallmark | Turns "AI-looking" design into human-looking design | MIT |
| Diagram Design | diagram-design | Branded infographics: process steps, timelines, comparisons (great for carousels: "USA visa process in 5 steps") | MIT |
| Humanizer | humanizer | Removes signs of AI writing (use with ig-human on every caption, script, DM) | MIT |
| Last 30 Days | last30days | What people said in the last 30 days on Reddit / X / YouTube about a topic (visa news, trends) for ig-viral and ig-plan | MIT |
| Scrapling | scrapling | Reading public web pages for research (public info only; respect site rules; never collect personal data) | BSD-3 |
| REA (reverse engineer anything) | reverse-engineer-anything | Breaking down how a competitor reel, page or funnel works | MIT |
| Ponytail | ponytail, ponytail-review, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help | Keeps our own scripts (render.py, sound.py) short and clean | MIT |
| yt-dlp + faster-whisper | (programs) | Download a reference reel the team owns or has rights to study, and transcribe it, for learn-style. faster-whisper needs `install.sh --full` | free |

## 2d. Looked at but NOT added (and why)
- Onyx: a full self-hosted AI chat app (needs its own server and database), not a skill. Not useful inside our cloud runs.
- OmniRoute: routes Claude Code to other AI models to save tokens. Our scheduled runs already run on Claude, and routing our data through other model providers adds risk for client info.
- Clipwing / "RealSFX" (shown in 2 reels): no public download could be found. earshot real-sound + SFX Kit + sfx-sync do the same job (real sounds placed on the exact frame).

## 3. Which tool for which piece
- Faceless reel (default): ig-reel -> motionmaxxing (direction + easing) -> HyperFrames (build + render) -> sound effects -> QA.
- Reel marked "3D" or travel / study topic: add a 3dviz-pro-max scene (globe, plane path, passport, 3D logo).
- Route / map reel ("Delhi to New York"): Remotion maps or HyperFrames.
- Long video from the team: claude-shorts or ig-repurpose.
- Copy the style of a reel we like: hyperframes-reverse-any-video / style-sampling (style only, never copy content, music or logos).
- Carousel: ig-carousel (static JPEGs). Story: ig-story (+ HyperFrames for video stories).
- Sound on every video: pick real sounds from SFX Kit (then earshot's bank, then synthesized) -> studio-sfx-sync places effects on the frame -> studio-mix-master to about -14 LUFS (Instagram level), true peak -1 dB -> earshot listens and flags missing / weak sounds before posting.
- Carousel or infographic: ig-carousel + uiux-ui-ux-pro-max (style) + diagram-design (steps/timelines) + hallmark or impeccable check.
- Every text: ig-human + humanizer.
- Weekly research: ig-viral + last30days (+ scrapling for public pages) + reverse-engineer-anything on 1 competitor reel.
- If any tool fails: studio/render.py. Never skip a post because of a tool.

## 3b. Learn-style: our style memory (from the "teach Claude your editing style" reel)
- Our approved style lives in `studio/styles/my-style.md` in this repo. EVERY run reads it before building anything.
- To learn from a new reference reel: studio-reference-study (or hyperframes-reverse-any-video) on the file -> write what was learned (colours, fonts, pacing, cut length, caption style, sound pattern) into my-style.md under "Learned from references", with the date. Study style only; never copy someone else's content, music, logos or faces.
- When the user approves or rejects a video, add one line to my-style.md (what they liked / disliked). This is how the system gets better every week.

## 4. Always-on quality rules
- Sound: every cut / pop / tick / slam / CTA gets an auto-matched sound effect (synthesized or royalty-free only).
- Easing: named curves, never linear. Hook words get tracking + weight animation.
- 1080x1920, H.264 + AAC, text inside safe zones, QA stills before final render.
- Compliance from ak-instagram-autopilot section 5 applies to everything.
- Weekly: profile + last-12-posts audit (ig-audit + ig-profile).

## 5. Adding a new tool later
Add one `grab owner/repo folder` line and one `link` line to install.sh, add a row here, commit to main.
Every future run picks it up automatically.

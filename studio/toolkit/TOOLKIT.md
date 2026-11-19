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
| Our own engine | studio/render.py + studio/templates/ | Backup renderer, approved chrome-glass look | ours |

## 3. Which tool for which piece
- Faceless reel (default): ig-reel -> motionmaxxing (direction + easing) -> HyperFrames (build + render) -> sound effects -> QA.
- Reel marked "3D" or travel / study topic: add a 3dviz-pro-max scene (globe, plane path, passport, 3D logo).
- Route / map reel ("Delhi to New York"): Remotion maps or HyperFrames.
- Long video from the team: claude-shorts or ig-repurpose.
- Copy the style of a reel we like: hyperframes-reverse-any-video / style-sampling (style only, never copy content, music or logos).
- Carousel: ig-carousel (static JPEGs). Story: ig-story (+ HyperFrames for video stories).
- If any tool fails: studio/render.py. Never skip a post because of a tool.

## 4. Always-on quality rules
- Sound: every cut / pop / tick / slam / CTA gets an auto-matched sound effect (synthesized or royalty-free only).
- Easing: named curves, never linear. Hook words get tracking + weight animation.
- 1080x1920, H.264 + AAC, text inside safe zones, QA stills before final render.
- Compliance from ak-instagram-autopilot section 5 applies to everything.
- Weekly: profile + last-12-posts audit (ig-audit + ig-profile).

## 5. Adding a new tool later
Add one `grab owner/repo folder` line and one `link` line to install.sh, add a row here, commit to main.
Every future run picks it up automatically.

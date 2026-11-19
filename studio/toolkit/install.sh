#!/usr/bin/env bash
# AK Consultancy creative toolkit - installs every video/3D/motion agent into a cloud run.
# Usage (from the ak-media clone):  bash studio/toolkit/install.sh
# Safe to run every time. If one tool fails, the others still install.
set -u
TK="$HOME/ak-toolkit"
SK="$TK/skills"
mkdir -p "$TK" "$SK"

grab () {  # grab <owner/repo> <folder>
  if [ -d "$TK/$2/.git" ]; then echo "[ok]   $2 (already here)"; return; fi
  if timeout 300 git clone -q --depth 1 "https://github.com/$1" "$TK/$2"; then
    echo "[ok]   $2"
  else
    echo "[FAIL] $2 - skip it and use the backup engine (studio/render.py)"
  fi
}

grab heygen-com/hyperframes        hyperframes      # HTML + GSAP -> MP4 (Apache-2.0)
grab Tejashmakwana/motionmaxxing   motionmaxxing    # pro motion direction, measured easing, QA gates (Apache-2.0)
grab viettranx/3dviz-pro-max       3dviz-pro-max    # Three.js / Blender 3D scenes, 223 recipes (MIT)
grab agricidaniel/claude-shorts    claude-shorts    # long video -> viral shorts, animated captions (MIT)
grab remotion-dev/remotion         remotion         # React video engine (Remotion Licence - see TOOLKIT.md)
# --- added 19 Nov 2026 (second batch of reels) ---
grab Leonxlnx/earshot              earshot          # SOUND: hear/critique audio, 201 code-made SFX bank, real-sound on exact frame (MIT)
grab wyzowl/sfx-kit                sfx-kit          # SOUND: 320 real sound effects made for AI agents, CC0 (free, no credit needed); read GUIDE.md + catalogue.md
grab Meraj-08/motion-studio-skills motion-studio    # SOUND+FILM: sfx-sync, mix-master, music-to-picture, frame-review, reference-study (MIT)
grab blader/humanizer              humanizer        # TEXT: remove AI-writing signs (MIT)
grab Nutlope/hallmark              hallmark         # DESIGN: AI-slop design -> human design (MIT)
grab pbakaus/impeccable            impeccable       # DESIGN: polished front-end / visual design rules (Apache-2.0)
grab nextlevelbuilder/ui-ux-pro-max-skill ui-ux-pro-max  # DESIGN: styles, palettes, fonts, banners, brand, slides (MIT)
grab cathrynlavery/diagram-design  diagram-design   # DESIGN: branded diagrams/infographics as HTML/SVG (MIT)
grab mvanhorn/last30days-skill     last30days       # RESEARCH: last 30 days of Reddit / X / YouTube trends on a topic (MIT)
grab D4Vinci/Scrapling             scrapling        # RESEARCH: web scraping of public pages (BSD-3)
grab morluto/rea                   rea              # RESEARCH: reverse-engineer anything (MIT)
grab DietrichGebert/ponytail       ponytail         # CODE: lean, senior-dev style code for our scripts (MIT)

# Collect every SKILL.md folder in one place so a run can read them.
link () { [ -d "$1" ] && ln -sfn "$1" "$SK/$2"; }
for d in "$TK"/hyperframes/skills/*/;               do link "$d" "hyperframes-$(basename "$d")"; done
link "$TK/motionmaxxing"                            motionmaxxing
link "$TK/3dviz-pro-max/skills/3dviz-pro-max"       3dviz-pro-max
link "$TK/claude-shorts"                            claude-shorts
for d in "$TK"/remotion/packages/skills/skills/*/;  do link "$d" "$(basename "$d")"; done
for d in "$TK"/earshot/skills/*/;                   do link "$d" "earshot-$(basename "$d")"; done
for d in "$TK"/motion-studio/skills/*/;             do link "$d" "studio-$(basename "$d")"; done
link "$TK/humanizer"                                humanizer
link "$TK/hallmark/skills/hallmark"                 hallmark
link "$TK/impeccable/plugin/skills/impeccable"      impeccable
for d in "$TK"/ui-ux-pro-max/.claude/skills/*/;     do link "$d" "uiux-$(basename "$d")"; done
link "$TK/diagram-design/skills/diagram-design"     diagram-design
link "$TK/last30days/skills/last30days"             last30days
link "$TK/scrapling/agent-skill/Scrapling-Skill"    scrapling
link "$TK/rea/.agents/skills/reverse-engineer-anything" reverse-engineer-anything
for d in "$TK"/ponytail/skills/*/;                  do link "$d" "$(basename "$d")"; done

# Helper programs for learning a style from reference videos (video 4: Python, ffmpeg, yt-dlp, faster-whisper).
# Light by default. Run with --full to also install the heavy ones (faster-whisper, earshot's CPU audio models).
pip install -q --break-system-packages yt-dlp >/dev/null 2>&1 && echo "[ok]   yt-dlp" || echo "[FAIL] yt-dlp"
if [ "${1:-}" = "--full" ]; then
  timeout 900 pip install -q --break-system-packages faster-whisper >/dev/null 2>&1 && echo "[ok]   faster-whisper" || echo "[FAIL] faster-whisper"
  timeout 900 pip install -q --break-system-packages -e "$TK/earshot" >/dev/null 2>&1 && echo "[ok]   earshot CLI" || echo "[FAIL] earshot CLI (use its sound bank files directly)"
fi

# Also expose them to Claude's skill folder (picked up by new sessions).
mkdir -p "$HOME/.claude/skills"
for d in "$SK"/*; do ln -sfn "$(readlink -f "$d")" "$HOME/.claude/skills/$(basename "$d")"; done

echo
echo "Skills ready in $SK :"
ls "$SK"
echo
echo "Read the SKILL.md of each tool you use, e.g.  $SK/hyperframes-hyperframes/SKILL.md"

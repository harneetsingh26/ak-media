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

# Collect every SKILL.md folder in one place so a run can read them.
link () { [ -d "$1" ] && ln -sfn "$1" "$SK/$2"; }
for d in "$TK"/hyperframes/skills/*/;               do link "$d" "hyperframes-$(basename "$d")"; done
link "$TK/motionmaxxing"                            motionmaxxing
link "$TK/3dviz-pro-max/skills/3dviz-pro-max"       3dviz-pro-max
link "$TK/claude-shorts"                            claude-shorts
for d in "$TK"/remotion/packages/skills/skills/*/;  do link "$d" "$(basename "$d")"; done

# Also expose them to Claude's skill folder (picked up by new sessions).
mkdir -p "$HOME/.claude/skills"
for d in "$SK"/*; do ln -sfn "$(readlink -f "$d")" "$HOME/.claude/skills/$(basename "$d")"; done

echo
echo "Skills ready in $SK :"
ls "$SK"
echo
echo "Read the SKILL.md of each tool you use, e.g.  $SK/hyperframes-hyperframes/SKILL.md"

#!/usr/bin/env bash
# Copy every film's facts and narration text to its Drive folder, Creator/English/<slug>/repo/, keeping the paths
# (owner, 2026-11-25: "keep every fact check file in Drive, so even without the repo we can reply to comments").
# What goes: claims*.csv, fact-check*.md, research/, narration*.md, vo.txt, the VO blocks and transcripts recovered
# from Drive, captions (*.srt) and youtube/ text. A copy, never a sync: nothing in Drive is ever deleted.
#
# Usage: scripts/drive_text_backup.sh [slug ...]      (no slug: every folder in projects/ except channel-research)
# Runs at every stage's end in the session, and on every push to main (.github/workflows/drive-backup.yml).
# Needs GDRIVE_RCLONE_TOKEN; the same pinned rclone and token repair as scripts/gdrive_pull.sh.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
[[ -n ${GDRIVE_RCLONE_TOKEN:-} ]] || { echo "GDRIVE_RCLONE_TOKEN is not set" >&2; exit 3; }

# rclone and the token repair, as in scripts/gdrive_pull.sh
RCLONE_VER=v1.71.1
CACHE="$ROOT/.cache/rclone"
RCLONE="$CACHE/rclone-$RCLONE_VER-linux-amd64/rclone"
if [[ ! -x $RCLONE ]]; then
  mkdir -p "$CACHE"
  curl -sSL -m 300 -o "$CACHE/rclone.zip" "https://downloads.rclone.org/$RCLONE_VER/rclone-$RCLONE_VER-linux-amd64.zip"
  (cd "$CACHE" && unzip -q -o rclone.zip && rm rclone.zip)
fi
# Same token repair as upload_gdrive.sh: the Claude app's environment field strips parts of the JSON.
TOKEN=$(python3 - <<'EOF'
import json, os, re
t = os.environ["GDRIVE_RCLONE_TOKEN"].strip()
try:
    json.loads(t); print(t)
except ValueError:
    rt = re.search(r'refresh_token"?\s*:\s*"?([^",}\s]+)', t)
    at = re.match(r'[{\s"]*(?:access_token"?\s*:\s*"?)?(ya29[^",}\s]*)', t)
    if not rt:
        raise SystemExit("GDRIVE_RCLONE_TOKEN has no refresh_token; run rclone authorize again")
    print(json.dumps({"access_token": at.group(1) if at else "", "token_type": "Bearer",
                      "refresh_token": rt.group(1), "expiry": "2000-01-01T00:00:00Z"}))
EOF
)
export RCLONE_CONFIG_GD_TYPE=drive RCLONE_CONFIG_GD_SCOPE=drive RCLONE_CONFIG_GD_TOKEN="$TOKEN"
export RCLONE_CONFIG_GD_ROOT_FOLDER_ID="${GDRIVE_CREATOR_FOLDER_ID:-1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M}" RCLONE_CONFIG=/dev/null

slugs=("$@")
if [[ ${#slugs[@]} -eq 0 ]]; then
  for d in projects/*/; do s=$(basename "$d"); [[ $s == channel-research ]] || slugs+=("$s"); done
fi
for s in "${slugs[@]}"; do
  [[ -d projects/$s ]] || { echo "no projects/$s" >&2; continue; }
  "$RCLONE" copy "projects/$s" "gd:English/$s/repo" --retries 4 --low-level-retries 10 \
    --filter "- assets/**" --filter "- node_modules/**" --filter "- remotion/**" --filter "- *.py" \
    --filter "+ claims*.csv" --filter "+ fact-check*.md" --filter "+ research/**" \
    --filter "+ narration*.md" --filter "+ vo.txt" --filter "+ vo_blocks*.md" --filter "+ vo_block*.txt" \
    --filter "+ recovered-from-drive/vo/**" --filter "+ recovered-from-drive/youtube/**" --filter "+ *.srt" \
    --filter "+ youtube/**" --filter "+ vo/*.tsv" --filter "- *"
  echo "$s → Creator/English/$s/repo/: $("$RCLONE" lsf -R --files-only "gd:English/$s/repo" | wc -l) files"
done

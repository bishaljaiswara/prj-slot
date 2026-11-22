#!/usr/bin/env bash
set -euo pipefail
SOURCE="$(cd "$(dirname "$0")" && pwd)/games/twinkle_treats"
SDK_ROOT="${1:-}"
if [[ -z "$SDK_ROOT" || ! -f "$SDK_ROOT/src/config/config.py" ]]; then
  echo "Usage: ./install_into_sdk.sh /path/to/math-sdk" >&2
  exit 1
fi
TARGET="$SDK_ROOT/games/twinkle_treats"
if [[ -e "$TARGET" ]]; then
  echo "Target already exists: $TARGET. Use a clean SDK checkout." >&2
  exit 1
fi
cp -R "$SOURCE" "$TARGET"
echo "Installed overlay into $TARGET"
echo "From SDK root run: python games/twinkle_treats/run.py"

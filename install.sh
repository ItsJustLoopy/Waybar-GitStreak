#!/usr/bin/env bash
set -euo pipefail


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 
PY_SCRIPT="$SCRIPT_DIR/scripts/github_streak.py"
WAYBAR_SCRIPT="$SCRIPT_DIR/scripts/waybar_config.py"
WAYBAR_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/waybar"
WAYBAR_CONFIG="$WAYBAR_DIR/config.jsonc"

[[ -f "$WAYBAR_CONFIG" ]] || WAYBAR_CONFIG="$WAYBAR_DIR/config" 

[[ -f "$PY_SCRIPT" ]] || { echo "Missing $PY_SCRIPT"; exit 1; }
[[ -f "$WAYBAR_SCRIPT" ]] || { echo "Missing $WAYBAR_SCRIPT"; exit 1; }
[[ -f "$WAYBAR_CONFIG" ]] || { echo "Missing Waybar config in $WAYBAR_DIR"; exit 1; }

USERNAME="${GITHUB_USERNAME:-${1:-}}"
[[ -n "${USERNAME// }" ]] && python3 "$PY_SCRIPT" --set-username "$USERNAME" >/dev/null

python3 "$WAYBAR_SCRIPT" "$WAYBAR_CONFIG" "$PY_SCRIPT" 

echo "Installed. Restart Waybar."

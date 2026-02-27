#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNCONFIG_SCRIPT="$SCRIPT_DIR/scripts/waybar_unconfig.py"
WAYBAR_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/waybar"
WAYBAR_CONFIG="$WAYBAR_DIR/config.jsonc"
APP_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/waybar-gitstreak"
APP_CONFIG_FILE="$APP_CONFIG_DIR/config.json"

[[ -f "$WAYBAR_CONFIG" ]] || WAYBAR_CONFIG="$WAYBAR_DIR/config"
[[ -f "$UNCONFIG_SCRIPT" ]] || { echo "Missing $UNCONFIG_SCRIPT"; exit 1; }

if [[ -f "$WAYBAR_CONFIG" ]]; then
  python3 "$UNCONFIG_SCRIPT" "$WAYBAR_CONFIG"
fi

rm -f "$APP_CONFIG_FILE"
rmdir "$APP_CONFIG_DIR" 2>/dev/null || true

echo "Uninstalled. Restart Waybar."

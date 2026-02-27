import os
import json
import re
import sys
from datetime import date, datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


config = {
    "name": "github_streak",
    "icon": "",
    "color": "#333",
    "unit": "day(s)"
}

APP_CONFIG_DIR = os.path.expanduser("~/.config/waybar-gitstreak")
APP_CONFIG_PATH = os.path.join(APP_CONFIG_DIR, "config.json")


def load_saved_username() -> str | None:
    try:
        with open(APP_CONFIG_PATH, "r", encoding="utf-8") as config_file:
            data = json.load(config_file)
            username = data.get("username")
            return username if isinstance(username, str) and username else None
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def save_username(username: str) -> bool:
    try:
        os.makedirs(APP_CONFIG_DIR, exist_ok=True)
        with open(APP_CONFIG_PATH, "w", encoding="utf-8") as config_file:
            json.dump({"username": username.strip()}, config_file)
        return True
    except OSError:
        return False


def resolve_username() -> str | None:
    env_username = os.getenv("GITHUB_USERNAME")
    if env_username:
        return env_username
    return load_saved_username()


def get_config() -> dict | None:
    username = resolve_username()

    if not username:
        return None

    return {
        **config,
        "username": username,
    }


def get_active_dates_public(username: str) -> set[date]:
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "waybar-github-streak",
        "Accept": "text/html",
    }
    request = Request(url, headers=headers)

    with urlopen(request) as response:
        svg = response.read().decode("utf-8")

    active_dates: set[date] = set()
    day_cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"', svg)

    for day_str, level_str in day_cells:
        if int(level_str) > 0:
            active_dates.add(datetime.strptime(day_str, "%Y-%m-%d").date())

    return active_dates


def get_streak_status(username: str) -> tuple[int, bool]:
    try:
        active_dates = get_active_dates_public(username)

        today = date.today()
        yesterday = today - timedelta(days=1)

        if today in active_dates:
            anchor_day = today
            at_risk = False
        elif yesterday in active_dates:
            anchor_day = yesterday
            at_risk = True
        else:
            return 0, False

        streak = 0
        current = anchor_day
        while current in active_dates:
            streak += 1
            current -= timedelta(days=1)

        return streak, at_risk
    except (HTTPError, URLError, ValueError, KeyError, TypeError):
        return 0, False
    except Exception:
        return 0, False


def to_waybar_output(user_config: dict | None) -> dict: 
    if not user_config:
        return {
            "text": " ?",
            "tooltip": "Set GITHUB_USERNAME or run: github_streak.py --set-username <name>",
            "class": "error",
        }

    streak_value, at_risk = get_streak_status(user_config["username"])
    unit = user_config["unit"]

    tooltip = f"GitHub contribution streak: {streak_value} {unit}"
    css_class = "warning" if at_risk else "ok"
    if at_risk:
        tooltip = f"{tooltip} • No contribution yet today"

    return {
        "text": f" {user_config['icon']} {streak_value}",
        "tooltip": tooltip,
        "class": css_class,
        "at_risk": at_risk,
    }


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--set-username":
        success = save_username(sys.argv[2])
        if success:
            print(f"Saved username to {APP_CONFIG_PATH}")
        else:
            print("Failed to save username")
        raise SystemExit(0 if success else 1)

    user_config = get_config()
    output = to_waybar_output(user_config)
    print(json.dumps(output))

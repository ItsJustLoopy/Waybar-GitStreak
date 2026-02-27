import os
import json
import re
from datetime import date, datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


config = {
    "name": "github_streak",
    "icon": "",
    "color": "#333",
    "unit": "day(s)"
}


def get_config() -> dict | None:
    username = os.getenv("GITHUB_USERNAME")

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
            "tooltip": "Set GITHUB_USERNAME",
            "class": "error",
        }

    streak_value, at_risk = get_streak_status(user_config["username"])
    unit = user_config["unit"]

    tooltip = f"GitHub contribution streak: {streak_value} {unit}"
    css_class = "warning" if at_risk else "ok"
    if at_risk:
        tooltip = f"{tooltip} • No contribution yet today"

    return {
        "text": f"{user_config['icon']} {streak_value}",
        "tooltip": tooltip,
        "class": css_class,
        "at_risk": at_risk,
    }


if __name__ == "__main__":
    user_config = get_config()
    output = to_waybar_output(user_config)
    print(json.dumps(output))

import os
import json
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
    token = os.getenv("GITHUB_TOKEN")

    if not username or not token:
        return None

    return {
        **config,
        "username": username,
        "token": token,
    }


def get_streak(username: str, token: str) -> int:
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v4+json",
        "User-Agent": "waybar-github-streak",
        "Content-Type": "application/json",
    }

    query = """
    query ContributionCalendar($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays { date contributionCount }
            }
          }
        }
      }
    }
    """

    payload_data = {
        "query": query,
        "variables": {"login": username},
    }
    payload = json.dumps(payload_data).encode("utf-8")
    request = Request(url, data=payload, headers=headers, method="POST")

    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            graph_data = data["data"]
            user = graph_data["user"]
            contributions_collection = user["contributionsCollection"]
            contribution_calendar = contributions_collection["contributionCalendar"]
            weeks = contribution_calendar["weeks"]

            active_dates = {
                datetime.strptime(day["date"], "%Y-%m-%d").date()
                for week in weeks
                for day in week["contributionDays"]
                if day["contributionCount"] > 0
            }

            streak = 0
            current = date.today()
            while current in active_dates:
                streak += 1
                current -= timedelta(days=1)

            return streak
    except HTTPError:
        return 0
    except URLError:
        return 0
    except Exception:
        return 0


def to_waybar_output(user_config: dict | None) -> dict: 
    if not user_config:
        return {
            "text": " ?",
            "tooltip": "Set GITHUB_USERNAME and GITHUB_TOKEN",
            "class": "error",
        }

    streak_value = get_streak(user_config["username"], user_config["token"])
    unit = user_config["unit"]

    return {
        "text": f"{user_config['icon']} {streak_value}",
        "tooltip": f"GitHub contribution streak: {streak_value} {unit}",
        "class": "ok",
    }


if __name__ == "__main__":
    user_config = get_config()
    output = to_waybar_output(user_config)
    print(json.dumps(output))

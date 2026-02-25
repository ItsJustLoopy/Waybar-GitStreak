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
    except HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        return 0
    except URLError as e:
        print(f"URL error: {e.reason}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0


user_config = get_config()
user_config.update({"value": get_streak(user_config["username"], user_config["token"])}) if user_config else None

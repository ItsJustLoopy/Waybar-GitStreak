# Waybar GitStreak

To setup Waybar GitStreak, run the following command after replacing "<github_username>" with your own github username:

```bash
git clone https://github.com/ItsJustLoopy/Waybar-GitStreak Waybar-GitStreak && cd Waybar-GitStreak && ./install.sh <github_username>
```

Then restart Waybar using the command:

```bash
pkill waybar || true; waybar &
```

The installer adds `custom/github_streak` to `modules-center`, right of `clock` when present (always there for omarchy users if you have not changed it) and sets refresh to 5 minutes.

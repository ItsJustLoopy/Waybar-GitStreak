# Waybar GitStreak

![WaybarGitStreakPreview](https://github.com/user-attachments/assets/96b805c8-16d6-42f9-8d86-f488fb8055bd)

I created Waybar GitStreak as a way to keep myself motivated to make github contributions daily, and I hope this helps anyone hoping to do the same.


# Installation

To setup Waybar GitStreak, run the following command after replacing "<github_username>" with your own github username:

```bash
git clone https://github.com/ItsJustLoopy/Waybar-GitStreak Waybar-GitStreak && cd Waybar-GitStreak && ./install.sh <github_username>
```

Then restart Waybar using the command:

```bash
pkill waybar || true; waybar &
```

The installer adds `custom/github_streak` to `modules-center`, right of `clock` when present and sets refresh rate to 5 minutes by default.

# Uninstallation

To uninstall Waybar GitStreak, run the following command:

```bash
./uninstall.sh && pkill waybar || true; waybar &
```

Then restart Waybar using the command:

```bash
pkill waybar || true; waybar &
```

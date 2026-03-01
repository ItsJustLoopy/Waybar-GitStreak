# Waybar GitStreak
Waybar GitStreak is a script written in Python which integrates your current GitHub contribution streak right into the Waybar.

I created it as a way to keep myself motivated to make GitHub contributions daily, and I hope this helps anyone hoping to do the same.

![WaybarGitStreakPreview](https://github.com/user-attachments/assets/96b805c8-16d6-42f9-8d86-f488fb8055bd)
[Big thank you to <a href="https://www.github.com/OldJobobo" target="_blank">@OldJobobo</a> for the Monolith Omarchy theme used in the preview above.]

# Installation

To setup Waybar GitStreak, run the following command after replacing "<github_username>" with your own github username:

```bash
git clone https://github.com/ItsJustLoopy/Waybar-GitStreak Waybar-GitStreak && \
cd Waybar-GitStreak && \
./install.sh <github_username>
```

Then restart Waybar using the command:

```bash
pkill waybar || true; waybar &
```

The installer adds `custom/github_streak` to `modules-center`, right of `clock` when present and sets refresh rate to 5 minutes by default.

# Uninstallation

To uninstall Waybar GitStreak, run the following command:

```bash
cd Waybar-GitStreak && \
./uninstall.sh
```

Then restart Waybar using the command:

```bash
pkill waybar || true; waybar &
```

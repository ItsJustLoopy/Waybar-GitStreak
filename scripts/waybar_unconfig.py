import re
import sys


def main() -> int:
    if len(sys.argv) != 2:
        return 1

    config_path = sys.argv[1]

    with open(config_path, "r", encoding="utf-8") as file:
        text = file.read()

    text = re.sub(
        r'\n?\s*"custom/github_streak"\s*:\s*\{\n(?:.*\n)*?\s*\}(?:\s*,)?',
        "",
        text,
        flags=re.M,
    )

    for key in ("modules-left", "modules-center", "modules-right"):
        pattern = rf'("{key}"\s*:\s*\[)(.*?)(\])'
        match = re.search(pattern, text, flags=re.S)
        if not match:
            continue

        items = re.findall(r'"[^"]+"', match.group(2))
        items = [item for item in items if item != '"custom/github_streak"']

        if items:
            body = "\n    " + ",\n    ".join(items) + "\n  "
        else:
            body = ""

        replacement = match.group(1) + body + match.group(3)
        text = text[:match.start()] + replacement + text[match.end():]

    text = re.sub(r',\s*(\})', r'\1', text)
    text = re.sub(r'(\{\s*),', r'\1', text)

    with open(config_path, "w", encoding="utf-8") as file:
        file.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

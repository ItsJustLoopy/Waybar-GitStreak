import re
import sys


def main() -> int:
    if len(sys.argv) != 3:
        return 1

    config_path, py_script = sys.argv[1], sys.argv[2]

    with open(config_path, "r", encoding="utf-8") as file:
        text = file.read()

    module = (
        '  "custom/github_streak": {\n'
        f'    "exec": "python3 {py_script}",\n'
        '    "interval": 300,\n'
        '    "return-type": "json",\n'
        '    "format": "{}"\n'
        '  }'
    )

    if '"custom/github_streak"' not in text:
        i = text.rfind("}")
        pre = text[:i].rstrip()
        text = text[:i] + ((",\n" if pre and not pre.endswith("{") and not pre.endswith(",") else "\n") + module + "\n") + text[i:]

    m = re.search(r'("modules-center"\s*:\s*\[)(.*?)(\])', text, flags=re.S)
    if m:
        items = re.findall(r'"[^"]+"', m.group(2))
        if '"custom/github_streak"' not in items:
            idx = items.index('"clock"') + 1 if '"clock"' in items else len(items)
            items.insert(idx, '"custom/github_streak"')
            body = "\n    " + ",\n    ".join(items) + "\n  "
            text = text[:m.start()] + m.group(1) + body + m.group(3) + text[m.end():]
    else:
        i = text.rfind("}")
        pre = text[:i].rstrip()
        add = '  "modules-center": [\n    "custom/github_streak"\n  ]\n'
        text = text[:i] + ((",\n" if pre and not pre.endswith("{") and not pre.endswith(",") else "\n") + add) + text[i:]

    with open(config_path, "w", encoding="utf-8") as file:
        file.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

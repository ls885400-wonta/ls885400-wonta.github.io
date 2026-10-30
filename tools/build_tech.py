"""Build 첨단 공학 탐험관 (tech/index.html) from src/tech/template.html, content.js and media.json.

    python tools/build_tech.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    tpl = read("src", "tech", "template.html")
    media = json.loads(read("src", "tech", "media.json"))
    data = read("src", "tech", "content.js") + "\nconst MEDIA = " + json.dumps(media, ensure_ascii=False) + ";\n"
    assert tpl.count("/*DATA*/") == 1
    os.makedirs(os.path.join(ROOT, "tech"), exist_ok=True)
    with open(os.path.join(ROOT, "tech", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(tpl.replace("/*DATA*/", data))
    print(f"built tech/index.html (media for {len(media)} fields)")

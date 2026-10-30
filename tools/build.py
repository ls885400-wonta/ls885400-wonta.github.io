"""Build the three textbook courses from one engine.

    python tools/build.py

Reads  src/engine.html, src/courses/<id>.js, src/media/<id>.json
Writes <id>/index.html  (ai, design, robot)
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COURSES = {
    "ai": {
        "name": "인공지능 기초", "short": "AI", "key": "ai-stairs-v1", "eyebrow": "고등학교 인공지능 기초",
        "title": "AI 계단 교실", "desc": "고등학교 인공지능 기초를 이야기, 사진·영상, 계단식 확인문제, 용어 카드, 10문제 시험으로 배우는 학습 사이트",
        "accent": "#0CA678", "soft": "#E3F8F1", "deep": "#087F5B", "dark": "#38D9A9", "soft_dark": "#123A30",
    },
    "design": {
        "name": "창의 공학 설계", "short": "설계", "key": "design-stairs-v1", "eyebrow": "고등학교 창의 공학 설계",
        "title": "공학 설계 계단 교실", "desc": "고등학교 창의 공학 설계를 이야기, 사진·영상, 계단식 확인문제, 용어 카드, 10문제 시험으로 배우는 학습 사이트",
        "accent": "#1C7ED6", "soft": "#E7F2FD", "deep": "#1864AB", "dark": "#74C0FC", "soft_dark": "#15304A",
        "matrix": {"ideas": ["A 접이식 카트", "B 큰 바퀴 카트", "C 바구니 분리 카트"], "crit": ["시간", "비용", "재료"]},
    },
    "robot": {
        "name": "로봇과 공학세계", "short": "로봇", "key": "robot-stairs-v1", "eyebrow": "고등학교 로봇과 공학세계",
        "title": "로봇 공학 계단 교실", "desc": "고등학교 로봇과 공학세계를 이야기, 사진·영상, 계단식 확인문제, 용어 카드, 10문제 시험으로 배우는 학습 사이트",
        "accent": "#7048E8", "soft": "#F0ECFE", "deep": "#5F3DC4", "dark": "#B197FC", "soft_dark": "#2A2148",
        "matrix": {"ideas": ["A 컨베이어 벨트 분류기", "B 로봇 팔 분류기", "C 압축 로봇"], "crit": ["기능", "비용", "제작 난이도"]},
    },
}


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def build(cid, cfg):
    engine = read("src", "engine.html")
    data = read("src", "courses", f"{cid}.js")
    media_path = os.path.join(ROOT, "src", "media", f"{cid}.json")
    media = read("src", "media", f"{cid}.json") if os.path.exists(media_path) else "{}"
    meta = {"id": cid, "name": cfg["name"], "short": cfg["short"], "key": cfg["key"], "eyebrow": cfg["eyebrow"]}
    if "matrix" in cfg:
        meta["matrix"] = cfg["matrix"]
    block = f"const COURSE = {json.dumps(meta, ensure_ascii=False)};\n{data}\nconst MEDIA = {media.strip()};\n"
    assert engine.count("/*DATA*/") == 1
    html = engine.replace("/*DATA*/", block)
    for k, v in {"{{TITLE}}": cfg["title"], "{{DESC}}": cfg["desc"], "{{ACCENT}}": cfg["accent"], "{{ACCENT_SOFT}}": cfg["soft"],
                 "{{ACCENT_DEEP}}": cfg["deep"], "{{ACCENT_DARK}}": cfg["dark"], "{{ACCENT_SOFT_DARK}}": cfg["soft_dark"]}.items():
        html = html.replace(k, v)
    assert "{{" not in html, f"unfilled placeholder in {cid}"
    os.makedirs(os.path.join(ROOT, cid), exist_ok=True)
    with open(os.path.join(ROOT, cid, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"built {cid}/index.html ({len(html):,} chars, media for {len(json.loads(media))} lessons)")


if __name__ == "__main__":
    for cid, cfg in COURSES.items():
        build(cid, cfg)

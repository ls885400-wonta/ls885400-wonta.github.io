"""Check every photo, video and outside link used by the sites.

    python tools/check_media.py            -> prints a report, writes tools/last_check.json
Exit code 1 when something is broken.
Images: HTTP HEAD must return 200.  Videos: YouTube oEmbed must succeed (401/404 = removed or embedding disabled).
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "ai-stairs-edu/1.0 (classroom site; github ls885400-wonta)"}


def status(url, method="HEAD"):
    for a in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, method=method, headers=UA), timeout=20).status
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(4 * (a + 1)); continue
            if e.code in (403, 405) and method == "HEAD":
                return status(url, "GET")
            return e.code
        except Exception as e:
            return str(e)[:60]
    return 429


def video_ok(vid):
    u = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote("https://www.youtube.com/watch?v=" + vid)
    try:
        urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
        return True
    except Exception:
        return False


def items():
    for c in ("ai", "design", "robot", "wood"):
        p = os.path.join(ROOT, "src", "media", f"{c}.json")
        for lid, m in json.load(open(p, encoding="utf-8")).items():
            where = f"{c}/{lid}"
            if m.get("img"):
                yield where, "img", m["img"]["thumb"]; yield where, "img", m["img"]["big"]
            for v in m.get("videos", []):
                yield where, "video", v["id"]
            for label, url in m.get("links", []):
                if url.startswith("http"):
                    yield where, "link", url
    res = open(os.path.join(ROOT, "src", "courses", "wood.js"), encoding="utf-8").read()
    for url in re.findall(r'url:"(https://[^"]+)"', res):
        if "instagram.com" not in url:  # Instagram answers 200 for every handle, so it cannot be checked
            yield "wood/resources", "link", url
    for fid, m in json.load(open(os.path.join(ROOT, "src", "tech", "media.json"), encoding="utf-8")).items():
        where = f"tech/{fid}"
        yield where, "img", m["img"]["card"]; yield where, "img", m["img"]["big"]
        for v in m["videos"]:
            yield where, "video", v["id"]
        if m.get("wiki"):
            yield where, "link", m["wiki"]
    hub = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    for u in re.findall(r'<img src="(https://[^"]+)"', hub):
        yield "hub", "img", u


if __name__ == "__main__":
    broken, n = [], 0
    for where, kind, ref in items():
        n += 1
        ok = video_ok(ref) if kind == "video" else status(ref) == 200
        if not ok:
            broken.append({"where": where, "kind": kind, "ref": ref})
            print(f"BROKEN {kind:5} {where:18} {ref}")
        time.sleep(0.35)
    json.dump({"checked": n, "broken": broken, "at": time.strftime("%Y-%m-%d %H:%M")},
              open(os.path.join(ROOT, "tools", "last_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"checked {n}, broken {len(broken)}")
    sys.exit(1 if broken else 0)

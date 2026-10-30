# 주간 업그레이드 절차 (Weekly upgrade routine)

The scheduled weekly task follows these steps in `D:\인공지능 학습 관련\클로드 연습`.
Git is at `C:\Program Files\Git\cmd\git.exe`; GitHub sign-in is already stored (Git Credential Manager).
Never ask for or type passwords or tokens.

## 1. Repair (every week)
1. `python -X utf8 tools/check_media.py` — checks every photo, video and outside link.
2. For each broken item in `tools/last_check.json`:
   - **video**: find a replacement on YouTube for the same topic from a trustworthy channel
     (YTN 사이언스, EBS, KBS, 국가과학기술연구회, 한국항공우주연구원, 대학·공공기관, the company that makes the thing).
     Confirm it with YouTube oEmbed (`https://www.youtube.com/oembed?format=json&url=...`) — a 401/404 means removed or not embeddable.
   - **img**: pick another freely licensed Wikimedia Commons photo of the same subject. Only standard thumbnail widths work
     (330/500/960/1280px). Record artist, license and file page.
   - **link**: replace with the current URL of the same page, or remove it.
   Edit `src/media/<course>.json` (ai, design, robot) or `src/tech/media.json`.

## 2. Enrich (every week, small and careful)
- Add at most **3** new, high-quality items in total across the courses, for example: one newer video that explains a lesson
  better, one recent Korean news or institution page about a field (자율주행, 누리호, 인공지능 윤리 …), or a photo for a lesson
  that has none (`robot/3-2`).
- Prefer the public institution sites listed in the textbooks' own reference pages (한국항공우주연구원, 생명공학포털,
  한국건설기술연구원, 한국에너지공단, 엔트리, arduino.cc …).
- Never copy textbook text. Lesson text in `src/courses/*.js` and `src/tech/content.js` changes only to fix a factual error,
  and only when the fix is verified against a reliable source.
- No more than 2 videos per lesson; replace rather than pile up.

## 3. Build and test
```
python -X utf8 tools/build.py
python -X utf8 tools/build_tech.py
powershell -File tools/test_course.ps1 -Course ai      (and design, robot)
python -X utf8 tools/check_media.py
```
All course tests must print `bad=[]` with no `ERR`/`EX`, and the checker must report `broken 0`.
**If anything fails, do not publish.** Leave the changes uncommitted and describe the problem in the report.

## 4. Publish
- Add one entry at the top of `updates.json`: `{"date": "YYYY-MM-DD", "title": "...", "items": ["...", "..."]}`
  written for students in plain Korean (what is new, which lesson). Keep the list to the newest 12 entries.
- `git add -A ai design robot tech src tools index.html updates.json` → commit `"Weekly update YYYY-MM-DD: ..."` → `git push origin main`.
- Check https://ls885400-wonta.github.io/ responds after ~1–2 minutes.

## 5. Report
Finish with a short Korean summary for the teacher: what was repaired, what was added (with lesson names), test results,
and anything that needs the teacher's decision.

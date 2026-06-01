import json
import time

import requests

from config import GEMINI_API_KEY, ANALYZE_PROMPT, SCORE_THRESHOLD

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def _call_gemini(prompt, retries=2):
    for i in range(retries):
        try:
            resp = requests.post(
                API_URL,
                params={"key": GEMINI_API_KEY},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=60,
            )
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if resp.status_code in (429, 503):
                wait = 30 * (i + 1)
                print(f"[Gemini] {resp.status_code}，等待 {wait}s...")
                time.sleep(wait)
                continue
            print(f"[Gemini] HTTP {resp.status_code}: {resp.text[:100]}")
            return None
        except Exception as e:
            if i < retries - 1:
                time.sleep(30)
            else:
                print(f"[Gemini] 调用失败: {e}")
                return None
    return None


def _parse_json(raw):
    cleaned = raw.strip().strip("`")
    if cleaned.startswith("json"):
        cleaned = cleaned[4:]
    return json.loads(cleaned.strip())


def analyze(items):
    scored = []
    for item in items:
        content = item["content"][:3000]
        prompt = ANALYZE_PROMPT.format(
            title=item["title"], author=item["author"],
            platform=item["platform"], content=content,
        )
        raw = _call_gemini(prompt)

        if not raw:
            item["score"] = 0
            print(f"  [0分] {item['title'][:50]} — 调用失败")
            time.sleep(10)
            continue

        try:
            data = _parse_json(raw)
        except (json.JSONDecodeError, ValueError):
            item["score"] = 0
            print(f"  [0分] {item['title'][:50]} — 解析失败: {raw[:80]}")
            time.sleep(10)
            continue

        score = data.get("score", 0)
        reason = data.get("reason", "")
        item["score"] = score
        item["score_reason"] = reason
        print(f"  [{score}分] {item['title'][:50]} — {reason}")

        if score >= SCORE_THRESHOLD and data.get("summary"):
            item["summary"] = data.get("summary", "")
            scored.append(item)

        time.sleep(10)

    return scored

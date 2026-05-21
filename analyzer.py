import json
import time

import requests

from config import GEMINI_API_KEY, SCORE_PROMPT, SUMMARY_PROMPT, SCORE_THRESHOLD

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def _call_gemini(prompt, retries=5):
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
                wait = min(4 * (2 ** i), 60)
                print(f"[Gemini] {resp.status_code}，等待 {wait}s...")
                time.sleep(wait)
                continue
            print(f"[Gemini] HTTP {resp.status_code}: {resp.text[:100]}")
            return None
        except Exception as e:
            if i < retries - 1:
                time.sleep(4 * (2 ** i))
            else:
                print(f"[Gemini] 调用失败: {e}")
                return None
    return None


def _parse_json(raw):
    cleaned = raw.strip().strip("`")
    if cleaned.startswith("json"):
        cleaned = cleaned[4:]
    return json.loads(cleaned.strip())


def _score(item):
    content = item["content"][:3000]
    prompt = SCORE_PROMPT.format(
        title=item["title"], author=item["author"], content=content
    )
    raw = _call_gemini(prompt)
    if not raw:
        return 0, "调用失败"
    try:
        data = _parse_json(raw)
        return data.get("score", 0), data.get("reason", "")
    except (json.JSONDecodeError, ValueError):
        print(f"[Gemini] 打分解析失败: {raw[:100]}")
        return 0, "解析失败"


def _summarize(item):
    content = item["content"][:3000]
    prompt = SUMMARY_PROMPT.format(
        title=item["title"], author=item["author"], content=content
    )
    raw = _call_gemini(prompt)
    if not raw:
        return None
    try:
        return _parse_json(raw)
    except (json.JSONDecodeError, ValueError):
        print(f"[Gemini] 摘要解析失败: {raw[:100]}")
        return None


def analyze(items):
    scored = []
    for item in items:
        score, reason = _score(item)
        item["score"] = score
        item["score_reason"] = reason
        print(f"  [{score}分] {item['title'][:50]} — {reason}")

        if score >= SCORE_THRESHOLD:
            time.sleep(10)
            summary_data = _summarize(item)
            if summary_data:
                item["category"] = summary_data.get("category", "trend")
                item["headline"] = summary_data.get("headline", item["title"])
                item["detail"] = summary_data.get("detail", "")
                scored.append(item)

        time.sleep(10)

    return scored

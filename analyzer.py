import json
import time

import google.generativeai as genai

from config import GEMINI_API_KEY, SCORE_PROMPT, SUMMARY_PROMPT, SCORE_THRESHOLD

_model = None


def _get_model():
    global _model
    if _model is None:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-2.0-flash")
    return _model


def _call_gemini(prompt, retries=3):
    model = _get_model()
    for i in range(retries):
        try:
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** (i + 1))
            else:
                print(f"[Gemini] 调用失败: {e}")
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
            summary_data = _summarize(item)
            if summary_data:
                item["category"] = summary_data.get("category", "trend")
                item["summary"] = summary_data.get("summary", "")
                scored.append(item)

        time.sleep(1)

    return scored

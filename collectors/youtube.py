import re
import json
import time
import urllib.parse
import requests
from youtube_transcript_api import YouTubeTranscriptApi


_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def _parse_relative_hours(text):
    """将 '5 days ago' 等相对时间转为小时数，无法解析返回 None。"""
    if not text:
        return None
    text = text.replace("Streamed ", "").replace("Premiered ", "").strip()
    m = re.match(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago", text)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2)
    multipliers = {
        "second": 1 / 3600, "minute": 1 / 60, "hour": 1,
        "day": 24, "week": 168, "month": 720, "year": 8760,
    }
    return n * multipliers.get(unit, 0)


def fetch_recent_videos(handle, max_age_hours=28):
    url = f"https://www.youtube.com/@{handle}/videos"
    resp = requests.get(url, headers=_HEADERS, timeout=15)
    if resp.status_code != 200:
        return []

    m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});</script>", resp.text, re.DOTALL)
    if not m:
        return []

    data = json.loads(m.group(1))
    tabs = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])

    videos = []
    for tab in tabs:
        grid = tab.get("tabRenderer", {}).get("content", {}).get("richGridRenderer", {})
        if not grid:
            continue
        for item in grid.get("contents", []):
            lvm = item.get("richItemRenderer", {}).get("content", {}).get("lockupViewModel", {})
            if not lvm or lvm.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO":
                continue

            video_id = lvm.get("contentId", "")
            meta = lvm.get("metadata", {}).get("lockupMetadataViewModel", {})
            title = meta.get("title", {}).get("content", "")

            parts = (meta.get("metadata", {}).get("contentMetadataViewModel", {})
                     .get("metadataRows", [{}])[0].get("metadataParts", []))
            time_text = parts[1].get("text", {}).get("content", "") if len(parts) > 1 else ""

            age_hours = _parse_relative_hours(time_text)
            if age_hours is not None and age_hours <= max_age_hours:
                videos.append({
                    "video_id": video_id,
                    "title": title,
                    "published": time_text,
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                })
        break

    return videos


_ytt = YouTubeTranscriptApi()


def get_transcript(video_id):
    try:
        result = _ytt.fetch(video_id, languages=["zh-Hans", "zh", "en"])
        return " ".join(s.text for s in result.snippets)
    except Exception:
        return None


def collect(channels):
    results = []
    for ch in channels:
        videos = fetch_recent_videos(ch["handle"])
        for video in videos:
            transcript = get_transcript(video["video_id"])
            results.append({
                "platform": "YouTube",
                "author": ch["name"],
                "title": video["title"],
                "content": transcript or video["title"],
                "link": video["link"],
                "published": video["published"],
                "has_transcript": transcript is not None,
            })
        print(f"[YouTube] {ch['name']}: {len(videos)} 新视频")

    return results


def _search_videos(keyword, max_age_hours=48):
    query = urllib.parse.quote(keyword)
    url = f"https://www.youtube.com/results?search_query={query}"
    resp = requests.get(url, headers=_HEADERS, timeout=15)
    if resp.status_code != 200:
        return []

    m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});</script>", resp.text, re.DOTALL)
    if not m:
        return []

    data = json.loads(m.group(1))
    sections = (data.get("contents", {})
                .get("twoColumnSearchResultsRenderer", {})
                .get("primaryContents", {})
                .get("sectionListRenderer", {})
                .get("contents", []))

    videos = []
    for section in sections:
        items = section.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            vr = item.get("videoRenderer")
            if not vr:
                continue

            video_id = vr.get("videoId", "")
            title_runs = vr.get("title", {}).get("runs", [])
            title = title_runs[0].get("text", "") if title_runs else ""

            time_text = vr.get("publishedTimeText", {}).get("simpleText", "")
            channel_runs = vr.get("ownerText", {}).get("runs", [])
            channel = channel_runs[0].get("text", "") if channel_runs else ""

            age_hours = _parse_relative_hours(time_text)
            if age_hours is not None and age_hours <= max_age_hours:
                videos.append({
                    "video_id": video_id,
                    "title": title,
                    "published": time_text,
                    "channel": channel,
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                })
            if len(videos) >= 5:
                break
        if len(videos) >= 5:
            break

    return videos


def _is_negative(title, neg_kws):
    t = title.lower()
    return any(kw.lower() in t for kw in neg_kws)


def search_collect(keywords, negative_keywords=None):
    results = []
    seen_ids = set()
    for kw in keywords:
        videos = _search_videos(kw)
        for video in videos:
            vid = video["video_id"]
            if vid in seen_ids:
                continue
            if negative_keywords and _is_negative(video["title"], negative_keywords):
                continue
            seen_ids.add(vid)
            results.append({
                "platform": "YouTube",
                "author": video.get("channel", ""),
                "title": video["title"],
                "content": video["title"],
                "link": video["link"],
                "published": video["published"],
                "has_transcript": False,
            })
        print(f"[YouTube 搜索] '{kw}': {len(videos)} 结果")
        time.sleep(2)
    return results

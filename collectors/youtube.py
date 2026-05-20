import re
import feedparser
import requests
from datetime import datetime, timedelta, timezone
from youtube_transcript_api import YouTubeTranscriptApi


def resolve_channel_id(handle):
    url = f"https://www.youtube.com/@{handle}"
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; ai-news-monitor/1.0)"},
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    match = re.search(r'"channelId":"(UC[^"]+)"', resp.text)
    return match.group(1) if match else None


def fetch_recent_videos(channel_id, hours=28):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    videos = []
    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published > cutoff:
            videos.append({
                "video_id": entry.yt_videoid,
                "title": entry.title,
                "published": published.isoformat(),
                "link": entry.link,
            })
    return videos


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["zh-Hans", "zh", "en"]
        )
        return " ".join(t["text"] for t in transcript)
    except Exception:
        return None


def collect(channels):
    results = []
    for ch in channels:
        channel_id = resolve_channel_id(ch["handle"])
        if not channel_id:
            print(f"[YouTube] 无法解析频道: {ch['name']} (@{ch['handle']})")
            continue

        videos = fetch_recent_videos(channel_id)
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

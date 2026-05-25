import time

import requests

from config import DOUYIN_COOKIE

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/148.0.0.0 Safari/537.36",
    "Referer": "https://www.douyin.com/",
}

_API_BASE = "https://www.douyin.com/aweme/v1/web"


class _DouyinClient:
    def __init__(self):
        self._s = requests.Session()
        self._s.headers.update(_HEADERS)
        self._s.headers["Cookie"] = DOUYIN_COOKIE

    def get_recent_videos(self, sec_uid, max_age_hours=28):
        try:
            resp = self._s.get(
                f"{_API_BASE}/aweme/post/",
                params={
                    "device_platform": "webapp",
                    "aid": "6383",
                    "sec_user_id": sec_uid,
                    "max_cursor": "0",
                    "count": "18",
                    "version_code": "170400",
                    "version_name": "17.4.0",
                },
                timeout=15,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
            if data.get("status_code") != 0:
                print(f"  [抖音] API 错误: {data.get('status_msg', '')}")
                return []
        except Exception as e:
            print(f"  [抖音] 请求失败: {e}")
            return []

        cutoff = time.time() - max_age_hours * 3600
        videos = []
        for v in data.get("aweme_list") or []:
            create_time = v.get("create_time", 0)
            if create_time >= cutoff:
                aweme_id = v.get("aweme_id", "")
                videos.append({
                    "aweme_id": aweme_id,
                    "desc": v.get("desc", ""),
                    "create_time": create_time,
                    "link": f"https://www.douyin.com/video/{aweme_id}",
                })
        return videos


def collect(bloggers):
    if not DOUYIN_COOKIE:
        print("[抖音] DOUYIN_COOKIE 未配置，跳过")
        return []

    try:
        client = _DouyinClient()
    except Exception as e:
        print(f"[抖音] 初始化失败: {e}")
        return []

    results = []
    for blogger in bloggers:
        videos = client.get_recent_videos(blogger["sec_uid"])
        for video in videos:
            desc = video["desc"]
            title = desc.split("\n")[0].strip() or desc[:50]
            content = " ".join(
                part for part in desc.split() if not part.startswith("#")
            )
            results.append({
                "platform": "抖音",
                "author": blogger["name"],
                "title": title,
                "content": content or desc,
                "link": video["link"],
                "published": time.strftime(
                    "%Y-%m-%d", time.localtime(video["create_time"])
                ),
                "has_transcript": False,
            })
        print(f"[抖音] {blogger['name']}: {len(videos)} 新视频")
        time.sleep(2)

    return results

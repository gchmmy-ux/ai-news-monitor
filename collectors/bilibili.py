import hashlib
import time
import urllib.parse
from functools import reduce

import requests

from config import BILIBILI_SESSDATA

_MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
    27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
    37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
    22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
]

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


class _BiliClient:
    def __init__(self):
        self._s = requests.Session()
        self._s.headers.update(_HEADERS)
        self._s.cookies.set("SESSDATA", BILIBILI_SESSDATA, domain=".bilibili.com")
        self._init_cookies()
        self._init_wbi()

    def _init_cookies(self):
        resp = self._s.get("https://api.bilibili.com/x/frontend/finger/spi", timeout=10)
        data = resp.json()["data"]
        self._s.cookies.set("buvid3", data["b_3"], domain=".bilibili.com")
        self._s.cookies.set("buvid4", data["b_4"], domain=".bilibili.com")

    def _init_wbi(self):
        resp = self._s.get("https://api.bilibili.com/x/web-interface/nav", timeout=10)
        wbi = resp.json()["data"]["wbi_img"]
        img_key = wbi["img_url"].rsplit("/", 1)[1].split(".")[0]
        sub_key = wbi["sub_url"].rsplit("/", 1)[1].split(".")[0]
        orig = img_key + sub_key
        self._mixin_key = reduce(lambda s, i: s + orig[i], _MIXIN_KEY_ENC_TAB, "")[:32]

    def _sign(self, params):
        params["wts"] = round(time.time())
        params = dict(sorted(params.items()))
        params = {
            k: "".join(c for c in str(v) if c not in "!'()*")
            for k, v in params.items()
        }
        query = urllib.parse.urlencode(params)
        params["w_rid"] = hashlib.md5((query + self._mixin_key).encode()).hexdigest()
        return params

    def get_recent_videos(self, uid, max_age_hours=28):
        params = self._sign({"mid": uid, "order": "pubdate", "pn": 1, "ps": 10})
        try:
            resp = self._s.get(
                "https://api.bilibili.com/x/space/wbi/arc/search",
                params=params,
                headers={"Referer": f"https://space.bilibili.com/{uid}/video"},
                timeout=15,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
            if data["code"] != 0:
                print(f"  [B站] uid={uid} API 错误: {data.get('message', '')}")
                return []
        except Exception as e:
            print(f"  [B站] uid={uid} 请求失败: {e}")
            return []

        cutoff = time.time() - max_age_hours * 3600
        videos = []
        for v in data["data"]["list"]["vlist"]:
            if v["created"] >= cutoff:
                videos.append({
                    "bvid": v["bvid"],
                    "title": v["title"],
                    "created": v["created"],
                    "link": f"https://www.bilibili.com/video/{v['bvid']}",
                })
        return videos

    def get_subtitle(self, bvid):
        try:
            info = self._s.get(
                "https://api.bilibili.com/x/web-interface/view",
                params={"bvid": bvid},
                timeout=10,
            ).json()
            if info["code"] != 0:
                return None
            cid = info["data"]["cid"]
        except Exception:
            return None

        try:
            resp = self._s.get(
                "https://api.bilibili.com/x/player/wbi/v2",
                params={"bvid": bvid, "cid": cid},
                timeout=10,
            ).json()
            subs = resp["data"]["subtitle"]["subtitles"]
        except Exception:
            return None

        target = next(
            (s for s in subs if s["lan"] in ("ai-zh", "zh-Hans", "zh")),
            None,
        )
        if not target:
            return None

        try:
            url = target["subtitle_url"]
            if url.startswith("//"):
                url = "https:" + url
            body = self._s.get(url, timeout=10).json().get("body", [])
            return " ".join(item["content"] for item in body)
        except Exception:
            return None


def collect(up_hosts):
    if not BILIBILI_SESSDATA:
        print("[B站] BILIBILI_SESSDATA 未配置，跳过")
        return []

    try:
        client = _BiliClient()
    except Exception as e:
        print(f"[B站] 初始化失败: {e}")
        return []

    results = []
    for up in up_hosts:
        videos = client.get_recent_videos(up["uid"])
        for video in videos:
            subtitle = client.get_subtitle(video["bvid"])
            results.append({
                "platform": "B站",
                "author": up["name"],
                "title": video["title"],
                "content": subtitle or video["title"],
                "link": video["link"],
                "published": time.strftime("%Y-%m-%d", time.localtime(video["created"])),
                "has_transcript": subtitle is not None,
            })
            time.sleep(2)
        print(f"[B站] {up['name']}: {len(videos)} 新视频")
        time.sleep(2)

    return results

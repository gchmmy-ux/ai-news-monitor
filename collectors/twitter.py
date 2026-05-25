import asyncio
import time
from datetime import datetime, timezone, timedelta

from twscrape import API, gather

from config import TWITTER_COOKIE


async def _collect_async(accounts, max_age_hours=28):
    api = API("/tmp/twscrape.db")
    await api.pool.add_account("x", "x", "x@x.com", "x", cookies=TWITTER_COOKIE)
    await api.pool.login_all()

    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    results = []

    for account in accounts:
        try:
            user = await api.user_by_login(account["handle"])
            if not user:
                print(f"  [Twitter] @{account['handle']} 未找到")
                continue

            tweets = await gather(api.user_tweets(user.id, limit=20))
            count = 0
            for t in tweets:
                if t.date < cutoff:
                    continue
                if t.rawContent.startswith("RT @"):
                    continue

                first_line = t.rawContent.split("\n")[0].strip()
                results.append({
                    "platform": "Twitter",
                    "author": account["name"],
                    "title": first_line[:80] if first_line else t.rawContent[:80],
                    "content": t.rawContent,
                    "link": f"https://x.com/{account['handle']}/status/{t.id}",
                    "published": t.date.strftime("%Y-%m-%d"),
                    "has_transcript": True,
                })
                count += 1
            print(f"[Twitter] @{account['handle']}: {count} 新推文")
        except Exception as e:
            print(f"[Twitter] @{account['handle']} 失败: {e}")
        time.sleep(1)

    return results


def collect(accounts):
    if not TWITTER_COOKIE:
        print("[Twitter] TWITTER_COOKIE 未配置，跳过")
        return []

    try:
        return asyncio.run(_collect_async(accounts))
    except Exception as e:
        print(f"[Twitter] 采集失败: {e}")
        return []

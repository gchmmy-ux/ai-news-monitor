import os

import requests
from datetime import datetime, timezone, timedelta

from config import SERVER_CHAN_KEY

_beijing = timezone(timedelta(hours=8))


def _today():
    return datetime.now(_beijing).strftime("%Y-%m-%d")


def build_report(items, total_raw):
    lines = [f"AI 日报 · {_today()}\n"]

    for item in items:
        summary = item.get("summary", item.get("title", ""))
        source = f"{item['author']} · {item['platform']}"
        lines.append(f"• {summary}（{source}）\n")

    lines.append(f"{len(items)} 条精选 / {total_raw} 条采集")
    return "\n".join(lines)


def push_to_wechat(title, content):
    if not SERVER_CHAN_KEY:
        print("[推送] SERVER_CHAN_KEY 未配置，跳过推送")
        return False

    url = f"https://sctapi.ftqq.com/{SERVER_CHAN_KEY}.send"
    resp = requests.post(url, data={"title": title, "desp": content}, timeout=15)
    if resp.status_code == 200 and resp.json().get("code") == 0:
        print("[推送] 微信推送成功")
        return True
    print(f"[推送] 失败: {resp.text[:200]}")
    return False


def save_report(content):
    os.makedirs("reports", exist_ok=True)
    path = f"reports/AI日报.{_today()}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[备份] 日报已保存: {path}")
    return path


def publish(items, total_raw):
    if not items:
        print("[日报] 今日无符合条件的内容，跳过")
        return

    report = build_report(items, total_raw)
    push_to_wechat(f"AI 日报 · {_today()}", report)
    save_report(report)

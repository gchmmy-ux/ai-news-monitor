import os

import requests
from datetime import datetime, timezone, timedelta

from config import SERVER_CHAN_KEY

CATEGORY_META = {
    "breaking": ("🔴", "重大发布"),
    "update": ("📦", "产品更新"),
    "trend": ("📊", "行业动向"),
    "practice": ("🛠", "实操与落地"),
}
CATEGORY_ORDER = ["breaking", "update", "trend", "practice"]

_beijing = timezone(timedelta(hours=8))


def _today():
    return datetime.now(_beijing).strftime("%Y-%m-%d")


def build_report(items, total_raw):
    lines = [f"# AI 日报 · {_today()}\n"]

    grouped = {}
    for item in items:
        grouped.setdefault(item.get("category", "trend"), []).append(item)

    for key in CATEGORY_ORDER:
        cat_items = grouped.get(key)
        if not cat_items:
            continue
        icon, label = CATEGORY_META[key]
        lines.append(f"### {icon} {label}\n")
        for item in cat_items:
            headline = item.get("headline", item.get("summary", item["title"]))
            detail = item.get("detail", "")
            lines.append(f"**{headline}**")
            if detail:
                lines.append(f"{detail}")
            lines.append(f"*{item['author']} · {item['platform']}*\n")

    lines.append(f"---\n{total_raw} 条采集 → {len(items)} 条精选")
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

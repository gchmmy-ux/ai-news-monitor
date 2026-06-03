from config import (
    YOUTUBE_CHANNELS, BILIBILI_UP_HOSTS,
    DOUYIN_BLOGGERS, TWITTER_ACCOUNTS,
    YOUTUBE_SEARCH_KEYWORDS, DOUYIN_SEARCH_KEYWORDS,
    NEGATIVE_KEYWORDS,
)
from collectors.youtube import collect as youtube_collect, search_collect as youtube_search
from collectors.bilibili import collect as bilibili_collect
from collectors.douyin import collect as douyin_collect, search_collect as douyin_search
from collectors.twitter import collect as twitter_collect
from analyzer import analyze
from publisher import publish


def _deduplicate(items):
    seen = set()
    result = []
    for item in items:
        key = item.get("link", "")
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def main():
    print("=" * 50)
    print("AI 资讯监控 · 开始采集")
    print("=" * 50)

    all_items = []

    print("\n[1/7] YouTube 关键词搜索...")
    all_items += youtube_search(YOUTUBE_SEARCH_KEYWORDS, NEGATIVE_KEYWORDS)

    print("\n[2/7] 抖音关键词搜索...")
    all_items += douyin_search(DOUYIN_SEARCH_KEYWORDS, NEGATIVE_KEYWORDS)

    print("\n[3/7] YouTube 频道订阅...")
    all_items += youtube_collect(YOUTUBE_CHANNELS)

    print("\n[4/7] B站 UP主...")
    all_items += bilibili_collect(BILIBILI_UP_HOSTS)

    print("\n[5/7] 抖音博主...")
    all_items += douyin_collect(DOUYIN_BLOGGERS)

    print("\n[6/7] Twitter...")
    all_items += twitter_collect(TWITTER_ACCOUNTS)

    all_items = _deduplicate(all_items)
    print(f"\n采集完成: {len(all_items)} 条（去重后）")

    if not all_items:
        print("今日无新内容，流程结束")
        return

    print("\n[7/7] Gemini 分析中...")
    scored_items = analyze(all_items)
    print(f"\n分析完成: {len(scored_items)}/{len(all_items)} 条通过筛选")

    print("\n生成日报并推送...")
    publish(scored_items, len(all_items))

    print("\n" + "=" * 50)
    print("流程完成")
    print("=" * 50)


if __name__ == "__main__":
    main()

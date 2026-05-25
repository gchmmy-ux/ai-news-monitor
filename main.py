from config import (
    YOUTUBE_CHANNELS, BILIBILI_UP_HOSTS,
    DOUYIN_BLOGGERS, TWITTER_ACCOUNTS,
)
from collectors.youtube import collect as youtube_collect
from collectors.bilibili import collect as bilibili_collect
from collectors.douyin import collect as douyin_collect
from collectors.twitter import collect as twitter_collect
from analyzer import analyze
from publisher import publish


def main():
    print("=" * 50)
    print("AI 资讯监控 · 开始采集")
    print("=" * 50)

    all_items = []

    print("\n[1/6] 采集 YouTube 内容...")
    all_items += youtube_collect(YOUTUBE_CHANNELS)

    print("\n[2/6] 采集 B站 内容...")
    all_items += bilibili_collect(BILIBILI_UP_HOSTS)

    print("\n[3/6] 采集 抖音 内容...")
    all_items += douyin_collect(DOUYIN_BLOGGERS)

    print("\n[4/6] 采集 Twitter 内容...")
    all_items += twitter_collect(TWITTER_ACCOUNTS)

    print(f"\n采集完成: {len(all_items)} 条原始内容")

    if not all_items:
        print("今日无新内容，流程结束")
        return

    print("\n[5/6] Gemini 分析中...")
    scored_items = analyze(all_items)
    print(f"\n分析完成: {len(scored_items)}/{len(all_items)} 条通过筛选")

    print("\n[6/6] 生成日报并推送...")
    publish(scored_items, len(all_items))

    print("\n" + "=" * 50)
    print("流程完成")
    print("=" * 50)


if __name__ == "__main__":
    main()

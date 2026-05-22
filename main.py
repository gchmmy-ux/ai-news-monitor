from config import YOUTUBE_CHANNELS, BILIBILI_UP_HOSTS
from collectors.youtube import collect as youtube_collect
from collectors.bilibili import collect as bilibili_collect
from analyzer import analyze
from publisher import publish


def main():
    print("=" * 50)
    print("AI 资讯监控 · 开始采集")
    print("=" * 50)

    all_items = []

    print("\n[1/4] 采集 YouTube 内容...")
    all_items += youtube_collect(YOUTUBE_CHANNELS)

    print("\n[2/4] 采集 B站 内容...")
    all_items += bilibili_collect(BILIBILI_UP_HOSTS)

    print(f"\n采集完成: {len(all_items)} 条原始内容")

    if not all_items:
        print("今日无新内容，流程结束")
        return

    print("\n[3/4] Gemini 分析中...")
    scored_items = analyze(all_items)
    print(f"\n分析完成: {len(scored_items)}/{len(all_items)} 条通过筛选")

    print("\n[4/4] 生成日报并推送...")
    publish(scored_items, len(all_items))

    print("\n" + "=" * 50)
    print("流程完成")
    print("=" * 50)


if __name__ == "__main__":
    main()

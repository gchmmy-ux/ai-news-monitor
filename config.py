import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SERVER_CHAN_KEY = os.environ.get("SERVER_CHAN_KEY", "")

SCORE_THRESHOLD = 6

YOUTUBE_CHANNELS = [
    {"name": "Matt Wolfe", "handle": "mreflow"},
    {"name": "OpenAI", "handle": "OpenAI"},
    {"name": "Google DeepMind", "handle": "googledeepmind"},
    {"name": "Dwarkesh Podcast", "handle": "DwarkeshPatel"},
    {"name": "Andrej Karpathy", "handle": "AndrejKarpathy"},
    {"name": "Two Minute Papers", "handle": "TwoMinutePapers"},
]

SCORE_PROMPT = """你是 AI 行业资讯分析师。对以下内容打分（1-10），判断其对 AI 行业从业者的价值。

打分标准：
- 8-10 分：产品发布、API 重大变化、行业格局变化
- 7-9 分：AI 工具实操教程、企业 AI 落地方法论、具体案例
- 6-8 分：技术突破、研究论文、新模型发布
- 5-7 分：产品小更新、工具推荐
- 1-3 分：纯观点、感想、无新信息
- 0 分：广告、转发无评论

严格按以下 JSON 格式输出，不要输出其他内容：
{{"score": 数字, "reason": "一句话理由"}}

内容标题：{title}
内容来源：{author} · YouTube

内容正文（字幕摘录，最多 3000 字）：
{content}"""

SUMMARY_PROMPT = """你是 AI 行业资讯编辑。为以下内容生成中文摘要，包含三层信息：

1. 什么事——发生了什么（一句话标题）
2. 具体内容——更新了什么功能、有什么变化（1-2 句细节）
3. 行业位置——这件事在行业中意味着什么、影响什么格局（1 句定位）

同时判断分类（只选一个）：
- breaking: 重大发布（产品发布、API 重大变化）
- update: 产品更新（功能更新、版本升级）
- trend: 行业动向（技术突破、格局变化、投融资）
- practice: 实操与落地（AI 工具教程、企业落地方法论、具体案例）

严格按以下 JSON 格式输出，不要输出其他内容：
{{"category": "分类英文key", "summary": "完整摘要文本（3-5句话）"}}

内容标题：{title}
内容来源：{author} · YouTube

内容正文（字幕摘录，最多 3000 字）：
{content}"""

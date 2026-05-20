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

SUMMARY_PROMPT = """你是 AI 行业资讯编辑。为以下内容生成极简中文摘要，供手机快速浏览。

输出两部分：
1. headline：一句话说清什么事（10-20字，不要"发布了""推出了"等废话动词，直接说核心）
2. detail：一句话补充关键信息，不超过 30 字。其中关键数字、产品名、必知信息用 **加粗** 标记（如：速度提升 **3倍**、支持 **100+语言**、售价 **$20/月**）

分类（只选一个）：
- breaking: 重大发布
- update: 产品更新
- trend: 行业动向
- practice: 实操与落地

严格按 JSON 输出，不要输出其他内容：
{{"category": "分类key", "headline": "标题", "detail": "含加粗标记的一句话要点"}}

内容标题：{title}
内容来源：{author} · YouTube

内容正文（最多 3000 字）：
{content}"""

import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SERVER_CHAN_KEY = os.environ.get("SERVER_CHAN_KEY", "")
BILIBILI_SESSDATA = os.environ.get("BILIBILI_SESSDATA", "")

SCORE_THRESHOLD = 6

YOUTUBE_CHANNELS = [
    {"name": "Matt Wolfe", "handle": "mreflow"},
    {"name": "OpenAI", "handle": "OpenAI"},
    {"name": "Google DeepMind", "handle": "googledeepmind"},
    {"name": "Dwarkesh Podcast", "handle": "DwarkeshPatel"},
    {"name": "Andrej Karpathy", "handle": "AndrejKarpathy"},
    {"name": "Two Minute Papers", "handle": "TwoMinutePapers"},
]

BILIBILI_UP_HOSTS = [
    {"name": "code秘密花园", "uid": 474921808},
    {"name": "程序员鱼皮", "uid": 12890453},
    {"name": "ai798Lab", "uid": 2094023919},
    {"name": "圣徒城的小诺", "uid": 150452545},
]

ANALYZE_PROMPT = """你是 AI 行业资讯分析师。对以下内容打分并生成摘要。

打分标准（1-10）：
- 8-10 分：产品发布、API 重大变化、行业格局变化
- 7-9 分：AI 工具实操教程、企业 AI 落地方法论、具体案例
- 6-8 分：技术突破、研究论文、新模型发布
- 5-7 分：产品小更新、工具推荐
- 1-3 分：纯观点、感想、无新信息
- 0 分：广告、转发无评论

摘要要求（仅 score >= 6 时需要填写，否则留空字符串）：
- category：breaking（重大发布）/ update（产品更新）/ trend（行业动向）/ practice（实操与落地）
- headline：一句话说清什么事（10-20字，直接说核心）
- detail：一句话补充关键信息，不超过 30 字，关键数字和产品名用 **加粗**

严格按 JSON 输出，不要输出其他内容：
{{"score": 数字, "reason": "一句话理由", "category": "", "headline": "", "detail": ""}}

内容标题：{title}
内容来源：{author} · {platform}

内容正文（最多 3000 字）：
{content}"""

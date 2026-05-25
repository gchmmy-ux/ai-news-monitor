import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SERVER_CHAN_KEY = os.environ.get("SERVER_CHAN_KEY", "")
BILIBILI_SESSDATA = os.environ.get("BILIBILI_SESSDATA", "")
DOUYIN_COOKIE = os.environ.get("DOUYIN_COOKIE", "")

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

DOUYIN_BLOGGERS = [
    {"name": "秋芝2046", "sec_uid": "MS4wLjABAAAAwbbVuf1W2DdgRe0xCa0oxg1ZIHbzuiTzyjq3NcOVgBuu6qIidYlMYqbL3ZFY2swu"},
    {"name": "量子位", "sec_uid": "MS4wLjABAAAA1bL6-89P1h_ODlkg17TXKneHuPfHijf8ogsmg6gPVAQ"},
    {"name": "差评君", "sec_uid": "MS4wLjABAAAAoioyA1wed-aUyuGnSSbUEcjLerCyVtbSCvAxym9ZOWUTEPEdaPbHUlNI4dHOhdMU"},
    {"name": "林亦LYi", "sec_uid": "MS4wLjABAAAAtSFk_pO6mcT_31WOWK60mRDvh_0Op6UvYT9dm77bCT20dADpgjU8ccRfj-VgY-qU"},
]

ANALYZE_PROMPT = """你是 AI 行业资讯编辑。读者是企业老板，不是程序员——用大白话写摘要，像跟朋友聊天一样说清楚发生了什么。

打分标准（1-10）：
- 8-10 分：大公司发新产品、行业格局变了
- 7-9 分：AI 工具怎么用的教程、企业怎么用 AI 的案例
- 6-8 分：新技术突破、新模型发布
- 5-7 分：产品小更新、工具推荐
- 1-3 分：纯观点、感想、没有新信息
- 0 分：广告

摘要要求（仅 score >= 6 时需要填写，否则留空字符串）：
- category：breaking（重大发布）/ update（产品更新）/ trend（行业动向）/ practice（实操与落地）
- headline：用大白话说清什么事（10-20字）。不要翻译英文标题，要说「所以怎么了」。例如不说「OpenAI 发布 Codex Goals」，而说「OpenAI 的 AI 编程助手现在能干更复杂的活了」
- detail：补充一句「为什么值得关注」或「具体能干嘛」，不超过 30 字，产品名用 **加粗**

严格按 JSON 输出，不要输出其他内容：
{{"score": 数字, "reason": "一句话理由", "category": "", "headline": "", "detail": ""}}

内容标题：{title}
内容来源：{author} · {platform}

内容正文（最多 3000 字）：
{content}"""

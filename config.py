import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SERVER_CHAN_KEY = os.environ.get("SERVER_CHAN_KEY", "")
BILIBILI_SESSDATA = os.environ.get("BILIBILI_SESSDATA", "")
DOUYIN_COOKIE = os.environ.get("DOUYIN_COOKIE", "")
TWITTER_COOKIE = os.environ.get("TWITTER_COOKIE", "")

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

TWITTER_ACCOUNTS = [
    {"name": "OpenAI", "handle": "OpenAI"},
    {"name": "Anthropic", "handle": "AnthropicAI"},
    {"name": "Google DeepMind", "handle": "GoogleDeepMind"},
    {"name": "Andrej Karpathy", "handle": "karpathy"},
    {"name": "Sam Altman", "handle": "sama"},
    {"name": "Ethan Mollick", "handle": "emollick"},
    {"name": "DAIR.AI", "handle": "DAIR_AI"},
]

ANALYZE_PROMPT = """你是 AI 行业资讯编辑。读者是企业老板，不是程序员。

打分标准（1-10）：
- 8-10 分：大公司发新产品、行业格局变了
- 7-9 分：AI 工具怎么用的教程、企业怎么用 AI 的案例
- 6-8 分：新技术突破、新模型发布
- 5-7 分：产品小更新、工具推荐
- 1-3 分：纯观点、感想、没有新信息
- 0 分：广告

摘要要求（仅 score >= 6 时需要填写，否则留空字符串）：
- summary：一句话说清「谁做了什么 + 为什么值得知道」，30-60 字
- 必须包含具体信息：产品名、功能名、数字、变化点。禁止模糊表述（如「据说能带来大变化」「引发关注」「值得关注」）
- 如果原文本身就没有具体信息，照实写「细节未公布」，不要编造

反面示例（禁止）：「DeepSeek又出新AI了，据说能带来大变化」「谷歌AI产品更新引争议，老板们需关注」
正面示例（学习）：「OpenAI Codex 新增预览截图和共享插件，企业编程助手基本成型」「DeepSeek 发布 V3 模型，数学推理跑分超过 GPT-4o」

严格按 JSON 输出，不要输出其他内容：
{{"score": 数字, "reason": "一句话理由", "summary": ""}}

内容标题：{title}
内容来源：{author} · {platform}

内容正文（最多 3000 字）：
{content}"""

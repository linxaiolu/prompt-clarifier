import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# 需求类型的关键词规则。第一版先用简单规则，方便新手理解和修改。
CATEGORY_KEYWORDS = {
    "学习规划类": ["学习", "课程", "考试", "复习", "自学", "计划", "规划", "入门", "提升"],
    "求职简历类": ["简历", "求职", "面试", "岗位", "实习", "工作", "招聘", "应聘"],
    "项目规划类": ["项目", "作品", "系统", "网站", "工具", "应用", "开发", "毕业设计", "比赛"],
    "写作表达类": ["写", "文案", "文章", "邮件", "演讲", "汇报", "表达", "润色", "标题"],
    "资料整理类": ["整理", "总结", "资料", "笔记", "归纳", "提取", "表格", "分类"],
    "问题解决类": ["问题", "报错", "不会", "失败", "解决", "怎么办", "原因", "修复"],
}


# 每类需求对应的问题库。每个问题都是选择题，前端会渲染成单选按钮。
QUESTION_BANK = {
    "学习规划类": [
        {
            "id": "goal",
            "question": "你的学习目标是什么？",
            "options": ["零基础入门", "通过考试", "完成课程作业", "提升实战能力", "准备求职"],
        },
        {
            "id": "level",
            "question": "你现在的基础如何？",
            "options": ["几乎零基础", "了解一点概念", "学过但不系统", "有一定实践经验"],
        },
        {
            "id": "time",
            "question": "你希望用多长时间完成？",
            "options": ["1周以内", "2到4周", "1到3个月", "3个月以上"],
        },
        {
            "id": "style",
            "question": "你更喜欢哪种学习方式？",
            "options": ["先讲概念", "边学边做", "项目驱动", "刷题巩固"],
        },
    ],
    "求职简历类": [
        {
            "id": "purpose",
            "question": "你这次主要想解决什么？",
            "options": ["优化简历", "准备面试", "提炼项目经历", "匹配目标岗位"],
        },
        {
            "id": "role",
            "question": "你的目标岗位更接近哪一类？",
            "options": ["AI算法", "数据分析", "后端开发", "前端开发", "产品/运营"],
        },
        {
            "id": "experience",
            "question": "你的经历目前更偏向哪种？",
            "options": ["学校课程", "实习经历", "个人项目", "比赛/科研", "暂时较少"],
        },
        {
            "id": "output",
            "question": "你希望 AI 最终输出什么？",
            "options": ["简历项目描述", "简历整体修改建议", "面试问答", "岗位匹配分析"],
        },
    ],
    "项目规划类": [
        {
            "id": "purpose",
            "question": "你做这个项目的主要目的是什么？",
            "options": ["写进简历", "毕业设计", "学习练手", "参加比赛"],
        },
        {
            "id": "direction",
            "question": "你希望项目偏向什么方向？",
            "options": ["医学影像", "AI办公", "数据分析", "聊天机器人", "网页工具"],
        },
        {
            "id": "level",
            "question": "你的技术基础如何？",
            "options": ["几乎零基础", "会一点 Python", "会简单网页", "有完整项目经验"],
        },
        {
            "id": "difficulty",
            "question": "你希望项目难度如何？",
            "options": ["尽量简单", "难度适中", "有一点挑战", "偏完整商业项目"],
        },
        {
            "id": "deliverable",
            "question": "你最希望得到哪种成果？",
            "options": ["项目方案", "代码实现步骤", "简历写法", "GitHub README", "完整项目规划"],
        },
    ],
    "写作表达类": [
        {
            "id": "type",
            "question": "你要写的内容属于哪一类？",
            "options": ["文章", "邮件", "汇报稿", "短视频文案", "演讲稿"],
        },
        {
            "id": "tone",
            "question": "你希望语气风格是什么？",
            "options": ["正式专业", "自然口语", "简洁直接", "有感染力", "温和礼貌"],
        },
        {
            "id": "audience",
            "question": "主要读者是谁？",
            "options": ["老师/导师", "同学朋友", "公司同事", "面试官", "普通大众"],
        },
        {
            "id": "length",
            "question": "你希望内容长度如何？",
            "options": ["很短", "适中", "详细", "分点说明"],
        },
    ],
    "资料整理类": [
        {
            "id": "source",
            "question": "你要整理的资料主要是什么？",
            "options": ["课堂笔记", "论文/文章", "会议记录", "网页资料", "项目资料"],
        },
        {
            "id": "format",
            "question": "你希望整理成什么形式？",
            "options": ["要点总结", "表格", "思维导图大纲", "分类清单", "复习笔记"],
        },
        {
            "id": "focus",
            "question": "整理时最需要突出什么？",
            "options": ["核心概念", "关键步骤", "结论观点", "待办事项", "易错点"],
        },
        {
            "id": "detail",
            "question": "你希望详细程度如何？",
            "options": ["只保留重点", "适中", "尽量详细", "适合考试复习"],
        },
    ],
    "问题解决类": [
        {
            "id": "problem_type",
            "question": "你遇到的问题更像哪一类？",
            "options": ["代码报错", "学习卡住", "工具不会用", "方案不知道怎么选", "结果不符合预期"],
        },
        {
            "id": "urgency",
            "question": "这个问题的紧急程度如何？",
            "options": ["现在就要解决", "今天内解决", "可以慢慢排查", "只是想理解原因"],
        },
        {
            "id": "info",
            "question": "你能提供的信息有多少？",
            "options": ["只有现象", "有报错信息", "有代码/截图", "已经尝试过一些方法"],
        },
        {
            "id": "output",
            "question": "你希望 AI 怎么帮助你？",
            "options": ["一步步排查", "直接给解决方案", "解释原因", "给多个可选方案"],
        },
    ],
}


TEMPLATE_INTROS = {
    "学习规划类": "请你作为一名学习规划助手，帮我把下面的学习需求拆成可执行计划。",
    "求职简历类": "请你作为一名求职简历顾问，帮我优化下面的求职相关需求。",
    "项目规划类": "请你作为一名项目规划导师，帮我设计一个适合执行和展示的项目方案。",
    "写作表达类": "请你作为一名写作表达助手，帮我完成下面的写作任务。",
    "资料整理类": "请你作为一名资料整理助手，帮我把资料整理得清晰、结构化。",
    "问题解决类": "请你作为一名问题排查助手，帮我一步步分析并解决下面的问题。",
}


def classify_requirement(text):
    """根据关键词给需求分类。如果多个类别命中，选择命中次数最多的类别。"""
    # “做项目写进简历”这类需求虽然提到简历，但用户真正要的是项目方案。
    if "项目" in text and any(word in text for word in ["做", "开发", "方案", "作品", "系统", "工具"]):
        return "项目规划类"

    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for keyword in keywords if keyword in text)

    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "问题解决类"
    return best_category


def build_prompt_input(requirement, category, answers):
    """把用户的原始需求和选择结果整理成 AI 或本地模板都能使用的输入。"""
    answer_lines = []
    for item in answers:
        question = item.get("question", "")
        answer = item.get("answer", "")
        if question and answer:
            answer_lines.append(f"- {question}：{answer}")

    answer_text = "\n".join(answer_lines) if answer_lines else "- 暂无补充选择"
    intro = TEMPLATE_INTROS.get(category, TEMPLATE_INTROS["问题解决类"])

    return f"""{intro}

我的原始需求是：
{requirement}

系统判断这个需求属于：{category}

我补充选择的信息如下：
{answer_text}

请你基于以上信息，生成一段完整、清晰、结构化、适合直接发给 AI 的提示词。
要求：
1. 不要回答这个需求本身，只生成“给 AI 的提示词”；
2. 提示词要包含用户目标、背景、限制条件和期望输出；
3. 语言要自然，适合用户直接复制使用；
4. 如果仍缺少关键信息，请在提示词末尾加入“还需要补充的信息”。"""


def generate_with_local_template(prompt_input):
    """没有配置 API Key 或 API 调用失败时，使用本地模板兜底。"""
    return prompt_input


def generate_with_openai(prompt_input):
    """调用真实 OpenAI API 生成更自然的提示词。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "未配置 OPENAI_API_KEY，已使用本地模板生成。"

    try:
        from openai import OpenAI
    except ImportError:
        return None, "未安装 openai 依赖，已使用本地模板生成。"

    model = os.getenv("OPENAI_MODEL", "gpt-5.5")
    client = OpenAI(api_key=api_key, timeout=30)

    response = client.responses.create(
        model=model,
        instructions=(
            "你是 Prompt Clarifier 的提示词优化引擎。"
            "你的任务是把用户的模糊需求和补充选择整理成一段可直接发给 AI 的中文提示词。"
            "只输出提示词正文，不要输出解释。"
        ),
        input=prompt_input,
        max_output_tokens=900,
    )

    return response.output_text.strip(), None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/clarify", methods=["POST"])
def clarify():
    data = request.get_json() or {}
    requirement = (data.get("requirement") or "").strip()

    if not requirement:
        return jsonify({"error": "请输入你的需求。"}), 400

    category = classify_requirement(requirement)
    questions = QUESTION_BANK[category][:8]

    return jsonify(
        {
            "category": category,
            "questions": questions,
        }
    )


@app.route("/api/generate", methods=["POST"])
def generate_prompt():
    data = request.get_json() or {}
    requirement = (data.get("requirement") or "").strip()
    category = data.get("category") or classify_requirement(requirement)
    answers = data.get("answers") or []

    if not requirement:
        return jsonify({"error": "缺少原始需求。"}), 400

    prompt_input = build_prompt_input(requirement, category, answers)

    try:
        ai_prompt, warning = generate_with_openai(prompt_input)
    except Exception as error:
        ai_prompt = None
        warning = f"AI API 调用失败，已使用本地模板生成。原因：{error}"

    if ai_prompt:
        return jsonify(
            {
                "prompt": ai_prompt,
                "source": "真实 AI API",
                "model": os.getenv("OPENAI_MODEL", "gpt-5.5"),
                "warning": "",
            }
        )

    return jsonify(
        {
            "prompt": generate_with_local_template(prompt_input),
            "source": "本地模板",
            "model": "",
            "warning": warning,
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)

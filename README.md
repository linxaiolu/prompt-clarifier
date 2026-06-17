# Prompt Clarifier：AI需求澄清助手

Prompt Clarifier 是一个基于 Flask 的 AI 需求澄清工具。它可以把用户的一句模糊想法，转化为一段结构化、清晰、适合直接发给 AI 的提示词。

项目适合 Python / Flask 初学者学习，也适合作为 AI 工具类简历项目展示。

![Prompt Clarifier 首页](docs/images/home.png)

## 项目亮点

- 支持 6 类常见需求：学习规划、求职简历、项目规划、写作表达、资料整理、问题解决
- 使用本地关键词规则自动判断需求类型
- 根据需求类型生成 3 到 8 个选择题
- 根据用户选择生成结构化 AI 提示词
- 支持接入真实 OpenAI API
- 未配置 API Key 时自动回退到本地模板，方便新手直接运行
- 前后端分离思路清晰，适合作为入门项目阅读和二次开发

## 使用流程

1. 用户输入一段模糊需求
2. 系统自动判断需求类型
3. 系统生成选择题帮助用户补充信息
4. 用户完成选择
5. 系统生成完整提示词
6. 用户一键复制并发送给 AI

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端 | Python、Flask |
| 前端 | HTML、CSS、JavaScript |
| AI 能力 | OpenAI Responses API |
| 生产部署 | Gunicorn、Render / Railway |
| 兜底方案 | 本地规则、问题库、提示词模板 |

## 项目结构

```text
prompt-clarifier/
├── app.py
├── Procfile
├── render.yaml
├── requirements.txt
├── DEPLOYMENT.md
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── docs/
    └── images/
        └── home.png
```

## 本地运行

进入项目目录：

```bash
cd prompt-clarifier
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动项目：

```bash
python app.py
```

浏览器打开：

```text
http://127.0.0.1:5000
```

## 配置 OpenAI API

项目默认从环境变量 `OPENAI_API_KEY` 读取 API Key。不要把 API Key 写进代码，也不要上传到 GitHub。

Windows PowerShell：

```powershell
setx OPENAI_API_KEY "你的 API Key"
setx OPENAI_MODEL "gpt-5.5"
```

重新打开 PowerShell 后启动项目：

```powershell
python app.py
```

如果不配置 `OPENAI_API_KEY`，项目仍然可以运行，只是会使用本地模板生成结果。

## API 接口

### 需求澄清

```text
POST /api/clarify
```

请求示例：

```json
{
  "requirement": "我想做一个能写进简历的AI项目，但是不知道做什么。"
}
```

返回内容：

```json
{
  "category": "项目规划类",
  "questions": []
}
```

### 生成提示词

```text
POST /api/generate
```

根据原始需求、需求类型和选择题答案，生成完整提示词。

## 线上部署

项目已准备好 Render / Railway 部署配置。

Render 推荐配置：

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

环境变量：

```text
OPENAI_API_KEY=你的 API Key
OPENAI_MODEL=gpt-5.5
```

详细步骤见 [DEPLOYMENT.md](DEPLOYMENT.md)。

## 适合展示的简历描述

```text
Prompt Clarifier：AI需求澄清助手
基于 Flask + HTML/CSS/JavaScript 开发的 AI 工具类项目。系统通过关键词规则识别用户需求类型，动态生成选择题收集补充信息，并结合 OpenAI API 或本地模板生成结构化提示词。项目实现了完整的前后端交互、API 接口设计、规则分类、模板生成和线上部署配置。
```

## 后续计划

- 让 AI 同时负责需求分类和问题生成
- 增加历史记录功能
- 支持导出 Markdown / Word
- 支持用户自定义问题库
- 增加更多展示截图
- 增加登录和个人提示词收藏

## License

MIT

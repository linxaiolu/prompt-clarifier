# Prompt Clarifier 线上部署说明

这份说明适合把项目部署到 Render、Railway 等支持 Python Web 服务的平台。

## 部署前准备

请先把项目上传到 GitHub。

推荐仓库结构保持为：

```text
prompt-clarifier/
├── app.py
├── Procfile
├── render.yaml
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## 方案一：部署到 Render

1. 打开 Render 官网：

```text
https://render.com
```

2. 注册或登录账号。

3. 点击 `New +`，选择 `Web Service`。

4. 连接你的 GitHub 仓库。

5. 选择这个项目仓库。

6. 配置参数：

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

7. 在环境变量里添加：

```text
OPENAI_API_KEY=你的 API Key
OPENAI_MODEL=gpt-5.5
```

如果暂时没有 API Key，也可以不配置 `OPENAI_API_KEY`，项目会自动回退到本地模板。

8. 点击部署。

部署完成后，Render 会给你一个线上访问地址，例如：

```text
https://prompt-clarifier.onrender.com
```

## 方案二：部署到 Railway

1. 打开 Railway：

```text
https://railway.app
```

2. 登录后选择 `New Project`。

3. 选择 `Deploy from GitHub repo`。

4. 选择你的项目仓库。

5. Railway 会自动识别 Python 项目。

6. 在 Variables 里添加：

```text
OPENAI_API_KEY=你的 API Key
OPENAI_MODEL=gpt-5.5
```

7. 如果需要手动设置启动命令，填写：

```text
gunicorn app:app
```

## 重要注意事项

- 不要把 `OPENAI_API_KEY` 写进代码。
- 不要把 `.env` 上传到 GitHub。
- 线上平台通常会自动设置 `PORT`，代码已经支持读取这个端口。
- 本地开发仍然可以使用：

```bash
python app.py
```

## 常见问题

### 1. 页面能打开，但是 AI 不工作

检查平台环境变量里是否设置了：

```text
OPENAI_API_KEY
```

### 2. 部署后提示应用启动失败

检查启动命令是否是：

```text
gunicorn app:app
```

### 3. 本地运行没问题，线上运行失败

优先检查：

- `requirements.txt` 是否包含 Flask、openai、gunicorn
- 平台是否正确选择 Python 环境
- 环境变量是否配置正确
- 日志里是否有 Python 报错

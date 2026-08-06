# CandleLight 博客部署指南

## Render 部署步骤

### 1. 准备工作
- 注册 [Render](https://render.com) 账号
- 将代码推送到 GitHub

### 2. 方式一：使用 render.yaml 一键部署
1. 登录 Render Dashboard
2. 点击 **New** → **Blueprint**
3. 连接你的 GitHub 仓库
4. Render 会自动读取 `render.yaml` 并创建 Web Service + PostgreSQL Database

### 3. 方式二：手动部署
1. **创建 PostgreSQL 数据库**：
   - New → PostgreSQL
   - Name: `candlelight_db`
   - Plan: Free
   - 创建后复制 **Internal Database URL**

2. **创建 Web Service**：
   - New → Web Service
   - 连接 GitHub 仓库
   - Runtime: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn my_blog.wsgi:application --bind 0.0.0.0:$PORT`

3. **配置环境变量**：
   - `DATABASE_URL`：粘贴刚才复制的数据库 URL
   - `SECRET_KEY`：使用 `python -c "import secrets; print(secrets.token_urlsafe(50))"` 生成
   - `DEBUG`：设为 `False`
   - `PYTHON_VERSION`：3.11.9

### 4. 部署后操作
- 首次部署后会自动执行迁移
- 如需创建超级用户：进入 Shell 运行 `python manage.py createsuperuser`
- 媒体文件（用户上传的头像/图片）：建议配置 AWS S3 或 Cloudflare R2

## 本地开发
```bash
# 激活虚拟环境
source myenv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env

# 数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

## 注意事项
- 媒体文件不会持久化在 Render 免费层（磁盘是临时的），生产环境建议使用 S3
- 免费层服务会在 15 分钟无活动后休眠，再次访问会延迟约 30 秒唤醒
- 每月 750 小时免费额度

## 文件清单
- `build.sh` - 部署构建脚本
- `Procfile` - 进程定义
- `runtime.txt` - Python 版本
- `requirements.txt` - Python 依赖
- `render.yaml` - Render 平台配置（基础设施即代码）
- `.env.example` - 环境变量示例
- `.gitignore` - Git 忽略文件

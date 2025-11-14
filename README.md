# indextts
基于 indextts2 模型的文案转语音平台，采用前后端分离架构：
- 前端：Angular（位于 `frontend/`），负责脚本编辑、音色管理、任务进度展示等交互。
- 后端：FastAPI（位于 `backend/`），封装 indextts2 推理、Celery 任务调度及 REST/WebSocket API。

## 快速开始
1. **前端**
   ```bash
   cd frontend
   npm install
   npm start
   ```
2. **后端**
   ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
   ```
   运行前可先 `cp .env.example .env` 并根据需要修改 `DATABASE_URL`、Redis 等连接配置。

## Docker 启动
```bash
cp backend/.env.example backend/.env   # 首次运行
docker compose build
docker compose up -d
```
容器启动后访问：
- 前端：<http://localhost:4200>
- 后端接口/Swagger：<http://localhost:8000/docs>
- PostgreSQL：`localhost:5432`（默认用户/密码 `indextts/indextts`）

更多说明见 `docs/requirements.md` 与 `docs/docker.md`。

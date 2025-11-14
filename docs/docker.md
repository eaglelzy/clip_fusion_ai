# Docker 部署

## 前置条件
- 安装 Docker 与 Docker Compose（v2 以上）。
- 首次运行前复制后端环境变量：`cp backend/.env.example backend/.env`，根据实际 Redis/Celery/数据库配置修改。

## 快速启动
```bash
docker compose build
docker compose up -d
```

启动后：
- 前端可通过 <http://localhost:4200> 访问。
- 后端 FastAPI/Swagger 位于 <http://localhost:8000/docs>。
- PostgreSQL 暴露在 `localhost:5432`（默认账号/密码 `indextts/indextts`）。
- Redis 默认暴露在 `localhost:6379`，供后台任务与调试使用。

## 组件说明
- `frontend`：基于 nginx 的静态站点，镜像在构建阶段运行 `npm ci && npm run build`。
- `backend`：运行 `uvicorn app.main:app`，加载 `.env` 配置，默认连接 docker 内的 PostgreSQL 与 Redis。
- `worker`：与 backend 复用镜像，执行 `celery -A app.workers.tasks.celery_app worker`，用于异步合成任务。
- `db`：PostgreSQL 15，初始化数据库/用户均为 `indextts`，数据存储在 `db_data` 卷中。
- `redis`：存放 Celery 队列与结果；可替换为外部 Redis，修改 `.env` 与 `docker-compose.yml` 即可。

## 常用命令
- 查看日志：`docker compose logs -f backend`、`docker compose logs -f worker`
- 重新构建：`docker compose build frontend backend`（前端/后端代码有更新时）
- 停止服务：`docker compose down`

# 中间件健康巡检 Agent

基于 LangChain + DeepSeek 的中间件智能巡检助手。自动巡检 Redis、MySQL、Nginx，输出健康状态、风险项与调优建议。

## 项目背景

传统中间件巡检需要人工逐台登录服务器，敲 `redis-cli info`、`show status`、`nginx -t` 等命令，效率低且容易遗漏。本项目利用 AI Agent 实现自动化巡检，Agent 会自动决定巡检顺序、调用工具收集指标、结合最佳实践给出调优建议。

## 功能特性

- ReAct Agent 自动决定巡检顺序（先查哪个中间件）
- 三大巡检工具：Redis / MySQL / Nginx
- 自动生成结构化的巡检报告：健康状态 + 风险项 + 调优建议
- 支持扩展新工具（Kafka、Elasticsearch 等）

## 架构
```
用户输入
↓
ReAct Agent (LangChain + DeepSeek)
↓ 自动决策
├── redis_health_check()
├── mysql_health_check()
└── nginx_health_check()
↓
巡检报告
```

## 技术栈

- **Agent 框架**：LangChain (`create_agent`)
- **大模型**：DeepSeek API
- **中间件**：Redis 7 / MySQL 8 / Nginx (Alpine)
- **容器化**：Docker + Docker Compose
- **云服务器**：腾讯云轻量应用服务器 (Ubuntu 22.04 LTS)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cb-Lobster/middleware-inspector.git
cd middleware-inspector
```
### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 启动中间件测试环境
```bash
docker compose up -d
docker ps  # 确认 test-redis / test-mysql / test-nginx 都在 Up 状态
```

### 4. 配置环境变量
```bash
cp .env.example .env
vim .env  # 填入你的 DeepSeek API Key
```
.env内容
```bash
DEEPSEEK_API_KEY=sk-你的key
DEEPSEEK_BASE_URL=https://api.deepseek.com
MYSQL_PASSWORD=test123
NGINX_URL=http://localhost:8080
```

### 5. 运行 Agent
```bash
python -m agent.main
```
输入：
```bash
帮我巡检所有中间件
```
## 项目结构
```
middleware-inspector/
├── agent/
│   ├── main.py              # Agent 入口
│   └── tools/
│       ├── redis_tool.py    # Redis 巡检工具
│       ├── mysql_tool.py    # MySQL 巡检工具
│       └── nginx_tool.py    # Nginx 巡检工具
├── tests/                   # 独立测试脚本
├── docker-compose.yml       # 中间件测试环境
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量模板
└── README.md
```
## 示例输出
巡检报告：

## 健康状态总结
| 组件  | 状态 | 关键指标 |
|-------|------|---------|
| Redis | ✅ 正常 | 内存 1.13M / 连接 1 / 慢查询 0 |
| MySQL | ✅ 正常 | 连接 1/151 / 慢查询 0 |
| Nginx | ✅ 正常 | HTTP 200 |

## 风险项
- Nginx 返回默认欢迎页，未配置业务站点

## 调优建议
- MySQL：建议提升 max_connections 至 300-500
- Redis：建议配置 maxmemory + allkeys-lru 策略

## 踩坑记录
Docker 拉取镜像超时：国内服务器拉取 Docker Hub 镜像会超时，配置腾讯云内网镜像源 mirror.ccs.tencentyun.com 解决。
LangChain API 变更：新版 LangChain (v1.0+) 已弃用 create_react_agent，改用 create_agent，调用方式和输出格式也变了。
工具函数 print vs return：Agent 工具必须 return 字符串给 LLM，用 print 会导致 LLM 读不到结果。
Ubuntu Server 无图形界面：云服务器选 Server 版镜像即可，通过 SSH + MobaXterm 操作。

## 后续计划
□ 接入 ChromaDB RAG 知识库，让 Agent 检索最佳实践文档
□ 增加 Kafka / Elasticsearch 巡检工具
□ 接入飞书/钉钉 Webhook，定时推送巡检报告
□ 打包 Docker 镜像，部署到 K8s 集群

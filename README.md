# 小红书内容自动生成与发布 Agent 系统

基于大语言模型的个人内容生成 Agent 系统，实现自动化内容创作流程。

## 功能模块

1. **信息采集模块** - 定时从指定网站抓取内容（支持 RSS/静态/动态网页）
2. **信息清洗与预处理模块** - 去HTML噪声、文本清洗、去重
3. **热点分析与主题生成模块** - 语义聚类、热点提取、选题生成
4. **小说生成模块** - 根据选题生成短篇小说
5. **内容优化模块** - 标题优化、标签生成、风格调整
6. **发布模块** - 内容格式化与导出
7. **调度系统** - 定时任务管理

## 技术栈

- Python 3.10+
- FastAPI（API服务）
- APScheduler（任务调度）
- Playwright（动态网页采集）
- LangChain（LLM框架）
- OpenAI/Qwen API
- FAISS（向量检索）

## 项目结构

```
xiaohongshu-agent/
├── app/
│   ├── crawler/          # 数据采集
│   ├── processor/        # 数据清洗
│   ├── topic_agent/      # 主题生成
│   ├── writer_agent/     # 小说生成
│   ├── editor_agent/     # 内容优化
│   ├── publisher/        # 发布模块
│   ├── scheduler/        # 定时任务
│   ├── config/           # 配置文件
│   └── main.py           # 启动入口
├── data/                 # 输出数据
├── logs/                 # 日志
├── requirements.txt
└── README.md
```

## 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd xiaohongshu-agent
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 安装 Playwright 浏览器
```bash
playwright install chromium
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置 LLM API Key
```

## 运行方式

### 方式一：运行示例脚本
```bash
python run_example.py
```

### 方式二：启动 API 服务
```bash
python -m uvicorn app.main:app --reload
```

### 方式三：使用定时任务
```bash
python -c "from app.main import scheduler, complete_pipeline; scheduler.add_daily_task(complete_pipeline); scheduler.start(); input('Press Enter to stop...')"
```

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/crawl` | POST | 执行数据爬取 |
| `/topics` | GET | 生成热点选题 |
| `/story` | POST | 根据选题生成故事 |
| `/publish` | POST | 导出发布内容 |
| `/run-pipeline` | POST | 执行完整流程 |
| `/scheduler/start` | POST | 启动调度器 |
| `/scheduler/stop` | POST | 停止调度器 |
| `/scheduler/jobs` | GET | 查看任务列表 |

## 使用示例

```python
from app.crawler import CrawlerManager
from app.topic_agent import TopicAgent
from app.writer_agent import WriterAgent
from app.editor_agent import EditorAgent
from app.publisher import Publisher

# 初始化模块
crawler = CrawlerManager()
topic_agent = TopicAgent()
writer = WriterAgent()
editor = EditorAgent()
publisher = Publisher()

# 添加爬虫
crawler.add_crawler("新浪新闻", "https://news.sina.com.cn/", "html")

# 爬取数据
data = crawler.crawl_all()

# 生成选题
topics = topic_agent.generate_topics(data)

# 生成故事
story = writer.generate_story(topics[0])

# 优化内容
edited = editor.edit_content(story, style="情感")

# 导出发布
publisher.export_content(edited)
```

## 配置说明

### 目标网站配置（app/config/settings.py）
```python
TARGET_WEBSITES = [
    {"name": "网站名称", "url": "网站地址", "type": "html|rss|dynamic"}
]
```

### LLM 配置（.env）
```
LLM_API_KEY=your_api_key
LLM_MODEL=qwen
LLM_BASE_URL=https://api.qwenlm.com/v1
```

## 注意事项

1. 需要配置有效的 LLM API Key 才能使用内容生成功能
2. 首次运行需要安装 Playwright 浏览器
3. 建议设置合理的爬取间隔，避免对目标网站造成压力
4. 生成的内容仅供参考，请根据实际情况进行调整

## 许可证

MIT License

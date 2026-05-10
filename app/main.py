import logging
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

from app.crawler import CrawlerManager
from app.processor import DataCleaner, TextProcessor
from app.topic_agent import TopicAgent
from app.writer_agent import WriterAgent
from app.editor_agent import EditorAgent
from app.publisher import Publisher
from app.scheduler import TaskScheduler
from app.config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{settings.LOG_DIR}/app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="小红书内容生成Agent", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

class CrawlRequest(BaseModel):
    websites: List[Dict[str, str]] = []

class StoryRequest(BaseModel):
    topic: str
    style: str = "情感"

class ProcessResult(BaseModel):
    success: bool
    message: str
    data: Dict = {}

crawler_manager = CrawlerManager()
data_cleaner = DataCleaner()
text_processor = TextProcessor()
topic_agent = TopicAgent()
writer_agent = WriterAgent()
editor_agent = EditorAgent()
publisher = Publisher()
scheduler = TaskScheduler()

def init_crawlers():
    for site in settings.TARGET_WEBSITES:
        crawler = crawler_manager.create_crawler(
            name=site["name"],
            url=site["url"],
            type=site.get("type", "html")
        )
        crawler_manager.add_crawler(crawler)

def complete_pipeline():
    try:
        logger.info("Starting complete content generation pipeline")

        raw_data = crawler_manager.crawl_all()
        if not raw_data:
            logger.warning("No data crawled")
            return

        cleaned_data = data_cleaner.clean_items(raw_data)
        deduplicated_data = data_cleaner.deduplicate(cleaned_data)

        topics = topic_agent.generate_topics(deduplicated_data)
        if not topics:
            logger.warning("No topics generated")
            return

        for topic in topics[:3]:
            story = writer_agent.generate_story(topic)
            edited = editor_agent.edit_content(story, style="情感")
            publisher.export_content(edited)
            publisher.export_json(edited)

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")

init_crawlers()

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/index.html")

@app.post("/crawl", response_model=ProcessResult)
async def crawl(request: CrawlRequest):
    try:
        if request.websites:
            for site in request.websites:
                crawler = crawler_manager.create_crawler(
                    name=site["name"],
                    url=site["url"],
                    type=site.get("type", "html")
                )
                crawler_manager.add_crawler(crawler)

        results = crawler_manager.crawl_all()

        return ProcessResult(
            success=True,
            message=f"爬取完成，共获取 {len(results)} 条数据",
            data={"count": len(results), "items": results[:5]}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topics", response_model=ProcessResult)
async def get_topics(count: int = 5):
    try:
        raw_data = crawler_manager.crawl_all()
        cleaned_data = data_cleaner.clean_items(raw_data)
        deduplicated_data = data_cleaner.deduplicate(cleaned_data)

        topics = topic_agent.generate_topics(deduplicated_data, count=count)

        return ProcessResult(
            success=True,
            message=f"生成 {len(topics)} 个选题",
            data={"topics": topics}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/story", response_model=ProcessResult)
async def generate_story(request: StoryRequest):
    try:
        story = writer_agent.generate_full_story(request.topic, word_count=1000)
        edited = editor_agent.edit_content(story, style=request.style)

        return ProcessResult(
            success=True,
            message="故事生成完成",
            data=edited
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/publish", response_model=ProcessResult)
async def publish(content: Dict):
    try:
        filepath = publisher.export_content(content)

        return ProcessResult(
            success=True,
            message=f"内容已导出",
            data={"filepath": filepath}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-pipeline", response_model=ProcessResult)
async def run_pipeline():
    try:
        complete_pipeline()

        return ProcessResult(
            success=True,
            message="完整流程执行完成"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scheduler/start")
async def start_scheduler():
    try:
        scheduler.add_daily_task(complete_pipeline, hour=9)
        scheduler.start()

        return {"message": "调度器已启动", "jobs": [str(job) for job in scheduler.get_jobs()]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scheduler/stop")
async def stop_scheduler():
    try:
        scheduler.stop()
        return {"message": "调度器已停止"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scheduler/jobs")
async def get_scheduler_jobs():
    jobs = scheduler.get_jobs()
    return {"jobs": [str(job) for job in jobs]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
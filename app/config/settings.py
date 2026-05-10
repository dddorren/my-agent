from pydantic.v1 import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")
    LOG_DIR: str = os.path.join(PROJECT_ROOT, "logs")
    
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "qwen"
    LLM_BASE_URL: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.LLM_API_KEY:
            self.LLM_API_KEY = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    
    SCHEDULE_CRON: str = "0 9 * * *"
    
    STORY_MIN_LENGTH: int = 1000
    STORY_MAX_LENGTH: int = 1200
    TOPIC_COUNT: int = 5
    
    DUPLICATE_THRESHOLD: float = 0.9
    
    CRAWL_TIMEOUT: int = 30
    CRAWL_INTERVAL: int = 5
    
    TARGET_WEBSITES: List[dict] = [
        {
            "name": "新浪新闻",
            "url": "https://news.sina.com.cn/",
            "type": "html"
        },
        {
            "name": "知乎热榜",
            "url": "https://www.zhihu.com/hot",
            "type": "html"
        },
        {
            "name": "网易新闻",
            "url": "https://news.163.com/",
            "type": "html"
        }
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

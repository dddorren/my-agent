from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime

class CrawlerBase(ABC):
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.last_crawl_time = None
    
    @abstractmethod
    def crawl(self) -> List[Dict[str, str]]:
        pass
    
    def get_name(self) -> str:
        return self.name
    
    def get_url(self) -> str:
        return self.url
    
    def set_last_crawl_time(self, time: datetime):
        self.last_crawl_time = time
    
    def get_last_crawl_time(self) -> Optional[datetime]:
        return self.last_crawl_time

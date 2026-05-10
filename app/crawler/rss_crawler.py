import feedparser
from typing import List, Dict
from datetime import datetime
from .base_crawler import CrawlerBase
import logging

logger = logging.getLogger(__name__)

class RSSCrawler(CrawlerBase):
    def crawl(self) -> List[Dict[str, str]]:
        results = []
        try:
            feed = feedparser.parse(self.url)
            
            for entry in feed.entries[:20]:
                item = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", ""),
                    "source": self.name,
                    "crawl_time": datetime.now().isoformat()
                }
                results.append(item)
            
            logger.info(f"RSS Crawler {self.name} fetched {len(results)} items")
            self.set_last_crawl_time(datetime.now())
            
        except Exception as e:
            logger.error(f"RSS Crawler {self.name} failed: {str(e)}")
        
        return results

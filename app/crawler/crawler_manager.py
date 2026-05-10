from typing import List, Dict
from .base_crawler import CrawlerBase
from .rss_crawler import RSSCrawler
from .html_crawler import HTMLCrawler
from .dynamic_crawler import DynamicCrawler
import logging

logger = logging.getLogger(__name__)

class CrawlerManager:
    def __init__(self):
        self.crawlers: List[CrawlerBase] = []
    
    def add_crawler(self, crawler: CrawlerBase):
        self.crawlers.append(crawler)
        logger.info(f"Added crawler: {crawler.get_name()}")
    
    def remove_crawler(self, name: str):
        self.crawlers = [c for c in self.crawlers if c.get_name() != name]
    
    def create_crawler(self, name: str, url: str, type: str = "html", **kwargs) -> CrawlerBase:
        if type.lower() == "rss":
            return RSSCrawler(name, url)
        elif type.lower() == "dynamic":
            timeout = kwargs.get("timeout", 30)
            wait_time = kwargs.get("wait_time", 5)
            return DynamicCrawler(name, url, timeout, wait_time)
        else:
            timeout = kwargs.get("timeout", 30)
            return HTMLCrawler(name, url, timeout)
    
    def crawl_all(self) -> List[Dict[str, str]]:
        all_results = []
        
        for crawler in self.crawlers:
            try:
                results = crawler.crawl()
                all_results.extend(results)
                logger.info(f"Crawler {crawler.get_name()} returned {len(results)} items")
            except Exception as e:
                logger.error(f"Crawler {crawler.get_name()} failed: {str(e)}")
        
        return all_results
    
    def crawl_single(self, name: str) -> List[Dict[str, str]]:
        for crawler in self.crawlers:
            if crawler.get_name() == name:
                return crawler.crawl()
        return []
    
    def get_crawler_names(self) -> List[str]:
        return [c.get_name() for c in self.crawlers]

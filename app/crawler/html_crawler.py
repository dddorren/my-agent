import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
from .base_crawler import CrawlerBase
import logging

logger = logging.getLogger(__name__)

class HTMLCrawler(CrawlerBase):
    def __init__(self, name: str, url: str, timeout: int = 30):
        super().__init__(name, url)
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def crawl(self) -> List[Dict[str, str]]:
        results = []
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = self._parse_html(soup)
            
            logger.info(f"HTML Crawler {self.name} fetched {len(results)} items")
            self.set_last_crawl_time(datetime.now())
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTML Crawler {self.name} failed: {str(e)}")
        
        return results
    
    def _parse_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        results = []
        
        title_selectors = [
            "h1", "h2", "h3",
            ".title", ".news-title", ".hot-title",
            ".list-item-title", ".article-title",
            ".title-link", ".link-title",
            "a[title]", "a[href*='article']"
        ]
        
        for selector in title_selectors:
            elements = soup.select(selector)
            for element in elements[:30]:
                title = element.get_text(strip=True) if element else ""
                link = element.get("href", "") if element else ""
                
                if title and len(title) > 5:
                    if not link.startswith("http"):
                        link = self.url + link if self.url else link
                    
                    item = {
                        "title": title,
                        "link": link,
                        "summary": "",
                        "published": "",
                        "source": self.name,
                        "crawl_time": datetime.now().isoformat()
                    }
                    results.append(item)
        
        return list({item["title"]: item for item in results}.values())

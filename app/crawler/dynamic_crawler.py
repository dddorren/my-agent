from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
from .base_crawler import CrawlerBase
import logging

logger = logging.getLogger(__name__)

class DynamicCrawler(CrawlerBase):
    def __init__(self, name: str, url: str, timeout: int = 30, wait_time: int = 5):
        super().__init__(name, url)
        self.timeout = timeout
        self.wait_time = wait_time
    
    def crawl(self) -> List[Dict[str, str]]:
        results = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                page.set_default_timeout(self.timeout * 1000)
                page.goto(self.url)
                page.wait_for_timeout(self.wait_time * 1000)
                
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                results = self._parse_html(soup)
                
                browser.close()
                logger.info(f"Dynamic Crawler {self.name} fetched {len(results)} items")
                self.set_last_crawl_time(datetime.now())
                
        except Exception as e:
            logger.error(f"Dynamic Crawler {self.name} failed: {str(e)}")
        
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

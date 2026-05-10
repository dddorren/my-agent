import re
from typing import List, Dict
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.html_pattern = re.compile(r'<[^>]+>')
        self.special_char_pattern = re.compile(r'[^\u4e00-\u9fff0-9a-zA-Z\s，。！？、；：""''（）《》【】—…·]')
        self.whitespace_pattern = re.compile(r'\s+')
    
    def remove_html(self, text: str) -> str:
        if not text:
            return ""
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text(strip=True)
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = self.remove_html(text)
        text = self.special_char_pattern.sub('', text)
        text = self.whitespace_pattern.sub(' ', text)
        text = text.strip()
        
        return text
    
    def clean_items(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        cleaned = []
        
        for item in items:
            cleaned_item = {
                "title": self.clean_text(item.get("title", "")),
                "link": item.get("link", ""),
                "summary": self.clean_text(item.get("summary", "")),
                "published": item.get("published", ""),
                "source": item.get("source", ""),
                "crawl_time": item.get("crawl_time", "")
            }
            
            if cleaned_item["title"] and len(cleaned_item["title"]) > 5:
                cleaned.append(cleaned_item)
        
        logger.info(f"Cleaned {len(cleaned)} items from {len(items)} raw items")
        return cleaned
    
    def deduplicate(self, items: List[Dict[str, str]], threshold: float = 0.9) -> List[Dict[str, str]]:
        if not items:
            return []
        
        unique_items = []
        seen_titles = set()
        
        for item in items:
            title = item["title"]
            normalized_title = self._normalize(title)
            
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_items.append(item)
        
        logger.info(f"Deduplicated {len(items)} items to {len(unique_items)} unique items")
        return unique_items
    
    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[，。！？、；：""''（）《》【】—…·\s]', '', text)
        return text

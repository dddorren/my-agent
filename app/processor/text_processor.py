import re
from typing import List, Dict
import jieba
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.sentence_pattern = re.compile(r'([。！？；])')
    
    def split_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        
        parts = self.sentence_pattern.split(text)
        sentences = []
        
        for i in range(0, len(parts)-1, 2):
            sentence = (parts[i] + parts[i+1]).strip()
            if sentence:
                sentences.append(sentence)
        
        return sentences
    
    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        
        words = jieba.lcut(text)
        words = [w for w in words if len(w) > 1 and not w.isspace()]
        
        return words
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        if not text:
            return []
        
        words = self.tokenize(text)
        word_counts = {}
        
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, count in sorted_words[:top_n]]
        
        return keywords
    
    def process_items(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        processed = []
        
        for item in items:
            text = item["title"] + " " + item.get("summary", "")
            sentences = self.split_sentences(text)
            keywords = self.extract_keywords(text)
            
            processed_item = {
                **item,
                "sentences": sentences,
                "keywords": keywords,
                "text_length": len(text)
            }
            
            processed.append(processed_item)
        
        logger.info(f"Processed {len(processed)} items")
        return processed

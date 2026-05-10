from typing import List, Dict
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import logging
from .llm_client import LLMClient
from app.config.prompts import TOPIC_GENERATION_PROMPT

logger = logging.getLogger(__name__)

class TopicAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            token_pattern=r'(?u)\b\w+\b'
        )
    
    def cluster_topics(self, items: List[Dict[str, str]], n_clusters: int = 5) -> List[List[Dict[str, str]]]:
        if len(items) < n_clusters:
            return [[item] for item in items]

        valid_items = [item for item in items if item.get("title")]
        if len(valid_items) < n_clusters:
            return [[item] for item in valid_items]

        texts = []
        for item in valid_items:
            title = item.get("title", "")
            summary = item.get("summary", "") or ""
            texts.append(f"{title} {summary}")

        try:
            X = self.vectorizer.fit_transform(texts)
            kmeans = KMeans(n_clusters=min(n_clusters, len(valid_items)), random_state=42, n_init="auto")
            labels = kmeans.fit_predict(X)

            clusters = [[] for _ in range(min(n_clusters, len(valid_items)))]
            for idx, item in enumerate(valid_items):
                clusters[labels[idx]].append(item)

            return clusters

        except Exception as e:
            logger.error(f"Clustering failed: {str(e)}")
            return [[item] for item in valid_items]
    
    def extract_hot_topics(self, items: List[Dict[str, str]]) -> List[str]:
        if not items:
            return []

        clusters = self.cluster_topics(items, n_clusters=5)
        hot_contents = []

        for cluster in clusters:
            if cluster:
                cluster_texts = [item["title"] for item in cluster if item.get("title")]
                if cluster_texts:
                    cluster_text = "\n".join(cluster_texts[:5])
                    hot_contents.append(cluster_text)

        return hot_contents
    
    def generate_topics(self, items: List[Dict[str, str]], count: int = 5) -> List[str]:
        if not items:
            return []
        
        hot_contents = self.extract_hot_topics(items)
        hot_content_text = "\n\n".join(hot_contents)
        
        prompt = TOPIC_GENERATION_PROMPT.format(hot_content=hot_content_text)
        response = self.llm_client.call_json(prompt)
        
        topics = response.get("topics", [])[:count]
        
        logger.info(f"Generated {len(topics)} topics")
        return topics

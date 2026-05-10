from typing import Dict, List, Optional
import logging
from app.topic_agent.llm_client import LLMClient
from app.config.prompts import TITLE_OPTIMIZATION_PROMPT, TAG_GENERATION_PROMPT, STYLE_ADJUSTMENT_PROMPT

logger = logging.getLogger(__name__)

class EditorAgent:
    def __init__(self):
        self.llm_client = LLMClient()
    
    def optimize_title(self, title: str) -> str:
        if not title:
            return ""
        
        prompt = TITLE_OPTIMIZATION_PROMPT.format(title=title)
        response = self.llm_client.call(prompt, max_tokens=100)
        
        optimized_title = response.strip() if response else title
        
        logger.info(f"Optimized title: {title} -> {optimized_title}")
        return optimized_title
    
    def generate_tags(self, story: str, count: int = 8) -> List[str]:
        if not story:
            return []
        
        prompt = TAG_GENERATION_PROMPT.format(story=story)
        response = self.llm_client.call(prompt, max_tokens=200)
        
        if response:
            tags = [t.strip() for t in response.split() if t.startswith("#")]
            return tags[:count]
        
        return ["#情感", "#故事", "#小说", "#小红书"]
    
    def adjust_style(self, story: str, style: str = "情感") -> str:
        if not story:
            return ""
        
        prompt = STYLE_ADJUSTMENT_PROMPT.format(story=story, style=style)
        response = self.llm_client.call(prompt, max_tokens=2000)
        
        adjusted_story = response.strip() if response else story
        
        logger.info(f"Adjusted story style to: {style}")
        return adjusted_story
    
    def edit_content(self, content: Dict[str, str], style: Optional[str] = None) -> Dict[str, str]:
        title = content.get("title", "")
        story = content.get("story", "")
        
        optimized_title = self.optimize_title(title)
        
        if style:
            adjusted_story = self.adjust_style(story, style)
        else:
            adjusted_story = story
        
        tags = self.generate_tags(adjusted_story)
        
        result = {
            "title": optimized_title,
            "story": adjusted_story,
            "tags": tags,
            "topic": content.get("topic", "")
        }
        
        logger.info(f"Edited content with {len(tags)} tags")
        return result

import json
import os
from datetime import datetime
from typing import Dict, Optional
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

class Publisher:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
    
    def format_content(self, content: Dict[str, str], format_type: str = "markdown") -> str:
        title = content.get("title", "")
        story = content.get("story", "")
        tags = content.get("tags", [])
        
        if format_type == "markdown":
            tag_str = " ".join(tags) if tags else ""
            return f"""# {title}

{story}

{tag_str}
"""
        elif format_type == "html":
            tag_str = " ".join(tags) if tags else ""
            return f"""<div class="xiaohongshu-content">
<h1>{title}</h1>
<p>{story}</p>
<div class="tags">{tag_str}</div>
</div>
"""
        else:
            return json.dumps(content, ensure_ascii=False, indent=2)
    
    def export_content(self, content: Dict[str, str], filename: Optional[str] = None, format_type: str = "markdown") -> str:
        formatted = self.format_content(content, format_type)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"post_{timestamp}.md"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(formatted)
            
            logger.info(f"Content exported to: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to export content: {str(e)}")
            return ""
    
    def export_json(self, content: Dict[str, str]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSON content exported to: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to export JSON: {str(e)}")
            return ""

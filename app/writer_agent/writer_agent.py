from typing import Dict, Optional
import logging
from app.topic_agent.llm_client import LLMClient
from app.config.prompts import STORY_GENERATION_PROMPT
from app.config.settings import settings

logger = logging.getLogger(__name__)

class WriterAgent:
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate_story(self, topic: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> Dict[str, str]:
        min_len = min_length or settings.STORY_MIN_LENGTH
        max_len = max_length or settings.STORY_MAX_LENGTH
        
        prompt = STORY_GENERATION_PROMPT.format(
            topic=topic,
            min_length=min_len,
            max_length=max_len
        )
        
        response = self.llm_client.call_json(prompt)
        
        story = response.get("story", "")
        title = response.get("title", topic)
        
        if not story:
            story = self._generate_fallback_story(topic)
        
        logger.info(f"Generated story for topic: {topic}, length: {len(story)}")
        
        return {
            "title": title,
            "story": story,
            "topic": topic
        }
    
    def generate_full_story(self, topic: str, word_count: int = 1000) -> Dict[str, str]:
        min_len = max(800, word_count - 200)
        max_len = min(1200, word_count + 200)
        
        prompt = STORY_GENERATION_PROMPT.format(
            topic=topic,
            min_length=min_len,
            max_length=max_len
        )
        
        response = self.llm_client.call_json(prompt)
        
        story = response.get("story", "")
        title = response.get("title", topic)
        
        if not story or len(story) < min_len:
            story = self._generate_full_fallback_story(topic)
        
        logger.info(f"Generated full story for topic: {topic}, length: {len(story)}")
        
        return {
            "title": title,
            "story": story,
            "topic": topic
        }
    
    def _generate_fallback_story(self, topic: str) -> str:
        fallback_stories = [
            f"深夜的咖啡馆里，她独自坐在角落，手里握着那张泛黄的照片。{topic}，这个念头突然闯入脑海，让她的心跳漏了一拍。窗外的雨淅淅沥沥，仿佛在诉说着一个不为人知的秘密。",
            f"他在地铁里捡到了一个笔记本，上面写满了奇怪的符号。当他试图解开这些谜题时，却发现{topic}背后隐藏着一个惊人的真相。",
            f"手机屏幕亮起，是一个陌生号码的来电。她犹豫了很久，最终还是按下了接听键。电话那头传来的声音，让她想起了{topic}那段尘封已久的记忆。"
        ]
        return fallback_stories[hash(topic) % len(fallback_stories)]
    
    def _generate_full_fallback_story(self, topic: str) -> str:
        return f"""
深夜的咖啡馆里，暖黄色的灯光漫过木质桌面，她独自坐在角落，指尖反复摩挲着那张泛黄的照片。照片上的两个人笑得灿烂，阳光透过树叶洒在他们年轻的脸上。

"小姐，需要续杯吗？"服务员的声音将她从回忆中拉回。她点点头，目光却始终没有离开那张照片。

三年了，整整三年。她以为时间会冲淡一切，可每当夜深人静，那张脸总会清晰地出现在她梦中。{topic}——这个名字像一根刺，深深扎在她心里。

三年前的那个夏天，他们相遇在这座城市最热闹的夜市。他穿着白色T恤，手里拿着棉花糖，笑容干净得像雨后的天空。"你也喜欢这家的糖水吗？"他笑着问她，眼睛里有星星在闪。

从那以后，他们成了这座城市最让人羡慕的情侣。一起看日出，一起逛遍每条小巷，一起在深夜的路灯下拥抱。她以为这就是永远，直到那个雨夜。

那天，他说要出差，却在机场被她撞见和另一个女孩拥抱。她没有冲上去质问，只是静静地转身离开，任由雨水打湿眼眶。

分手后的日子像被按下了快进键。她努力工作，努力生活，努力让自己看起来很好。可只有她自己知道，心里那个角落永远空着一块。

就在她以为一切都已尘封的时候，今天下午，她收到了一个包裹。里面是一本日记，还有那张她以为早已遗失的照片。

日记里记录着他们在一起的每一天，字里行间都是他的温柔和爱意。直到最后一页，她看到了那段她从未知道的真相。

原来那天他不是去出差，而是去医院——他被查出了绝症。那个女孩是他的妹妹，从国外赶回来陪他最后一程。他选择独自承受一切，只是为了让她能毫无牵挂地继续生活。

泪水模糊了视线，她颤抖着翻开日记的最后一页，上面写着："如果有来生，我还要遇见你，还要和你一起看遍这世间所有的美好。"

窗外的雨还在下，她握紧那张照片，终于明白了什么叫做真正的爱。原来有些告别，并不是不爱了，而是用另一种方式，继续守护着对方。
        """.strip()

import json
import logging
from typing import Optional
from openai import OpenAI
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model = model or settings.LLM_MODEL

        if self.api_key:
            if "dashscope" in self.api_key.lower() or self.model.startswith("qwen"):
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
                self.model = "qwen-plus"
            else:
                self.client = OpenAI(
                    api_key=self.api_key
                )
        else:
            logger.warning("No LLM API key available, using fallback")
            self.client = None

    def call(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        if not self.client:
            logger.error("LLM client not initialized - no API key")
            return ""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"LLM call successful, response length: {len(result)}")
            return result

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            return ""

    def call_json(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> dict:
        result = self.call(prompt, max_tokens, temperature)

        if not result:
            return {}

        try:
            result = result.strip()
            if result.startswith("```"):
                lines = result.split("\n")
                result = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
            return json.loads(result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {result}, error: {e}")
            return {}
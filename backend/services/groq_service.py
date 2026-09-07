"""
Groq API Service - Central hub for all LLM interactions via Groq.
Handles chat completions, streaming, and multi-turn conversations.
"""

import json
import logging
from typing import AsyncGenerator, Optional
from groq import AsyncGroq, Groq
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import GROQ_API_KEY, GROQ_MODELS, GROQ_BASE_URL

logger = logging.getLogger(__name__)


class GroqService:
    """Service for interacting with Groq API."""

    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.client = Groq(api_key=self.api_key)
        self.async_client = AsyncGroq(api_key=self.api_key)
        self.models = GROQ_MODELS

    def _get_model(self, model_key: str = "primary") -> str:
        """Get model name from key."""
        return self.models.get(model_key, self.models["primary"])

    def chat_completion(
        self,
        messages: list[dict],
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        response_format: Optional[dict] = None,
    ) -> str:
        """Synchronous chat completion."""
        try:
            model = self._get_model(model_key)
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if response_format:
                kwargs["response_format"] = response_format

            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq chat completion error: {e}")
            raise

    async def async_chat_completion(
        self,
        messages: list[dict],
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        response_format: Optional[dict] = None,
    ) -> str:
        """Asynchronous chat completion."""
        try:
            model = self._get_model(model_key)
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if response_format:
                kwargs["response_format"] = response_format

            response = await self.async_client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq async chat completion error: {e}")
            raise

    async def streaming_chat(
        self,
        messages: list[dict],
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        """Streaming chat completion - yields tokens."""
        try:
            model = self._get_model(model_key)
            stream = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            yield f"Error: {str(e)}"

    def structured_completion(
        self,
        messages: list[dict],
        model_key: str = "primary",
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> dict:
        """Chat completion that returns structured JSON."""
        try:
            result = self.chat_completion(
                messages=messages,
                model_key=model_key,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            return json.loads(result)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            result = self.chat_completion(
                messages=messages,
                model_key=model_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Extract JSON from markdown code block
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            return {"raw_response": result}
        except Exception as e:
            logger.error(f"Groq structured completion error: {e}")
            raise


# Singleton instance
groq_service = GroqService()

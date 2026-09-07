"""
RAG Engine - Combines knowledge base retrieval with LLM generation.
Orchestrates the multi-agent system for compliance analysis.
"""

import json
import logging
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import RAG_CONFIG
from backend.services.groq_service import groq_service
from backend.services.knowledge_base_service import kb_service

logger = logging.getLogger(__name__)


class RAGEngine:
    """Core RAG engine that retrieves context and generates responses."""

    def __init__(self):
        self.groq = groq_service
        self.kb = kb_service

    def retrieve_context(self, query: str, top_k: int = None, category: str = None, city: str = None) -> str:
        """Retrieve relevant context from the knowledge base."""
        results = self.kb.search(query=query, top_k=top_k or RAG_CONFIG["top_k"], category=category, city=city)

        if not results:
            return "No relevant knowledge base entries found for this query."

        context_parts = []
        for i, result in enumerate(results):
            meta = result.get("metadata", {})
            context_parts.append(
                f"[Source {i+1}: {meta.get('law_name', 'Unknown Law')} | "
                f"{meta.get('city', 'All Cities')}, {meta.get('state', '')} | "
                f"{meta.get('category', '')} | Relevance: {result.get('relevance_score', 0):.2f}]\n"
                f"{result['text']}"
            )

        return "\n\n---\n\n".join(context_parts)

    def generate(
        self,
        query: str,
        system_prompt: str,
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        use_rag: bool = True,
        category: str = None,
        city: str = None,
        additional_context: str = "",
        history: list[dict] = None,
    ) -> str:
        """Generate a response using RAG + LLM."""
        # Retrieve context from KB
        context = ""
        if use_rag:
            context = self.retrieve_context(query=query, category=category, city=city)

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            messages.extend(history)

        user_message = ""
        if context:
            user_message += f"## Relevant Legal Knowledge Base Context:\n\n{context}\n\n---\n\n"
        if additional_context:
            user_message += f"## Additional Context:\n\n{additional_context}\n\n---\n\n"
        user_message += f"## Query/Request:\n\n{query}"

        messages.append({"role": "user", "content": user_message})

        return self.groq.chat_completion(
            messages=messages,
            model_key=model_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def async_generate(
        self,
        query: str,
        system_prompt: str,
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        use_rag: bool = True,
        category: str = None,
        city: str = None,
        additional_context: str = "",
        history: list[dict] = None,
    ) -> str:
        """Async generate with RAG."""
        context = ""
        if use_rag:
            context = self.retrieve_context(query=query, category=category, city=city)

        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)

        user_message = ""
        if context:
            user_message += f"## Relevant Legal Knowledge Base Context:\n\n{context}\n\n---\n\n"
        if additional_context:
            user_message += f"## Additional Context:\n\n{additional_context}\n\n---\n\n"
        user_message += f"## Query/Request:\n\n{query}"

        messages.append({"role": "user", "content": user_message})

        return await self.groq.async_chat_completion(
            messages=messages,
            model_key=model_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def streaming_generate(
        self,
        query: str,
        system_prompt: str,
        model_key: str = "primary",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        additional_context: str = "",
        history: list[dict] = None,
    ):
        """Streaming generation."""
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)

        user_message = ""
        if additional_context:
            user_message += f"## Context:\n\n{additional_context}\n\n---\n\n"
        user_message += f"## Query:\n\n{query}"
        messages.append({"role": "user", "content": user_message})

        async for chunk in self.groq.streaming_chat(
            messages=messages,
            model_key=model_key,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield chunk


# Singleton
rag_engine = RAGEngine()

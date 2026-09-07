"""
Knowledge Base Service - Vector store management, document indexing, and RAG retrieval.
Uses ChromaDB for vector storage and sentence-transformers for embeddings.
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import (
    KB_DIR, EMBEDDING_MODEL, EMBEDDING_DIMENSION,
    CHROMA_PERSIST_DIR, CHUNK_SIZE, CHUNK_OVERLAP,
    RAG_CONFIG
)

logger = logging.getLogger(__name__)

# Lazy imports for heavy libraries
_chroma_client = None
_embedding_fn = None


def _get_embedding_function():
    """Lazy-load the sentence transformer embedding function."""
    global _embedding_fn
    if _embedding_fn is None:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        _embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
    return _embedding_fn


def _get_chroma_client():
    """Lazy-load the ChromaDB persistent client."""
    global _chroma_client
    if _chroma_client is None:
        import chromadb
        CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR)
        )
    return _chroma_client


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def create_document_chunks(law_entry: dict) -> list[dict]:
    """Create searchable chunks from a law knowledge base entry."""
    chunks = []
    doc_id = law_entry.get("id", "unknown")

    # Main summary chunk
    main_text = (
        f"Law: {law_entry.get('law_name', '')} ({law_entry.get('law_number', '')})\n"
        f"City: {law_entry.get('city', '')}, State: {law_entry.get('state', '')}\n"
        f"Category: {law_entry.get('category', '')} - {law_entry.get('subcategory', '')}\n"
        f"Authority: {law_entry.get('authority', '')}\n"
        f"Summary: {law_entry.get('summary', '')}\n"
    )

    # Add detailed provisions
    provisions = law_entry.get("detailed_provisions", [])
    if provisions:
        main_text += "Detailed Provisions:\n"
        for i, p in enumerate(provisions, 1):
            main_text += f"{i}. {p}\n"

    # Add penalties
    penalties = law_entry.get("penalties", "")
    if penalties:
        main_text += f"Penalties: {penalties}\n"

    # Add tags
    tags = law_entry.get("tags", [])
    if tags:
        main_text += f"Tags: {', '.join(tags)}\n"

    # Chunk the main text
    text_chunks = chunk_text(main_text)
    for i, chunk in enumerate(text_chunks):
        chunk_id = f"{doc_id}_chunk_{i}"
        metadata = {
            "doc_id": doc_id,
            "city": law_entry.get("city", ""),
            "state": law_entry.get("state", ""),
            "category": law_entry.get("category", ""),
            "subcategory": law_entry.get("subcategory", ""),
            "law_name": law_entry.get("law_name", ""),
            "authority": law_entry.get("authority", ""),
            "chunk_index": i,
            "total_chunks": len(text_chunks),
            "tags": ",".join(tags) if tags else "",
        }
        chunks.append({
            "id": chunk_id,
            "text": chunk,
            "metadata": metadata,
        })

    return chunks


class KnowledgeBaseService:
    """Manages the vector knowledge base for construction compliance laws."""

    def __init__(self):
        self.collection_name = "knowledge_base"

    def get_collection(self):
        """Get or create the ChromaDB collection."""
        client = _get_chroma_client()
        embedding_fn = _get_embedding_function()
        try:
            collection = client.get_collection(
                name=self.collection_name,
                embedding_function=embedding_fn,
            )
        except Exception:
            collection = client.create_collection(
                name=self.collection_name,
                embedding_function=embedding_fn,
                metadata={"description": "Indian Construction Compliance Laws Knowledge Base"}
            )
        return collection

    def index_knowledge_base(self):
        """Index all knowledge base JSON files into ChromaDB."""
        collection = self.get_collection()

        # Load all KB files
        kb_files = list(KB_DIR.glob("*.json"))
        all_chunks = []

        for kb_file in kb_files:
            logger.info(f"Loading knowledge base: {kb_file.name}")
            with open(kb_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                entries = data
            elif isinstance(data, dict) and "entries" in data:
                entries = data["entries"]
            else:
                entries = [data]

            for entry in entries:
                chunks = create_document_chunks(entry)
                all_chunks.extend(chunks)

        logger.info(f"Total chunks to index: {len(all_chunks)}")

        # Batch upsert into ChromaDB
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            ids = [c["id"] for c in batch]
            documents = [c["text"] for c in batch]
            metadatas = [c["metadata"] for c in batch]

            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )

            if (i + batch_size) % 500 == 0:
                logger.info(f"  Indexed {i + batch_size}/{len(all_chunks)} chunks...")

        logger.info(f"Knowledge base indexing complete: {collection.count()} documents")
        return collection.count()

    def search(
        self,
        query: str,
        top_k: int = None,
        category: Optional[str] = None,
        city: Optional[str] = None,
    ) -> list[dict]:
        """Search the knowledge base with optional filters."""
        if top_k is None:
            top_k = RAG_CONFIG["top_k"]

        collection = self.get_collection()
        where_filter = {}
        if category:
            where_filter["category"] = category
        if city:
            where_filter["city"] = city

        kwargs = {
            "query_texts": [query],
            "n_results": min(top_k, collection.count()) if collection.count() > 0 else top_k,
        }
        if where_filter:
            kwargs["where"] = where_filter if len(where_filter) == 1 else {"$and": [{k: v} for k, v in where_filter.items()]}

        results = collection.query(**kwargs)

        formatted_results = []
        if results and results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 0

                formatted_results.append({
                    "text": doc,
                    "metadata": metadata,
                    "relevance_score": max(0, 1 - distance),
                })

        return formatted_results

    def get_collection_stats(self) -> dict:
        """Get statistics about the knowledge base."""
        collection = self.get_collection()
        count = collection.count()
        return {
            "total_documents": count,
            "collection_name": self.collection_name,
            "status": "ready" if count > 0 else "empty",
        }


# Singleton
kb_service = KnowledgeBaseService()

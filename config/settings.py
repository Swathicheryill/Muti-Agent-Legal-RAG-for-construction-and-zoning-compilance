"""
Configuration settings for Multi-Agent Legal RAG System.
All API keys, paths, and system parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ============================================================================
# BASE PATHS
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
KB_DIR = DATASETS_DIR / "knowledge_base"
OBJ1_DIR = DATASETS_DIR / "objective1_conflict"
OBJ2_DIR = DATASETS_DIR / "objective2_prediction"
OBJ3_DIR = DATASETS_DIR / "objective3_verification"

# ============================================================================
# GROQ API CONFIGURATION
# ============================================================================

# Set your Groq API key here or via environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")

# Groq models available (updated to current API)
GROQ_MODELS = {
    "primary": "qwen/qwen3.6-27b",              # Main model for complex reasoning
    "fast": "qwen/qwen3.8-27b",                 # Fast model for simple queries
    "code": "qwen/qwen3.8-27b",                 # Code generation
    "analysis": "openai/gpt-oss-20b",            # Analysis model
}

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MAX_TOKENS = 4096
GROQ_TEMPERATURE = 0.3  # Low temperature for legal accuracy

# ============================================================================
# EMBEDDING MODEL CONFIGURATION
# ============================================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
CHROMA_PERSIST_DIR = BASE_DIR / "vector_store"
CHROMA_COLLECTION_KB = "knowledge_base"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

AGENTS = {
    "conflict_resolver": {
        "name": "Conflict Resolution Agent",
        "description": "Resolves contradictory legal requirements across jurisdictions",
        "model": GROQ_MODELS["primary"],
        "temperature": 0.2,
        "max_tokens": 4096,
        "system_prompt_file": "conflict_resolver_prompt.txt"
    },
    "time_predictor": {
        "name": "Time-Aware Prediction Agent",
        "description": "Predicts future compliance violations 6-12 months ahead",
        "model": GROQ_MODELS["primary"],
        "temperature": 0.4,
        "max_tokens": 4096,
        "system_prompt_file": "time_predictor_prompt.txt"
    },
    "verifier": {
        "name": "Verification & Reporting Agent",
        "description": "Produces inspector-ready compliance reports with reasoning chains",
        "model": GROQ_MODELS["primary"],
        "temperature": 0.1,
        "max_tokens": 4096,
        "system_prompt_file": "verifier_prompt.txt"
    },
    "inspector_chatbot": {
        "name": "Inspector Chatbot",
        "description": "AI inspector/authority person for interactive compliance guidance",
        "model": GROQ_MODELS["primary"],
        "temperature": 0.5,
        "max_tokens": 2048,
        "system_prompt_file": "inspector_prompt.txt"
    },
    "legal_parser": {
        "name": "Legal Parsing Agent",
        "description": "Parses and extracts structured information from legal documents",
        "model": GROQ_MODELS["fast"],
        "temperature": 0.1,
        "max_tokens": 2048,
        "system_prompt_file": "legal_parser_prompt.txt"
    }
}

# ============================================================================
# RAG CONFIGURATION
# ============================================================================

RAG_CONFIG = {
    "top_k": 10,
    "similarity_threshold": 0.3,
    "rerank_top_k": 5,
    "max_context_length": 8000,
    "use_reranker": True,
}

# ============================================================================
# TRAINING CONFIGURATION
# ============================================================================

TRAINING_CONFIG = {
    "epochs": 3,
    "batch_size": 16,
    "learning_rate": 2e-5,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "max_length": 512,
    "output_dir": BASE_DIR / "training" / "output",
    "log_steps": 100,
    "eval_steps": 500,
    "save_steps": 1000,
    "fp16": True,
    "gradient_accumulation_steps": 4,
}

# ============================================================================
# API SERVER CONFIGURATION
# ============================================================================

API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "cors_origins": ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
}

# ============================================================================
# FRONTEND CONFIGURATION
# ============================================================================

FRONTEND_CONFIG = {
    "port": 3000,
    "api_base_url": "http://localhost:8000/api/v1",
}

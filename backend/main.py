"""
Multi-Agent Legal RAG System - Main FastAPI Application
Construction & Zoning Compliance for Indian Metropolitan Cities
"""

import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.settings import API_CONFIG
from backend.api.routes import router
from backend.services.knowledge_base_service import kb_service

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    logger.info("=" * 60)
    logger.info("Multi-Agent Legal RAG System - Starting Up")
    logger.info("=" * 60)

    # Initialize knowledge base
    try:
        stats = kb_service.get_collection_stats()
        if stats["status"] == "empty":
            logger.info("Knowledge base is empty. Indexing...")
            count = kb_service.index_knowledge_base()
            logger.info(f"Knowledge base indexed: {count} documents")
        else:
            logger.info(f"Knowledge base ready: {stats['total_documents']} documents")
    except Exception as e:
        logger.error(f"Knowledge base initialization error: {e}")

    logger.info("System ready!")

    yield

    # Shutdown
    logger.info("Multi-Agent Legal RAG System - Shutting Down")


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Legal RAG - Construction & Zoning Compliance",
    description=(
        "AI-powered multi-agent system for autonomous compliance analysis "
        "of construction and zoning regulations across Indian metropolitan cities "
        "(Bangalore, Chennai, Delhi, Mumbai, Hyderabad)."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(router, prefix="/api/v1")

# Serve frontend static files (if built)
FRONTEND_BUILD_DIR = os.path.join(PROJECT_ROOT, "frontend", "build")
if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD_DIR, "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for any non-API route."""
        file_path = os.path.join(FRONTEND_BUILD_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_BUILD_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "message": "Multi-Agent Legal RAG System - Construction & Zoning Compliance",
            "docs": "/docs",
            "api": "/api/v1",
            "status": "running",
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["debug"],
    )

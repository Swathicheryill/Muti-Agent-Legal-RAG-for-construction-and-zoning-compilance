"""
API Routes - FastAPI endpoints for the Multi-Agent Legal RAG system.
"""

import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.agents.conflict_resolver import conflict_resolver
from backend.agents.time_predictor import time_predictor
from backend.agents.verifier import verifier
from backend.agents.inspector_chatbot import inspector_chatbot, INSPECTOR_PERSONAS
from backend.services.knowledge_base_service import kb_service

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ConflictRequest(BaseModel):
    conflict_description: str = Field(..., description="Description of the legal conflict")
    city: Optional[str] = Field(None, description="City: Bangalore, Chennai, Delhi, Mumbai, Hyderabad")
    category: Optional[str] = Field(None, description="Law category: Building Construction, Environment, Water, etc.")
    project_details: Optional[dict] = Field(None, description="Project details: type, size, etc.")


class PredictionRequest(BaseModel):
    project_description: str = Field(..., description="Description of the construction project")
    city: Optional[str] = Field(None, description="City")
    project_timeline: Optional[dict] = Field(None, description="Timeline details")
    current_permits: Optional[list[str]] = Field(None, description="Current permits obtained")


class VerificationRequest(BaseModel):
    project_description: str = Field(..., description="Project description for verification")
    city: Optional[str] = Field(None, description="City")
    category: Optional[str] = Field(None, description="Verification category")
    inspection_details: Optional[dict] = Field(None, description="Inspection details")
    scope: str = Field("full", description="Verification scope: full, structural, fire, environmental")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the inspector")
    persona: str = Field("municipal_engineer", description="Inspector persona: municipal_engineer, environment_officer, fire_safety_officer, legal_advisor")
    history: Optional[list[dict]] = Field(None, description="Conversation history")


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    city: Optional[str] = Field(None, description="Filter by city")
    category: Optional[str] = Field(None, description="Filter by category")
    top_k: int = Field(5, description="Number of results")


# ============================================================================
# HEALTH & SYSTEM ROUTES
# ============================================================================

@router.get("/health")
async def health_check():
    """System health check."""
    kb_stats = kb_service.get_collection_stats()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "knowledge_base": kb_stats,
        "agents": ["conflict_resolver", "time_predictor", "verifier", "inspector_chatbot"],
        "groq_status": "connected",
    }


@router.get("/stats")
async def get_system_stats():
    """Get system statistics."""
    kb_stats = kb_service.get_collection_stats()
    return {
        "knowledge_base": kb_stats,
        "available_personas": list(INSPECTOR_PERSONAS.keys()),
        "supported_cities": ["Bangalore", "Chennai", "Delhi", "Mumbai", "Hyderabad"],
        "supported_categories": [
            "Building Construction", "Environment", "Water", "Air",
            "Road & Infrastructure", "Housing", "Industry", "Area/Zoning"
        ],
    }


# ============================================================================
# KNOWLEDGE BASE ROUTES
# ============================================================================

@router.post("/knowledge-base/search")
async def search_knowledge_base(request: SearchRequest):
    """Search the knowledge base."""
    try:
        results = kb_service.search(
            query=request.query,
            top_k=request.top_k,
            category=request.category,
            city=request.city,
        )
        return {
            "query": request.query,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/knowledge-base/index")
async def index_knowledge_base():
    """Re-index the knowledge base."""
    try:
        count = kb_service.index_knowledge_base()
        return {"status": "indexed", "document_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# OBJECTIVE 1: CONFLICT RESOLUTION
# ============================================================================

@router.post("/conflict-resolve")
async def resolve_conflict(request: ConflictRequest):
    """Resolve a legal conflict across jurisdictions."""
    try:
        result = conflict_resolver.resolve_conflict(
            conflict_description=request.conflict_description,
            city=request.city,
            category=request.category,
            project_details=request.project_details,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conflict-resolve/async")
async def async_resolve_conflict(request: ConflictRequest):
    """Async conflict resolution."""
    try:
        result = await conflict_resolver.async_resolve_conflict(
            conflict_description=request.conflict_description,
            city=request.city,
            category=request.category,
            project_details=request.project_details,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# OBJECTIVE 2: TIME-AWARE PREDICTION
# ============================================================================

@router.post("/predict")
async def predict_compliance(request: PredictionRequest):
    """Predict future compliance violations."""
    try:
        result = time_predictor.predict(
            project_description=request.project_description,
            city=request.city,
            project_timeline=request.project_timeline,
            current_permits=request.current_permits,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/async")
async def async_predict(request: PredictionRequest):
    """Async prediction."""
    try:
        result = await time_predictor.async_predict(
            project_description=request.project_description,
            city=request.city,
            project_timeline=request.project_timeline,
            current_permits=request.current_permits,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# OBJECTIVE 3: VERIFICATION & REPORTING
# ============================================================================

@router.post("/verify")
async def verify_compliance(request: VerificationRequest):
    """Generate a compliance verification report."""
    try:
        result = verifier.generate_report(
            project_description=request.project_description,
            city=request.city,
            category=request.category,
            inspection_details=request.inspection_details,
            scope=request.scope,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify/async")
async def async_verify(request: VerificationRequest):
    """Async verification report generation."""
    try:
        result = await verifier.async_generate_report(
            project_description=request.project_description,
            city=request.city,
            category=request.category,
            inspection_details=request.inspection_details,
            scope=request.scope,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INSPECTOR CHATBOT
# ============================================================================

@router.get("/chat/personas")
async def get_personas():
    """Get available inspector personas."""
    return inspector_chatbot.get_available_personas()


@router.post("/chat")
async def chat_with_inspector(request: ChatRequest):
    """Chat with an inspector/authority person."""
    try:
        if request.persona != inspector_chatbot.persona_key:
            inspector_chatbot.set_persona(request.persona)

        response = inspector_chatbot.get_response(
            user_message=request.message,
            history=request.history,
        )
        return {
            "response": response,
            "persona": inspector_chatbot.persona["name"],
            "role": inspector_chatbot.persona["role"],
            "avatar": inspector_chatbot.persona["avatar"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/async")
async def async_chat(request: ChatRequest):
    """Async chat with inspector."""
    try:
        if request.persona != inspector_chatbot.persona_key:
            inspector_chatbot.set_persona(request.persona)

        response = await inspector_chatbot.async_get_response(
            user_message=request.message,
            history=request.history,
        )
        return {
            "response": response,
            "persona": inspector_chatbot.persona["name"],
            "role": inspector_chatbot.persona["role"],
            "avatar": inspector_chatbot.persona["avatar"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UNIFIED COMPLIANCE CHECK
# ============================================================================

@router.post("/compliance-check")
async def comprehensive_compliance_check(request: dict):
    """
    Comprehensive compliance check that runs all three agents:
    1. Conflict resolution for jurisdictional issues
    2. Time-aware prediction for future risks
    3. Verification report for current compliance
    """
    try:
        project_desc = request.get("project_description", "")
        city = request.get("city", None)

        # Run all three agents
        conflict_result = conflict_resolver.resolve_conflict(
            conflict_description=f"Check for jurisdictional conflicts in: {project_desc}",
            city=city,
        )

        prediction_result = time_predictor.predict(
            project_description=project_desc,
            city=city,
        )

        verification_result = verifier.generate_report(
            project_description=project_desc,
            city=city,
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "conflict_analysis": conflict_result,
            "risk_prediction": prediction_result,
            "compliance_report": verification_result,
            "summary": {
                "conflict_risk": conflict_result.get("risk_assessment", {}).get("level", "Unknown"),
                "prediction_confidence": prediction_result.get("confidence_score", 0),
                "compliance_status": verification_result.get("compliance_summary", {}).get("overall_status", "Unknown"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

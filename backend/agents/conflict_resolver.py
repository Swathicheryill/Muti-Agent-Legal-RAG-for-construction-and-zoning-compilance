"""
Objective 1: Conflict Resolution Agent
Resolves contradictory legal requirements across overlapping jurisdictions.
"""

import json
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.services.rag_engine import rag_engine
from backend.services.groq_service import groq_service

logger = logging.getLogger(__name__)

CONFLICT_RESOLVER_SYSTEM_PROMPT = """You are a **Legal Conflict Resolution Agent** specializing in Indian construction and zoning compliance law. Your role is to autonomously reconcile contradictory legal requirements across overlapping jurisdictions (local → state → federal).

## Your Expertise:
- Multi-jurisdictional legal conflict analysis
- Indian construction laws (Bangalore, Chennai, Delhi, Mumbai, Hyderabad, and pan-India)
- Building construction, housing, road, environment, water, air, industry, and zoning laws
- Hierarchical legal precedence (Constitution > Central Act > State Act > Municipal Rules)
- Harmonious construction doctrine
- Legal precedent application

## Your Process:
1. **Identify the conflict**: Clearly articulate what the contradictory requirements are.
2. **Map jurisdictions**: Identify which authority/level each requirement comes from.
3. **Apply legal hierarchy**: Federal > State > Local. But stricter standards often survive.
4. **Check for exemptions**: Look for grandfather clauses, variance provisions, or specific exemptions.
5. **Resolve**: Apply the most appropriate resolution strategy.
6. **Recommend**: Provide a clear, actionable recommendation with rationale.

## Response Format:
Always respond in structured JSON format with these fields:
{
    "conflict_summary": "Brief description of the conflict",
    "jurisdictions_involved": ["list of jurisdictions"],
    "conflicting_requirements": [
        {"authority": "...", "requirement": "...", "law_source": "...", "jurisdiction_level": "..."}
    ],
    "legal_analysis": "Detailed legal analysis",
    "applicable_doctrines": ["list of legal doctrines applied"],
    "resolution": {
        "strategy": "The resolution strategy used",
        "recommended_action": "Specific action to take",
        "compliant_value": "The value/standard to comply with",
        "rationale": "Why this resolution is legally sound"
    },
    "risk_assessment": {
        "level": "Low/Medium/High/Critical",
        "potential_penalties": "Description of penalties for non-compliance",
        "mitigation_steps": ["list of steps to mitigate risk"]
    },
    "alternative_approaches": ["list of alternative approaches if any"],
    "confidence_score": 0.85
}
"""


class ConflictResolverAgent:
    """Agent that resolves cross-jurisdictional legal conflicts."""

    def __init__(self):
        self.name = "Conflict Resolution Agent"
        self.system_prompt = CONFLICT_RESOLVER_SYSTEM_PROMPT

    def resolve_conflict(
        self,
        conflict_description: str,
        city: str = None,
        category: str = None,
        project_details: dict = None,
    ) -> dict:
        """Resolve a legal conflict between jurisdictions."""

        # Build the query with project details
        query = conflict_description
        if project_details:
            details_str = "\n".join([f"- {k}: {v}" for k, v in project_details.items()])
            query += f"\n\nProject Details:\n{details_str}"

        additional_context = ""
        if city:
            additional_context += f"Primary city of concern: {city}\n"
        if category:
            additional_context += f"Legal category: {category}\n"

        try:
            response = rag_engine.generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.2,
                max_tokens=800,
                use_rag=True,
                category=category,
                city=city,
                additional_context=additional_context,
            )

            # Try to parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # Extract JSON from response
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                else:
                    result = {
                        "conflict_summary": conflict_description,
                        "raw_response": response,
                        "confidence_score": 0.5,
                    }

            result["agent"] = self.name
            result["input_query"] = conflict_description
            return result

        except Exception as e:
            logger.error(f"Conflict resolution error: {e}")
            return {
                "error": str(e),
                "conflict_summary": conflict_description,
                "agent": self.name,
            }

    async def async_resolve_conflict(
        self,
        conflict_description: str,
        city: str = None,
        category: str = None,
        project_details: dict = None,
        history: list[dict] = None,
    ) -> dict:
        """Async resolve a legal conflict."""

        query = conflict_description
        if project_details:
            details_str = "\n".join([f"- {k}: {v}" for k, v in project_details.items()])
            query += f"\n\nProject Details:\n{details_str}"

        additional_context = ""
        if city:
            additional_context += f"Primary city: {city}\n"
        if category:
            additional_context += f"Category: {category}\n"

        try:
            response = await rag_engine.async_generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.2,
                max_tokens=800,
                use_rag=True,
                category=category,
                city=city,
                additional_context=additional_context,
                history=history,
            )

            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                else:
                    result = {"conflict_summary": conflict_description, "raw_response": response}

            result["agent"] = self.name
            result["input_query"] = conflict_description
            return result

        except Exception as e:
            logger.error(f"Async conflict resolution error: {e}")
            return {"error": str(e), "conflict_summary": conflict_description, "agent": self.name}


# Singleton
conflict_resolver = ConflictResolverAgent()

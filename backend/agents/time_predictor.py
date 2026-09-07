"""
Objective 2: Time-Aware Prediction Agent
Predicts future compliance violations (6-12 months ahead) and outputs
probabilistic compliance roadmaps with confidence intervals.
"""

import json
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.services.rag_engine import rag_engine

logger = logging.getLogger(__name__)

TIME_PREDICTOR_SYSTEM_PROMPT = """You are a **Time-Aware Compliance Prediction Agent** specializing in Indian construction and zoning law. Your role is to predict future compliance violations 6-12 months ahead based on historical code changes, political signals, and construction project timelines.

## Your Expertise:
- Historical analysis of Indian construction code changes (2018-2025)
- Regulatory trend analysis for Bangalore, Chennai, Delhi, Mumbai, Hyderabad
- Construction project timeline risk assessment
- Probabilistic compliance risk modeling
- Identifying early warning indicators for regulatory changes

## Key Data You Use:
- 2,500+ historical code changes across Indian cities
- Political cycles, court orders, environmental events
- Industry trends, public pressure patterns
- Infrastructure development timelines
- International regulatory alignment trends

## Your Process:
1. **Analyze current status**: What regulations currently apply to the project?
2. **Identify trend indicators**: What signals suggest future changes?
3. **Predict changes**: What specific regulatory changes are likely?
4. **Assess risk**: What is the probability of each predicted change?
5. **Build roadmap**: Create a compliance roadmap with milestones
6. **Estimate impact**: Financial and timeline impact of each change

## Response Format (JSON):
{
    "project_analysis": {
        "current_regulations": ["list of current applicable regulations"],
        "compliance_status": "current compliance assessment"
    },
    "predictions": [
        {
            "change_type": "Type of predicted change",
            "description": "What change is expected",
            "probability": 0.75,
            "confidence_interval": {"lower": 0.60, "upper": 0.85},
            "predicted_timeframe_months": 8,
            "key_indicators": ["list of indicators supporting this prediction"],
            "source_law_affected": "The law likely to be amended",
            "impact_description": "How this affects the project"
        }
    ],
    "compliance_roadmap": {
        "milestones": [
            {
                "milestone": "Description",
                "timeline_months": 3,
                "action_required": "What to do",
                "risk_level": "Low/Medium/High",
                "estimated_cost_impact": "Description of cost impact"
            }
        ],
        "overall_risk_score": 0.65,
        "overall_risk_level": "Medium",
        "total_estimated_cost_impact": "Description"
    },
    "historical_precedents": [
        {
            "year": 2022,
            "city": "Delhi",
            "event": "Description of similar past event",
            "outcome": "What happened and how it was resolved"
        }
    ],
    "proactive_recommendations": [
        {
            "action": "Recommended action",
            "priority": "High/Medium/Low",
            "timeline": "When to act",
            "rationale": "Why this action is recommended"
        }
    ],
    "monitoring_plan": {
        "frequency": "How often to monitor",
        "key_triggers": ["events that trigger reassessment"],
        "review_dates": ["suggested review dates"]
    },
    "confidence_score": 0.72
}
"""


class TimePredictorAgent:
    """Agent that predicts future compliance violations."""

    def __init__(self):
        self.name = "Time-Aware Prediction Agent"
        self.system_prompt = TIME_PREDICTOR_SYSTEM_PROMPT

    def predict(
        self,
        project_description: str,
        city: str = None,
        project_timeline: dict = None,
        current_permits: list[str] = None,
    ) -> dict:
        """Predict future compliance violations for a project."""

        query = f"Predict compliance risks and future violations for: {project_description}"

        additional_context = ""
        if city:
            additional_context += f"Project city: {city}\n"
        if project_timeline:
            additional_context += f"Timeline: {json.dumps(project_timeline)}\n"
        if current_permits:
            additional_context += f"Current permits: {', '.join(current_permits)}\n"

        try:
            response = rag_engine.generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.4,
                max_tokens=800,
                use_rag=True,
                city=city,
                category=None,
                additional_context=additional_context,
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
                    result = {
                        "project_analysis": {"compliance_status": "Analysis generated"},
                        "raw_response": response,
                        "confidence_score": 0.5,
                    }

            result["agent"] = self.name
            result["input_query"] = project_description
            return result

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "error": str(e),
                "project_description": project_description,
                "agent": self.name,
            }

    async def async_predict(
        self,
        project_description: str,
        city: str = None,
        project_timeline: dict = None,
        current_permits: list[str] = None,
        history: list[dict] = None,
    ) -> dict:
        """Async prediction."""

        query = f"Predict compliance risks and future violations for: {project_description}"

        additional_context = ""
        if city:
            additional_context += f"Project city: {city}\n"
        if project_timeline:
            additional_context += f"Timeline: {json.dumps(project_timeline)}\n"
        if current_permits:
            additional_context += f"Current permits: {', '.join(current_permits)}\n"

        try:
            response = await rag_engine.async_generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.4,
                max_tokens=800,
                use_rag=True,
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
                else:
                    result = {"raw_response": response, "confidence_score": 0.5}

            result["agent"] = self.name
            return result

        except Exception as e:
            logger.error(f"Async prediction error: {e}")
            return {"error": str(e), "agent": self.name}


# Singleton
time_predictor = TimePredictorAgent()

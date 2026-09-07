"""
Objective 3: Verification & Reporting Agent
Produces inspector-ready, legally defensible compliance reports with
traceable reasoning chains and minimum-change recommendations.
"""

import json
import logging
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.services.rag_engine import rag_engine

logger = logging.getLogger(__name__)

VERIFIER_SYSTEM_PROMPT = """You are a **Compliance Verification & Reporting Agent** specializing in Indian construction law. Your role is to produce inspector-ready, legally defensible compliance reports with traceable reasoning chains.

## Your Expertise:
- Construction compliance inspection and verification
- Indian construction laws (all metropolitan cities)
- Structural safety, fire safety, environmental compliance
- Building plan approval verification
- RERA compliance assessment
- Legal documentation and evidence trail creation

## Your Process:
1. **Review project details**: Building type, size, location, permits.
2. **Check each regulation**: Against the knowledge base of 67+ laws.
3. **Identify findings**: Categorize as Critical, Major, Minor, Observation, or Compliant.
4. **Generate reasoning chain**: Document step-by-step compliance analysis.
5. **Create report**: Inspector-ready format with traceable evidence.
6. **Recommend minimum changes**: Minimum-change recommendations for compliance.

## Response Format (JSON):
{
    "report_metadata": {
        "report_id": "RPT-XXXX-YYYY",
        "report_type": "Compliance Certificate/Non-Compliance Notice/etc.",
        "generated_date": "YYYY-MM-DD",
        "reporting_authority": "The authority context",
        "legal_disclaimer": "Standard disclaimer"
    },
    "project_summary": {
        "building_type": "...",
        "project_size": "...",
        "location": "...",
        "applicable_regulations": ["list of applicable laws"]
    },
    "inspection_findings": [
        {
            "finding_id": "F001",
            "category": "Building Construction/Environment/Water/etc.",
            "sub_category": "...",
            "severity": "Critical/Major/Minor/Observation/Compliant",
            "description": "Detailed finding description",
            "applicable_regulation": "The specific regulation",
            "reference_section": "Section/rule reference",
            "measured_value": "What was measured/observed",
            "required_value": "What is required by law",
            "status": "Pass/Fail/Partial",
            "evidence": {
                "measurement": "...",
                "photograph_reference": "...",
                "document_reference": "..."
            }
        }
    ],
    "compliance_summary": {
        "total_parameters_checked": 15,
        "critical_findings": 0,
        "major_findings": 2,
        "minor_findings": 3,
        "observations": 1,
        "compliant_items": 9,
        "compliance_percentage": 60.0,
        "overall_status": "Partially Compliant"
    },
    "reasoning_chain": [
        "Step 1: Verified building type against zoning regulations...",
        "Step 2: Checked setback requirements...",
        "..."
    ],
    "minimum_change_recommendations": [
        {
            "priority": 1,
            "finding": "Description of finding",
            "current_state": "Current non-compliant state",
            "required_change": "Minimum change needed",
            "estimated_cost": "₹XX,XXX",
            "timeline": "X weeks/months",
            "regulation_reference": "The regulation that requires this change"
        }
    ],
    "executive_summary": "Plain language summary for stakeholders",
    "certification": {
        "status": "Compliant/Non-Compliant/Conditionally Compliant",
        "conditions": ["list of conditions if any"],
        "reinspection_required": true/false,
        "reinspection_date": "YYYY-MM-DD if applicable"
    },
    "confidence_score": 0.88
}
"""


class VerifierAgent:
    """Agent that produces compliance verification reports."""

    def __init__(self):
        self.name = "Verification & Reporting Agent"
        self.system_prompt = VERIFIER_SYSTEM_PROMPT

    def generate_report(
        self,
        project_description: str,
        city: str = None,
        category: str = None,
        inspection_details: dict = None,
        scope: str = "full",
    ) -> dict:
        """Generate a compliance verification report."""

        query = f"Generate a compliance verification report for: {project_description}"

        additional_context = f"Scope: {scope} compliance verification\n"
        if city:
            additional_context += f"Project city: {city}\n"
        if category:
            additional_context += f"Verification category: {category}\n"
        if inspection_details:
            additional_context += f"Inspection details: {json.dumps(inspection_details)}\n"

        try:
            response = rag_engine.generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.1,
                max_tokens=800,
                use_rag=True,
                category=category,
                city=city,
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
                        "report_metadata": {
                            "report_id": f"RPT-{datetime.now().strftime('%Y%m%d%H%M')}",
                            "report_type": "Compliance Report",
                            "generated_date": datetime.now().strftime("%Y-%m-%d"),
                        },
                        "raw_response": response,
                        "confidence_score": 0.5,
                    }

            result["agent"] = self.name
            result["input_query"] = project_description
            return result

        except Exception as e:
            logger.error(f"Verification report error: {e}")
            return {
                "error": str(e),
                "project_description": project_description,
                "agent": self.name,
            }

    async def async_generate_report(
        self,
        project_description: str,
        city: str = None,
        category: str = None,
        inspection_details: dict = None,
        scope: str = "full",
        history: list[dict] = None,
    ) -> dict:
        """Async report generation."""

        query = f"Generate a compliance verification report for: {project_description}"

        additional_context = f"Scope: {scope} compliance verification\n"
        if city:
            additional_context += f"Project city: {city}\n"
        if inspection_details:
            additional_context += f"Details: {json.dumps(inspection_details)}\n"

        try:
            response = await rag_engine.async_generate(
                query=query,
                system_prompt=self.system_prompt,
                model_key="primary",
                temperature=0.1,
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
                else:
                    result = {"raw_response": response, "confidence_score": 0.5}

            result["agent"] = self.name
            return result

        except Exception as e:
            logger.error(f"Async verification error: {e}")
            return {"error": str(e), "agent": self.name}


# Singleton
verifier = VerifierAgent()

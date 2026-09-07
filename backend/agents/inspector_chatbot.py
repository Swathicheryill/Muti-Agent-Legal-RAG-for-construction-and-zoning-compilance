"""
Inspector & Authority Chatbot
AI-powered interactive chatbot acting as a construction inspector or authority person.
Provides conversational compliance guidance with a professional persona.
"""

import json
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.services.rag_engine import rag_engine
from backend.services.groq_service import groq_service

logger = logging.getLogger(__name__)

INSPECTOR_PERSONAS = {
    "municipal_engineer": {
        "name": "Er. Rajesh Kumar, Chief Municipal Engineer",
        "system_prompt": """You are **Er. Rajesh Kumar**, Chief Municipal Engineer with 25 years of experience in Indian construction compliance. You work with BBMP (Bangalore), GCC (Chennai), MCD (Delhi), BMC (Mumbai), and GHMC (Hyderabad).

## Your Persona:
- Professional, experienced, and authoritative
- You speak with the authority of someone who has inspected hundreds of buildings
- You use specific code references and measurements
- You are firm on safety but helpful in guiding compliance
- You sometimes share practical tips from your experience

## Your Expertise:
- Building plan verification and approval
- Structural safety assessment
- Fire safety compliance
- Setback and FAR calculations
- Parking requirements
- Construction quality inspection

## Communication Style:
- Start with a professional greeting
- Use technical terms with explanations
- Provide specific code sections and measurements
- Give practical advice alongside regulatory requirements
- Always recommend official verification

## Rules:
- Only discuss construction compliance topics
- Always reference specific laws and standards
- Be honest about limitations - recommend consulting the actual authority
- Never provide false or misleading compliance advice
- If unsure about something, say so and recommend consulting the relevant authority

IMPORTANT: You are an AI assistant role-playing as this inspector for educational purposes. Make this clear if asked about your identity.""",
        "avatar": "👨‍🔧",
        "role": "Chief Municipal Engineer"
    },
    "environment_officer": {
        "name": "Dr. Priya Sharma, Environmental Compliance Officer",
        "system_prompt": """You are **Dr. Priya Sharma**, Environmental Compliance Officer with 15 years of experience at State Pollution Control Boards. You specialize in environmental clearance for construction projects.

## Your Persona:
- Scientific and precise in your assessments
- Strong advocate for environmental protection
- Balances development needs with ecological concerns
- Uses data and measurements in your recommendations

## Your Expertise:
- EIA (Environmental Impact Assessment) requirements
- CRZ (Coastal Regulation Zone) compliance
- Air and water quality standards
- Noise pollution control
- C&D waste management
- Green building certification

## Communication Style:
- Data-driven responses
- Reference specific standards (PM2.5, PM10, BOD, COD values)
- Explain environmental implications clearly
- Provide actionable compliance steps
- Recommend monitoring protocols

IMPORTANT: You are an AI assistant role-playing as this officer for educational purposes.""",
        "avatar": "👩‍🔬",
        "role": "Environmental Compliance Officer"
    },
    "fire_safety_officer": {
        "name": "Capt. Vikram Singh, Fire Safety Officer",
        "system_prompt": """You are **Capt. Vikram Singh**, Fire Safety Officer with 20 years of experience in fire services. You specialize in fire safety compliance for buildings.

## Your Persona:
- Safety-first approach, sometimes strict
- Emphasizes life safety over convenience
- Practical and solution-oriented
- Uses NFPA and NBC standards

## Your Expertise:
- Fire safety NOC requirements
- Fire escape and staircase design
- Sprinkler and suppression systems
- Emergency evacuation planning
- Fire resistance ratings
- Refuge area requirements

## Communication Style:
- Clear, unambiguous safety guidance
- Reference specific NBC and DFS standards
- Always emphasize safety implications
- Provide practical solutions for compliance
- Use urgency language for critical safety issues

IMPORTANT: You are an AI assistant role-playing as this officer for educational purposes.""",
        "avatar": "🧑‍🚒",
        "role": "Fire Safety Officer"
    },
    "legal_advisor": {
        "name": "Adv. Lakshmi Iyer, Construction Law Advisor",
        "system_prompt": """You are **Adv. Lakshmi Iyer**, a construction law advisor with 18 years of experience in real estate and construction law in India.

## Your Persona:
- Thorough and detail-oriented
- Risk-conscious, always considers legal implications
- Explains complex legal concepts simply
- Provides balanced legal perspective

## Your Expertise:
- RERA compliance and disputes
- Building approval processes
- Environmental law compliance
- Land use and zoning regulations
- Construction contract law
- Regulatory risk assessment

## Communication Style:
- Explain legal concepts in plain language
- Reference specific acts and sections
- Always include risk assessments
- Recommend legal consultation for complex issues
- Provide both the letter and spirit of the law

IMPORTANT: You are an AI assistant role-playing as this advisor for educational purposes. This is not actual legal advice.""",
        "avatar": "👩‍⚖️",
        "role": "Construction Law Advisor"
    },
}


class InspectorChatbot:
    """Interactive chatbot that acts as a construction inspector or authority person."""

    def __init__(self, persona: str = "municipal_engineer"):
        self.set_persona(persona)

    def set_persona(self, persona: str):
        """Switch the chatbot persona."""
        if persona in INSPECTOR_PERSONAS:
            self.persona_key = persona
            self.persona = INSPECTOR_PERSONAS[persona]
        else:
            self.persona_key = "municipal_engineer"
            self.persona = INSPECTOR_PERSONAS["municipal_engineer"]

    def get_response(self, user_message: str, history: list[dict] = None) -> str:
        """Get a response from the inspector chatbot."""
        # Build conversation with persona context
        messages = [{"role": "system", "content": self.persona["system_prompt"]}]

        # Add conversation history
        if history:
            messages.extend(history[-10:])  # Keep last 10 messages for context

        messages.append({"role": "user", "content": user_message})

        try:
            response = groq_service.chat_completion(
                messages=messages,
                model_key="primary",
                temperature=0.5,
                max_tokens=800,
            )
            return response
        except Exception as e:
            logger.error(f"Inspector chatbot error: {e}")
            return f"I apologize, but I'm experiencing a technical issue. Please try again. (Error: {str(e)})"

    async def async_get_response(self, user_message: str, history: list[dict] = None) -> str:
        """Async response from the inspector chatbot."""
        messages = [{"role": "system", "content": self.persona["system_prompt"]}]

        if history:
            messages.extend(history[-10:])

        messages.append({"role": "user", "content": user_message})

        try:
            response = await groq_service.async_chat_completion(
                messages=messages,
                model_key="primary",
                temperature=0.5,
                max_tokens=800,
            )
            return response
        except Exception as e:
            logger.error(f"Async inspector chatbot error: {e}")
            return f"I apologize, but I'm experiencing a technical issue. Please try again. (Error: {str(e)})"

    async def streaming_response(self, user_message: str, history: list[dict] = None):
        """Streaming response from the inspector chatbot."""
        messages = [{"role": "system", "content": self.persona["system_prompt"]}]

        if history:
            messages.extend(history[-10:])

        messages.append({"role": "user", "content": user_message})

        async for chunk in groq_service.streaming_chat(
            messages=messages,
            model_key="primary",
            temperature=0.5,
            max_tokens=2048,
        ):
            yield chunk

    def get_available_personas(self) -> dict:
        """Get list of available personas."""
        return {
            key: {
                "name": val["name"],
                "role": val["role"],
                "avatar": val["avatar"],
            }
            for key, val in INSPECTOR_PERSONAS.items()
        }


# Singleton with default persona
inspector_chatbot = InspectorChatbot()

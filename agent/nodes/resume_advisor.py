"""Node 6: Suggest resume tweaks tailored to the target company."""

import os
from langchain_anthropic import ChatAnthropic
from agent.utils import parse_json_from_response

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3,
)

PROMPT = """You are a resume strategist. Given this resume and target company,
suggest specific tweaks to make the resume more compelling for THIS company.

RESUME TEXT:
{resume_text}

TARGET COMPANY: {company}
THEIR PAIN POINTS: {pain_points}
THEIR TECH STACK: {tech_stack}
MY SKILL GAPS FOR THIS COMPANY: {gaps}
MY STRONG MATCHES: {matches}

Return ONLY valid JSON (no markdown, no explanation) with these exact keys:
{{
    "resume_tweaks": [
        {{
            "section": "which section to change",
            "current_text": "what it currently says (quote from resume)",
            "suggested_text": "what it should say instead",
            "reason": "why this change helps for this company"
        }}
    ],
    "tailored_summary": "A completely rewritten 2-3 sentence professional summary targeting this specific company"
}}"""


def resume_advisor_node(state: dict) -> dict:
    """Suggest resume tweaks specific to the target company."""
    response = llm.invoke(PROMPT.format(
        resume_text=state.get("resume_text", "")[:3000],  # Limit to avoid token overflow
        company=state.get("company_name", ""),
        pain_points=state.get("company_pain_points", []),
        tech_stack=state.get("company_tech_stack", []),
        gaps=state.get("gaps", []),
        matches=state.get("skill_matches", [])[:5],
    ))
    parsed = parse_json_from_response(response.content)

    return {
        "resume_tweaks": parsed.get("resume_tweaks", []),
        "tailored_summary": parsed.get("tailored_summary", ""),
    }

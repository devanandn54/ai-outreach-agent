"""Node 3: Match resume skills to company pain points."""

import os
from langchain_anthropic import ChatAnthropic
from agent.utils import parse_json_from_response

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0,
)

PROMPT = """You are a strategic career advisor.

MY SKILLS: {skills}
MY EXPERIENCE: {experience}
MY STRENGTHS: {strengths}

TARGET COMPANY: {company}
THEIR PAIN POINTS: {pain_points}
THEIR TECH STACK: {tech_stack}
THEIR JOB SIGNALS: {job_signals}

Analyze the overlap between my skills and their needs.

Return ONLY valid JSON (no markdown, no explanation) with these exact keys:
{{
    "skill_matches": [
        {{"skill": "my skill", "their_need": "what they need", "match_strength": "strong"}}
    ],
    "value_propositions": ["specific way I can help them 1", "way 2", "way 3"],
    "gaps": ["skill they need that I lack 1", "gap 2"]
}}"""


def gap_analyzer_node(state: dict) -> dict:
    """Match user's skills against company's pain points."""
    response = llm.invoke(PROMPT.format(
        skills=state.get("resume_skills", []),
        experience=state.get("resume_experience_summary", ""),
        strengths=state.get("resume_strengths", []),
        company=state.get("company_name", ""),
        pain_points=state.get("company_pain_points", []),
        tech_stack=state.get("company_tech_stack", []),
        job_signals=state.get("company_job_signals", []),
    ))
    parsed = parse_json_from_response(response.content)

    return {
        "skill_matches": parsed.get("skill_matches", []),
        "value_propositions": parsed.get("value_propositions", []),
        "gaps": parsed.get("gaps", []),
    }

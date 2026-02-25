"""Node 1: Parse and analyze the uploaded resume."""

import os
from langchain_anthropic import ChatAnthropic
from agent.tools.doc_parser import extract_text
from agent.utils import parse_json_from_response

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0,
)

PROMPT = """Analyze this resume and extract structured information.

Resume text:
{resume_text}

Return ONLY valid JSON (no markdown, no explanation) with these exact keys:
{{
    "skills": ["skill1", "skill2", ...],
    "experience_summary": "2-3 sentence summary of their experience",
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["gap1", "gap2", ...]
}}"""


def resume_parser_node(state: dict) -> dict:
    """Parse resume and analyze skills, strengths, weaknesses."""
    resume_text = extract_text(state["resume_path"])

    response = llm.invoke(PROMPT.format(resume_text=resume_text))
    parsed = parse_json_from_response(response.content)

    return {
        "resume_text": resume_text,
        "resume_skills": parsed.get("skills", []),
        "resume_experience_summary": parsed.get("experience_summary", ""),
        "resume_strengths": parsed.get("strengths", []),
        "resume_weaknesses": parsed.get("weaknesses", []),
    }

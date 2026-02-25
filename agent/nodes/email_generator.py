"""Node 5: Generate personalized outreach emails."""

import os
from langchain_anthropic import ChatAnthropic
from agent.utils import parse_json_from_response

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.7,
)

PROMPT = """Write 3 cold outreach email variants to {recipient_name} ({recipient_title})
at {company}.

CONTEXT:
- Company overview: {overview}
- Their pain points: {pain_points}
- How I can help: {value_propositions}
- My strongest skill matches: {skill_matches}
- My experience: {experience}
- Recent company news: {recent_news}

RULES:
- Under 150 words each
- Lead with THEIR pain, not my pitch
- Reference something specific about their company
- Sound human, not a template
- Soft CTA — don't demand a meeting
- NO buzzwords like synergy, leverage, game-changer

Return ONLY a valid JSON array (no markdown, no explanation):
[
    {{
        "variant": "Direct Value",
        "subject_line": "subject here",
        "body": "email body here",
        "strategy": "why this approach works",
        "recipient": "{recipient_name}"
    }},
    {{
        "variant": "Empathy Hook",
        "subject_line": "subject here",
        "body": "email body here",
        "strategy": "why this approach works",
        "recipient": "{recipient_name}"
    }},
    {{
        "variant": "Insight Gift",
        "subject_line": "subject here",
        "body": "email body here",
        "strategy": "why this approach works",
        "recipient": "{recipient_name}"
    }}
]"""


def email_generator_node(state: dict) -> dict:
    """Generate 3 outreach email variants per leadership contact."""
    all_emails = []
    contacts = state.get("leadership_contacts", [])

    # If no contacts found, create emails for the target role generically
    if not contacts:
        contacts = [{"name": state.get("target_role", "CTO"), "title": state.get("target_role", "CTO")}]

    for contact in contacts:
        name = contact.get("name", "Hiring Manager")
        title = contact.get("title", state.get("target_role", "CTO"))

        response = llm.invoke(PROMPT.format(
            recipient_name=name,
            recipient_title=title,
            company=state.get("company_name", ""),
            overview=state.get("company_overview", ""),
            pain_points=state.get("company_pain_points", []),
            value_propositions=state.get("value_propositions", []),
            skill_matches=state.get("skill_matches", [])[:5],
            experience=state.get("resume_experience_summary", ""),
            recent_news=state.get("company_recent_news", [])[:3],
        ))
        parsed = parse_json_from_response(response.content)

        if isinstance(parsed, list):
            all_emails.extend(parsed)
        elif isinstance(parsed, dict) and not parsed.get("parse_error"):
            all_emails.append(parsed)

    return {"generated_emails": all_emails}

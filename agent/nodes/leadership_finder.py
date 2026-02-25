"""Node 4: Find company leadership contacts."""

import os
from langchain_anthropic import ChatAnthropic
from agent.tools.search import search_company
from agent.utils import parse_json_from_response, format_results

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0,
)

PROMPT = """From these search results, extract leadership contacts for {company}.
Focus on: {target_role}, CEO, VP Engineering, Head of Engineering.

SEARCH RESULTS:
{results}

Return ONLY a valid JSON array (no markdown, no explanation):
[
    {{
        "name": "Person Name",
        "title": "Their Title",
        "linkedin_url": "URL or empty string",
        "email_guess": "best guess email or empty string"
    }}
]

If you can't find specific people, return an array with at least one entry using 
the company name and target role with empty strings for unknown fields."""


def leadership_finder_node(state: dict) -> dict:
    """Find leadership contacts via web search."""
    company = state.get("company_name", "")
    target = state.get("target_role", "CTO")

    results = search_company(f"{company} {target} LinkedIn", max_results=5)
    results += search_company(f"{company} leadership team engineering", max_results=3)

    formatted = format_results(results)

    response = llm.invoke(
        PROMPT.format(company=company, target_role=target, results=formatted)
    )
    parsed = parse_json_from_response(response.content)

    # Ensure it's a list
    if isinstance(parsed, dict):
        parsed = [parsed]

    return {"leadership_contacts": parsed}

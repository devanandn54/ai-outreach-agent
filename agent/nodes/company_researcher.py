"""Node 2: Deep company research using web search."""

import os
from langchain_anthropic import ChatAnthropic
from agent.tools.search import search_company
from agent.utils import parse_json_from_response, format_results

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0,
)

SYNTHESIS_PROMPT = """Based on these search results about {company}, extract structured intelligence.

SEARCH RESULTS:
{results}

Return ONLY valid JSON (no markdown, no explanation) with these exact keys:
{{
    "overview": "what the company does in 2-3 sentences",
    "industry": "their industry",
    "stage": "startup/scaleup/enterprise",
    "problem_solved": "the core problem they solve for customers",
    "tech_stack": ["tech1", "tech2"],
    "pain_points": ["pain point 1", "pain point 2"],
    "recent_news": ["news item 1", "news item 2"],
    "job_signals": ["signal from job postings 1", "signal 2"]
}}"""


def company_researcher_node(state: dict) -> dict:
    """Run multiple web searches and synthesize company intelligence."""
    company = state["company_name"]
    all_results = []

    queries = [
        f"{company} company what do they do",
        f"{company} funding investors crunchbase",
        f"{company} engineering blog tech stack",
        f"{company} careers jobs engineering",
        f"{company} news challenges 2025",
        f"{company} CTO VP engineering leadership",
    ]

    for query in queries:
        results = search_company(query, max_results=3)
        all_results.extend(results)

    formatted = format_results(all_results)

    response = llm.invoke(
        SYNTHESIS_PROMPT.format(company=company, results=formatted)
    )
    parsed = parse_json_from_response(response.content)

    return {
        "company_overview": parsed.get("overview", ""),
        "company_industry": parsed.get("industry", ""),
        "company_stage": parsed.get("stage", ""),
        "company_problem_solved": parsed.get("problem_solved", ""),
        "company_tech_stack": parsed.get("tech_stack", []),
        "company_pain_points": parsed.get("pain_points", []),
        "company_recent_news": parsed.get("recent_news", []),
        "company_job_signals": parsed.get("job_signals", []),
        "raw_search_results": all_results,
    }

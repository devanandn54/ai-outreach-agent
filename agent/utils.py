"""Shared utilities for the outreach agent."""

import json
import re


def parse_json_from_response(text: str):
    """Extract JSON from Claude's response, handling markdown fences and edge cases."""
    # Strip markdown code fences
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON array first, then object
    for pattern in [r"\[[\s\S]*\]", r"\{[\s\S]*\}"]:
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                continue

    # Fallback: return raw text in a wrapper
    return {"raw": text, "parse_error": True}


def format_results(results: list) -> str:
    """Format search results into a readable string for LLM prompts."""
    formatted = []
    for r in results:
        if isinstance(r, dict):
            formatted.append(
                f"Title: {r.get('title', 'N/A')}\n"
                f"URL: {r.get('url', 'N/A')}\n"
                f"Content: {r.get('content', 'N/A')}\n"
            )
        else:
            formatted.append(str(r))
    return "\n---\n".join(formatted)

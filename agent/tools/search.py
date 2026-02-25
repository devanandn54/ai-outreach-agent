"""Tavily web search wrapper."""

import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_company(query: str, max_results: int = 5) -> list:
    """Search the web and return structured results."""
    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
        )
        return response.get("results", [])
    except Exception as e:
        print(f"Search error for '{query}': {e}")
        return []

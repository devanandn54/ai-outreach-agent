"""LangGraph state machine — the brain of the agent."""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.resume_parser import resume_parser_node
from agent.nodes.company_researcher import company_researcher_node
from agent.nodes.gap_analyzer import gap_analyzer_node
from agent.nodes.leadership_finder import leadership_finder_node
from agent.nodes.email_generator import email_generator_node
from agent.nodes.resume_advisor import resume_advisor_node


def build_agent():
    """Build and compile the LangGraph agent."""
    graph = StateGraph(AgentState)

    # Add all nodes
    graph.add_node("parse_resume", resume_parser_node)
    graph.add_node("research_company", company_researcher_node)
    graph.add_node("analyze_gaps", gap_analyzer_node)
    graph.add_node("find_leadership", leadership_finder_node)
    graph.add_node("generate_emails", email_generator_node)
    graph.add_node("advise_resume", resume_advisor_node)

    # Define SEQUENTIAL flow (avoids parallel execution issues)
    # Step 1: Parse resume
    graph.set_entry_point("parse_resume")
    # Step 2: Research company
    graph.add_edge("parse_resume", "research_company")
    # Step 3: Analyze gaps (needs both resume + company data)
    graph.add_edge("research_company", "analyze_gaps")
    # Step 4: Find leadership (needs company data)
    graph.add_edge("analyze_gaps", "find_leadership")
    # Step 5: Generate emails (needs gaps + leadership)
    graph.add_edge("find_leadership", "generate_emails")
    # Step 6: Advise on resume tweaks (needs gaps + company data)
    graph.add_edge("generate_emails", "advise_resume")
    # Done
    graph.add_edge("advise_resume", END)

    return graph.compile()


# Create the compiled agent
agent = build_agent()


def run_agent(company_name: str, resume_path: str, target_role: str = "CTO") -> dict:
    """Execute the full agent pipeline."""
    initial_state = {
        "company_name": company_name,
        "resume_path": resume_path,
        "target_role": target_role,
    }

    result = agent.invoke(initial_state)
    return result

"""Shared state schema for the outreach agent."""

from typing import TypedDict


class AgentState(TypedDict, total=False):
    """
    All keys are optional (total=False) so nodes can read/write
    only the keys they care about.
    """
    # --- Inputs ---
    company_name: str
    resume_path: str
    target_role: str

    # --- Node 1: Resume Parser ---
    resume_text: str
    resume_skills: list
    resume_experience_summary: str
    resume_strengths: list
    resume_weaknesses: list

    # --- Node 2: Company Researcher ---
    company_overview: str
    company_industry: str
    company_stage: str
    company_problem_solved: str
    company_tech_stack: list
    company_pain_points: list
    company_recent_news: list
    company_job_signals: list
    raw_search_results: list

    # --- Node 3: Gap Analyzer ---
    skill_matches: list
    value_propositions: list
    gaps: list

    # --- Node 4: Leadership Finder ---
    leadership_contacts: list

    # --- Node 5: Email Generator ---
    generated_emails: list

    # --- Node 6: Resume Advisor ---
    resume_tweaks: list
    tailored_summary: str

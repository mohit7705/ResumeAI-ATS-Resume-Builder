from backend.ai.analyzer import analyze_job_description
from backend.ai.matcher import match_skills
from backend.ai.project_ranker import rank_projects
from backend.ai.summary_generator import generate_summary
from backend.ai.project_rewriter import rewrite_projects
from backend.ai.ats_score import calculate_ats_score


def optimize_resume(job_description: str):
    """
    Build the final AI-optimized resume.
    """

    # Step 5.1
    analysis = analyze_job_description(
        job_description
    )

    # Step 5.2
    skill_match = match_skills(
        analysis["skills"]
    )

    # Step 5.3
    project_ranking = rank_projects(
        job_description
    )

    # Step 5.4
    summary = generate_summary(
    job_description,
    project_ranking["top_projects"],
    )

    # Step 5.5
    projects = rewrite_projects(
    job_description,
    project_ranking["top_projects"],
    )

    # Step 5.6
    ats_score = calculate_ats_score(
        skill_match,
        project_ranking,
    )

    return {
        "analysis": analysis,
        "skill_match": skill_match,
        "project_ranking": project_ranking,
        "summary": summary,
        "projects": projects,
        "ats_score": ats_score,
    }
from backend.ai.resume_optimizer import optimize_resume

from backend.data.personal_loader import load_personal_data

from backend.resume.builder import build_resume
from backend.resume.validator import validate_resume


def generate_resume(job_description: str):

    personal = load_personal_data()

    ai_result = optimize_resume(
        job_description
    )

    resume = build_resume(
        personal=personal,
        summary=ai_result["summary"],
        skills=personal["skills"],
        projects=ai_result["projects"],
    )

    validation = validate_resume(resume)

    return {
        "resume": resume,
        "validation": validation,
        "ats_score": ai_result["ats_score"],
        "skill_match": ai_result["skill_match"],
        "project_ranking": ai_result["project_ranking"],
    }
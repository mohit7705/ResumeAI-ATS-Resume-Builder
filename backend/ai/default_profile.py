"""Build the input for the default, general-purpose resume."""

from backend.data.personal_loader import load_personal_data
from backend.resume.engine import SKILL_CATEGORIES, get_enabled_skill_categories


DEFAULT_TITLE_FALLBACK = "B.Tech Student (Artificial Intelligence & Machine Learning)"

CATEGORY_LABELS = {
    "languages": "Programming languages",
    "ai_ml": "AI and machine learning",
    "databases": "Databases",
    "cs_fundamentals": "Computer science fundamentals",
    "tools": "Tools and frameworks",
    "cloud": "Cloud platforms",
    "soft_skills": "Soft skills",
}


def build_default_job_description() -> tuple[str, str]:
    """Return (job_description, professional_title) for the default resume."""
    personal = load_personal_data()
    pool = get_enabled_skill_categories(personal.get("skills", {}))

    lines = []
    for category in SKILL_CATEGORIES:
        skills = pool.get(category, [])
        if skills:
            lines.append(f"- {CATEGORY_LABELS[category]}: {', '.join(skills)}")

    if not lines:
        raise ValueError(
            "Add and enable your technical skills first, then generate the default resume."
        )

    job_description = (
        "General-purpose entry-level software engineering role.\n\n"
        "Responsibilities:\n"
        "- Design, build, test and maintain reliable software and APIs\n"
        "- Work with data, databases and machine learning where relevant\n"
        "- Write clean, documented code and collaborate with a team\n"
        "- Learn new tools quickly and deliver working projects\n\n"
        "Requirements:\n" + "\n".join(lines) + "\n"
    )

    profile = personal.get("profile", {})
    title = str(profile.get("professional_title") or "").strip() or DEFAULT_TITLE_FALLBACK
    return job_description, title

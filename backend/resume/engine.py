from backend.ai.resume_optimizer import optimize_resume
from backend.data.personal_loader import load_personal_data
from backend.resume.builder import build_resume
from backend.resume.skill_selector import select_skills
from backend.resume.recruiter_check import recruiter_check
from backend.resume.validator import validate_resume


SKILL_CATEGORIES = (
    "languages",
    "ai_ml",
    "databases",
    "cs_fundamentals",
    "tools",
    "cloud",
    "soft_skills",
)


SKILL_ALIASES = {
    "rest apis": "rest api",
    "rest api development": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "azure": "microsoft azure",
    "gcp": "google cloud platform",
    "object oriented programming": "object-oriented programming",
    "oops": "object-oriented programming",
    "database management systems": "dbms",
    "computer network": "computer networks",
}


PROJECT_SKILL_CATEGORIES = {
    "python": "languages",
    "java": "languages",
    "javascript": "languages",
    "typescript": "languages",
    "c": "languages",
    "c++": "languages",
    "sql": "languages",
    "machine learning": "ai_ml",
    "deep learning": "ai_ml",
    "tensorflow": "ai_ml",
    "pytorch": "ai_ml",
    "scikit-learn": "ai_ml",
    "shap": "ai_ml",
    "vision ai": "ai_ml",
    "gemini ai": "ai_ml",
    "gemini api": "ai_ml",
    "ollama": "ai_ml",
    "langgraph": "ai_ml",
    "rag": "ai_ml",
    "vector embeddings": "ai_ml",
    "postgresql": "databases",
    "mysql": "databases",
    "mongodb": "databases",
    "sqlite": "databases",
    "git": "tools",
    "github": "tools",
    "docker": "tools",
    "fastapi": "tools",
    "flask": "tools",
    "django": "tools",
    "rest api": "tools",
    "linux": "tools",
    "ffmpeg": "tools",
    "whisper": "tools",
    "faster-whisper": "tools",
    "opencv": "tools",
    "yt-dlp": "tools",
    "razorpay": "tools",
    "aws": "cloud",
    "microsoft azure": "cloud",
    "google cloud platform": "cloud",
    "vertex ai": "cloud",
    "cloud run": "cloud",
    "vercel": "cloud",
    "render": "cloud",
    "kubernetes": "tools",
}


# Related skills are evidence to highlight, not proof of proficiency
# in the missing skill itself.
RELATED_SKILLS = {
    "kubernetes": [
        "Docker",
        "Linux",
        "AWS",
        "Microsoft Azure",
        "Google Cloud Platform",
    ],
    "docker": [
        "Linux",
        "Kubernetes",
        "AWS",
        "Microsoft Azure",
        "Google Cloud Platform",
    ],
    "machine learning": [
        "Python",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
    ],
    "deep learning": [
        "Machine Learning",
        "TensorFlow",
        "PyTorch",
    ],
    "cloud computing": [
        "AWS",
        "Microsoft Azure",
        "Google Cloud Platform",
    ],
    "rest api": [
        "FastAPI",
        "Flask",
        "Django",
    ],
    "sql": [
        "PostgreSQL",
        "MySQL",
        "SQLite",
    ],
}


def normalize_skill(value):
    """Normalize capitalization, whitespace, and common skill aliases."""
    if not isinstance(value, str):
        return ""

    key = " ".join(value.strip().casefold().split())
    return SKILL_ALIASES.get(key, key)


def unique_skills(skills):
    """Remove duplicate skills while preserving their original spelling."""
    result = []
    seen = set()

    for skill in skills:
        if not isinstance(skill, str) or not skill.strip():
            continue

        key = normalize_skill(skill)

        if key and key not in seen:
            result.append(skill.strip())
            seen.add(key)

    return result


def is_skill_relevant(skill: str, job_requirements: dict) -> bool:
    """Check whether a skill is explicitly or contextually relevant to a job."""
    skill_key = normalize_skill(skill)

    if not skill_key:
        return False

    job_text_parts = []

    for field in (
        "skills",
        "inferred_skills",
        "keywords",
        "responsibilities",
    ):
        values = job_requirements.get(field, [])

        if isinstance(values, list):
            job_text_parts.extend(
                value.casefold()
                for value in values
                if isinstance(value, str)
            )

    job_text = " ".join(job_text_parts)
    job_terms = {
        normalize_skill(value)
        for field in ("skills", "inferred_skills", "keywords")
        for value in job_requirements.get(field, [])
        if isinstance(value, str)
    }

    # Exact job-skill matches are the strongest relevance signal.
    if skill_key in job_terms:
        return True

    # Contextual rules prevent unrelated technologies from being included.
    context_rules = {
        "fastapi": (
            "backend development",
            "backend developer",
            "rest api",
            "restful api",
            "web services",
            "api development",
        ),
        "docker": (
            "docker",
            "containerization",
            "containerization",
            "devops",
            "deployment",
            "container orchestration",
        ),
        "git": (
            "git",
            "version control",
            "source control",
        ),
        "shap": (
            "shap",
            "explainable ai",
            "model interpretability",
            "model explainability",
            "interpretable machine learning",
        ),
    }

    allowed_contexts = context_rules.get(skill_key, ())

    return any(
        context in job_text
        for context in allowed_contexts
    )


def get_enabled_skill_categories(personal_skills: dict) -> dict:
    """Return only enabled categories and enabled skills."""
    enabled_categories = {}

    for category in SKILL_CATEGORIES:
        category_data = personal_skills.get(category, [])

        # Support the old list format for backward compatibility.
        if isinstance(category_data, list):
            enabled_categories[category] = unique_skills(category_data)
            continue

        if not isinstance(category_data, dict):
            continue

        if category_data.get("enabled", True) is not True:
            continue

        skills = category_data.get("skills", [])

        if not isinstance(skills, list):
            continue

        enabled_skills = []

        for skill in skills:
            if isinstance(skill, str):
                enabled_skills.append(skill)
                continue

            if not isinstance(skill, dict):
                continue

            if skill.get("enabled", True) is not True:
                continue

            name = skill.get("name")

            if isinstance(name, str) and name.strip():
                enabled_skills.append(name.strip())

        enabled_categories[category] = unique_skills(enabled_skills)

    return enabled_categories


def build_resume_skills(
    personal_skills: dict,
    projects: list,
    matching_skills: list,
    additional_resume_skills: list,
    matching_cs_fundamentals: list,
    confirmed_skills: list[str] | None = None,
    job_requirements: dict | None = None,
) -> dict:
    """Build Technical Skills for this job only from the enabled pool."""
    pool = get_enabled_skill_categories(personal_skills)
    matched = (
        list(matching_skills or [])
        + list(additional_resume_skills or [])
        + list(matching_cs_fundamentals or [])
    )
    return select_skills(
        pool=pool,
        projects=projects,
        job=job_requirements or {},
        matched=matched,
        confirmed=confirmed_skills or [],
    )


def build_skill_gap_recommendations(
    missing_skills: list,
    resume_skills: dict,
    projects: list,
) -> list:
    """Suggest relevant next steps for job skills not currently matched."""

    available = {
        normalize_skill(skill): skill
        for skills in resume_skills.values()
        if isinstance(skills, list)
        for skill in skills
        if isinstance(skill, str)
    }

    # Project technologies can provide additional context.
    project_technologies = set()

    for project in projects:
        if not isinstance(project, dict):
            continue

        technologies = project.get("technologies", [])

        if isinstance(technologies, list):
            project_technologies.update(
                normalize_skill(technology)
                for technology in technologies
                if isinstance(technology, str)
            )

    recommendations = []
    seen = set()

    for missing in missing_skills:
        if not isinstance(missing, str) or not missing.strip():
            continue

        key = normalize_skill(missing)

        if not key or key in seen:
            continue

        seen.add(key)

        related = RELATED_SKILLS.get(key, [])

        evidence = [
            skill
            for skill in related
            if normalize_skill(skill) in available
            or normalize_skill(skill) in project_technologies
        ]

        if evidence:
            action = (
                "Highlight the related skills and relevant project evidence. "
                "Do not claim proficiency in the missing skill without evidence."
            )
        else:
            action = (
                "Consider learning this skill and completing a practical "
                "project before listing it as a demonstrated skill."
            )

        recommendations.append(
            {
                "skill": missing.strip(),
                "status": "missing",
                "related_skills": evidence,
                "recommendation": action,
            }
        )

    return recommendations


def generate_resume(
    job_description: str,
    confirmed_skills: list[str] | None = None,
    target_title: str | None = None,
):
    """Generate a tailored resume and report any skill gaps.

    target_title: set only for title-based generation. It replaces the
    professional title shown under the name in the resume header.
    """

    personal = load_personal_data()
    ai_result = optimize_resume(job_description)

    skill_match = ai_result["skill_match"]
    confirmed_skills = confirmed_skills or []

    missing_list = skill_match.get("missing_skills", [])

    if not isinstance(missing_list, list):
        missing_list = []

    missing_keys = {
        normalize_skill(skill)
        for skill in missing_list
        if isinstance(skill, str) and normalize_skill(skill)
    }

    invalid_confirmations = [
        skill
        for skill in confirmed_skills
        if not isinstance(skill, str)
        or not skill.strip()
        or normalize_skill(skill) not in missing_keys
    ]

    if invalid_confirmations:
        raise ValueError(
            "Confirmed skills must come from the missing-skills list: "
            + ", ".join(str(skill) for skill in invalid_confirmations)
        )

    # Deduplicate confirmations without changing their displayed spelling.
    confirmed_skills = unique_skills(confirmed_skills)

    resume_skills = build_resume_skills(
        personal_skills=personal.get("skills", {}),
        projects=ai_result.get("projects", []),
        matching_skills=skill_match.get("matching_skills", []),
        additional_resume_skills=skill_match.get(
            "additional_resume_skills", []
        ),
        matching_cs_fundamentals=skill_match.get(
            "matching_cs_fundamentals", []
        ),
        confirmed_skills=confirmed_skills,
        job_requirements=ai_result.get("analysis", {}),
    )

    skill_gap_recommendations = build_skill_gap_recommendations(
        missing_skills=missing_list,
        resume_skills=resume_skills,
        projects=ai_result.get("projects", []),
    )

    resume = build_resume(
        personal=personal,
        summary=ai_result["summary"],
        skills=resume_skills,
        projects=ai_result.get("projects", []),
    )

    if target_title:
        resume.header["professional_title"] = target_title
    else:
        role = str((ai_result.get("analysis") or {}).get("role") or "").strip()
        if role and len(role) <= 42:
            resume.header["professional_title"] = (
                f"Aspiring {role} | B.Tech Student (AI & ML)"
            )
        else:
            resume.header["professional_title"] = (
                "B.Tech Student (Artificial Intelligence & Machine Learning)"
            )

    validation = validate_resume(
        resume,
        source_experience=personal.get("experience", []),
    )

    if not validation["experience_unchanged"]:
        raise ValueError("Experience section was modified. Resume stopped.")

    recruiter = recruiter_check(
        resume,
        ai_result["analysis"],
        personal.get("experience", []),
    )

    return {
        "resume": resume,
        "analysis": ai_result["analysis"],
        "validation": validation,
        "recruiter_check": recruiter,
        "ats_score": ai_result["ats_score"],
        "skill_match": skill_match,
        "project_ranking": ai_result["project_ranking"],
        "skill_gap_recommendations": skill_gap_recommendations,
    }

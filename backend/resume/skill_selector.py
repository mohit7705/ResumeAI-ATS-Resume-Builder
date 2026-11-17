"""Pick only the technical skills a fresher should show for one job."""

import re
from collections import Counter


MAX_TOTAL = 24
MAX_PER_CATEGORY = 6
MAX_SOFT = 6
MAX_LANGUAGES_WHEN_VAGUE = 3
MAX_OTHER_WHEN_VAGUE = 2

DEFAULT_SKILLS = (
    "Python", "SQL",
    "MySQL", "PostgreSQL", "MongoDB",
    "Git", "GitHub", "REST API", "FastAPI",
    "Object-Oriented Programming", "DBMS",
    "Data Structures and Algorithms", "Computer Networks",
    "AWS", "Microsoft Azure", "Render", "Vercel",
    "Problem Solving", "Critical Thinking",
)

# Cloud platforms always shown on the resume (candidate confirmed these).
DEFAULT_CLOUD = ("AWS", "Microsoft Azure", "Google Cloud Platform")

CATEGORY_ORDER = (
    "languages",
    "ai_ml",
    "databases",
    "tools",
    "cs_fundamentals",
    "cloud",
    "soft_skills",
)

TRIM_ORDER = (
    "soft_skills",
    "cloud",
    "cs_fundamentals",
    "tools",
    "databases",
    "ai_ml",
    "languages",
)

CATEGORY_TRIGGERS = {
    "languages": [
        "programming", "coding", "software development", "software engineer",
        "developer", "backend", "back-end", "frontend", "front-end",
        "full stack", "full-stack", "scripting", "automation",
    ],
    "databases": [
        "database", "databases", "sql", "nosql", "data storage", "dbms",
        "postgresql", "mysql", "mongodb", "data modeling", "queries",
    ],
    "ai_ml": [
        "machine learning", "ml", "ai", "artificial intelligence",
        "deep learning", "nlp", "data science", "data scientist",
        "generative ai", "genai", "llm", "computer vision", "neural",
    ],
    "tools": [
        "git", "github", "version control", "docker", "container", "api",
        "apis", "rest", "restful", "postman", "linux", "devops", "ci/cd",
        "testing", "debugging",
    ],
    "cloud": [
        "cloud", "aws", "azure", "gcp", "google cloud", "deployment",
        "hosting", "serverless",
    ],
    "cs_fundamentals": [
        "data structures", "algorithms", "dsa", "oop", "object-oriented",
        "object oriented", "operating system", "computer networks",
        "networking", "computer science fundamentals", "cs fundamentals",
        "dbms",
    ],
    "soft_skills": [
        "communication", "teamwork", "team player", "collaborat",
        "problem solving", "problem-solving", "interpersonal",
    ],
}

ALIASES = {
    "rest apis": "rest api", "restful api": "rest api",
    "restful apis": "rest api", "rest api development": "rest api",
    "scikit learn": "scikit-learn", "sklearn": "scikit-learn",
    "js": "javascript", "ts": "typescript", "postgres": "postgresql",
    "azure": "microsoft azure", "gcp": "google cloud platform",
    "oops": "object-oriented programming",
    "object oriented programming": "object-oriented programming",
    "dsa": "data structures and algorithms",
    "database management systems": "dbms",
    "computer network": "computer networks",
    "ml": "machine learning", "genai": "generative ai",
    "github": "git",
}

CONFIRMED_CATEGORY = {
    "python": "languages", "java": "languages", "javascript": "languages",
    "typescript": "languages", "sql": "languages", "c++": "languages",
    "machine learning": "ai_ml", "tensorflow": "ai_ml", "pytorch": "ai_ml",
    "postgresql": "databases", "mysql": "databases", "mongodb": "databases",
    "docker": "tools", "git": "tools", "linux": "tools", "fastapi": "tools",
    "aws": "cloud", "microsoft azure": "cloud",
}


def norm(value) -> str:
    if not isinstance(value, str):
        return ""
    key = " ".join(value.strip().casefold().split())
    return ALIASES.get(key, key)


def _has_word(text: str, word: str) -> bool:
    return re.search(
        r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])",
        text,
    ) is not None


def _job_text(job: dict) -> tuple[str, set[str]]:
    parts = []
    terms = set()
    for field in ("role", "experience"):
        value = job.get(field)
        if isinstance(value, str):
            parts.append(value.casefold())
    for field in ("skills", "inferred_skills", "keywords", "responsibilities"):
        values = job.get(field, [])
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str):
                    parts.append(value.casefold())
                    if field != "responsibilities":
                        terms.add(norm(value))
    return " ".join(parts), terms


def needed_categories(job: dict, text: str) -> set[str]:
    categories = set()
    given = job.get("needed_categories", [])
    if isinstance(given, list):
        categories.update(
            category for category in given if category in CATEGORY_ORDER
        )
    for category, words in CATEGORY_TRIGGERS.items():
        if any(_has_word(text, word) for word in words):
            categories.add(category)
    return categories


def select_skills(
    pool: dict,
    projects: list,
    job: dict,
    matched: list | None = None,
    confirmed: list | None = None,
) -> dict:
    job = job or {}
    text, terms = _job_text(job)
    categories = needed_categories(job, text)
    default_keys = {norm(skill) for skill in DEFAULT_SKILLS}
    default_keys.update(norm(skill) for skill in DEFAULT_CLOUD)

    # Always offer the default cloud platforms, even if they are missing
    # from (or disabled in) the saved skills data.
    pool = dict(pool)
    cloud = list(pool.get("cloud", []))
    known = {norm(skill) for skill in cloud}
    cloud += [skill for skill in DEFAULT_CLOUD if norm(skill) not in known]
    pool["cloud"] = cloud

    matched_keys = {
        norm(skill) for skill in (matched or []) if isinstance(skill, str)
    }
    confirmed = [
        skill for skill in (confirmed or [])
        if isinstance(skill, str) and skill.strip()
    ]

    usage = Counter()
    for project in projects or []:
        technologies = (
            project.get("technologies", [])
            if isinstance(project, dict) else []
        )
        for technology in technologies:
            usage[norm(technology)] += 1

    result = {}
    for category in CATEGORY_ORDER:
        skills = list(pool.get(category, []))
        existing = {norm(skill) for skill in skills}

        for skill in confirmed:
            if (CONFIRMED_CATEGORY.get(norm(skill), "tools") == category
                    and norm(skill) not in existing):
                skills.append(skill.strip())

        if not skills:
            continue

        def asked(skill):
            key = norm(skill)
            return (
                key in terms
                or key in matched_keys
                or _has_word(text, key)
                or any(norm(item) == key for item in confirmed)
            )

        base = [skill for skill in skills if norm(skill) in default_keys]
        direct = [
            skill for skill in skills
            if asked(skill) and norm(skill) not in default_keys
        ]
        direct.sort(key=lambda skill: (-usage[norm(skill)], skills.index(skill)))
        limit = MAX_SOFT if category == "soft_skills" else MAX_PER_CATEGORY
        picked = (base + direct)[:limit]

        if not picked and category in categories:
            ranked = sorted(
                skills,
                key=lambda skill: (-usage[norm(skill)], skills.index(skill)),
            )
            count = (
                MAX_SOFT if category == "soft_skills"
                else MAX_LANGUAGES_WHEN_VAGUE
                if category == "languages"
                else MAX_OTHER_WHEN_VAGUE
            )
            used = [skill for skill in ranked if usage[norm(skill)] > 0]
            picked = (used + [skill for skill in ranked if skill not in used])[:count]

        if picked:
            result[category] = picked

    if not result:
        languages = sorted(
            pool.get("languages", []),
            key=lambda skill: -usage[norm(skill)],
        )[:MAX_LANGUAGES_WHEN_VAGUE]
        if languages:
            result["languages"] = languages

    def total():
        return sum(len(skills) for skills in result.values())

    for category in TRIM_ORDER:
        while total() > MAX_TOTAL and len(result.get(category, [])) > 1:
            result[category].pop()
    for category in TRIM_ORDER:
        if total() > MAX_TOTAL and category in result:
            del result[category]

    return {
        category: result[category]
        for category in CATEGORY_ORDER
        if category in result
    }

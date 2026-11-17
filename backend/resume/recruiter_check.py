"""HR-style final check of the finished resume. It only warns."""

import re

from backend.ai.keyword_guard import BANNED_WORDS, has_word, job_terms


MAX_SUMMARY_WORDS = 55
MAX_SKILLS = 24
MAX_BULLET_WORDS = 30
MIN_KEYWORD_COVERAGE = 0.6


def _check(name: str, ok: bool, detail: str = "") -> dict:
    return {"name": name, "ok": bool(ok), "detail": detail}


def _resume_text(resume) -> str:
    parts = [str((resume.summary or {}).get("content", ""))]
    labels = {
        "languages": "programming languages", "databases": "databases",
        "cs_fundamentals": "computer science fundamentals", "tools": "tools",
        "cloud": "cloud", "ai_ml": "machine learning ai",
        "soft_skills": "soft skills",
    }
    for category, skills in (resume.skills or {}).items():
        parts.append(labels.get(category, category))   # the heading counts too
        parts.extend(skills)
    for project in resume.projects or []:
        parts.extend(project.get("highlights", []) or [])
        parts.extend(
            project.get("display_technologies")
            or project.get("technologies", [])
            or []
        )

    joined = " ".join(parts).casefold()
    if "linux" in joined:                               # Linux = Unix family
        parts.append("unix")
    if "object-oriented programming" in joined:
        parts.append("object oriented design")
    if "rag" in joined:
        parts.append("retrieval-augmented generation retrieval augmented generation")
    if "vector embeddings" in joined or "vector cosine" in joined:
        parts.append("vector databases vector database")
    return " ".join(parts).casefold()


def recruiter_check(
    resume,
    analysis: dict,
    source_experience: list | None = None,
) -> dict:
    checks = []
    summary = str((resume.summary or {}).get("content", "")).strip()
    words = summary.split()
    sentences = len(re.findall(r"[.!?]+(?=\s|$)", summary))
    buzz = [word for word in BANNED_WORDS if has_word(summary, word)]
    checks.append(_check(
        "Summary is short and simple",
        0 < len(words) <= MAX_SUMMARY_WORDS and sentences <= 3 and not buzz,
        f"{len(words)} words, {sentences} sentences"
        + (f", buzzwords: {', '.join(buzz)}" if buzz else ""),
    ))

    skills = resume.skills or {}
    total = sum(len(values) for values in skills.values())
    checks.append(_check(
        f"Skills are {MAX_SKILLS} or fewer",
        0 < total <= MAX_SKILLS and all(skills.values()),
        f"{total} skills in {len(skills)} lines",
    ))

    bad = []
    for project in resume.projects or []:
        bullets = project.get("highlights", []) or []
        if (
            not 1 <= len(bullets) <= 3
            or any(len(bullet.split()) > MAX_BULLET_WORDS for bullet in bullets)
        ):
            bad.append(project.get("title", "project"))
    checks.append(_check(
        "Project bullets are short (max 3 each)",
        not bad and bool(resume.projects),
        "too long/short: " + ", ".join(bad)
        if bad else f"{len(resume.projects or [])} projects",
    ))

    all_bullets = " ".join(
        bullet
        for project in (resume.projects or [])
        for bullet in (project.get("highlights", []) or [])
    )
    found = [word for word in BANNED_WORDS if has_word(all_bullets, word)]
    checks.append(_check(
        "No buzzwords in project bullets",
        not found,
        ", ".join(found),
    ))

    must_have = job_terms(analysis, ("skills",))
    if must_have:
        text = _resume_text(resume)
        hit = [term for term in must_have if has_word(text, term)]
        missing = [term for term in must_have if term not in hit]
        checks.append(_check(
            "Job keywords appear on the resume",
            len(hit) / len(must_have) >= MIN_KEYWORD_COVERAGE,
            f"{len(hit)}/{len(must_have)} found"
            + (f"; missing: {', '.join(missing[:6])}" if missing else ""),
        ))

    if source_experience is not None:
        checks.append(_check(
            "Experience is exactly as you saved it",
            resume.experience == source_experience,
        ))

    header = resume.header or {}
    lacking = [
        field for field in ("email", "phone", "linkedin", "github")
        if not header.get(field)
    ]
    checks.append(_check(
        "Contact links are present",
        not lacking,
        ", ".join(lacking),
    ))

    passed = sum(1 for check in checks if check["ok"])
    return {"passed": passed, "total": len(checks), "checks": checks}

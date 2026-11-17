
import json
import re
from pathlib import Path

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

PROFILE_FILE = ROOT_DIR / "data" / "personal" / "profile.json"
SKILLS_FILE = ROOT_DIR / "data" / "personal" / "skills.json"

MIN_WORDS = 40
MAX_WORDS = 75
MIN_SENTENCES = 2
MAX_ATTEMPTS = 2
FORBIDDEN_WORDS = {
    "leveraged", "spearheaded", "orchestrated", "utilized", "robust",
    "seamless", "cutting-edge", "innovative", "state-of-the-art", "synergy",
    "passionate", "dynamic", "scalable", "end-to-end", "holistic", "pivotal",
    "streamlined", "harnessed", "empowered", "proficient", "adept",
}


SUMMARY_PROMPT = """
You write the Summary line of a fresher's resume. Imagine an HR who
reads it in 6 seconds, and an ATS robot that looks for keywords.

RULES
- Exactly 2 sentences, 50 to 60 words in total. It must fill 2 to 3 lines.
- Simple, clear English. Short words. No fancy words.
- Never use: leveraged, spearheaded, passionate, motivated, robust,
  seamless, cutting-edge, innovative, dynamic, results-driven.
- Do not start with the candidate's name. Do not use "I", "my" or "he/she".
- Sentence 1: who the candidate is (final-year Computer Science student,
  the target role from the job description) and 3 or 4 main skills.
- Sentence 2: what the candidate has built with those skills
  (use the projects below) and what they want to do in this role.
- Use job-description keywords ONLY when the candidate skills or
  projects below really contain them. Never add a skill that is not below.
- If the job description does not name a programming language, mention
  the candidate's own main language from the skills below.
- Do not invent experience, numbers, achievements or certificates.
- Plain text only. No heading, bullets or quotation marks.

STYLE
- Write like a final-year student talking to an HR: short, plain words.
- Use only facts that appear in the candidate data below. Never invent.
- Forbidden words: leveraged, spearheaded, orchestrated, utilized, robust,
  seamless, cutting-edge, innovative, state-of-the-art, synergy, passionate,
  dynamic, scalable, end-to-end, holistic, pivotal, streamlined, harnessed,
  empowered, proficient, adept.

CANDIDATE PROFILE:
{profile}

CANDIDATE SKILLS:
{skills}

RELEVANT PROJECTS:
{projects}

TARGET JOB DESCRIPTION:
{job_description}
"""


def load_profile():
    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_skills():
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    result = {}
    for category, value in data.items():
        if isinstance(value, list):
            names = [skill for skill in value if isinstance(skill, str)]
        elif isinstance(value, dict) and value.get("enabled", True):
            names = [
                skill["name"] if isinstance(skill, dict) else skill
                for skill in value.get("skills", [])
                if not isinstance(skill, dict) or skill.get("enabled", True)
            ]
        else:
            names = []
        if names:
            result[category] = names
    return result


def is_valid_summary(summary: str) -> bool:
    """Check that the generated summary meets minimum content requirements."""

    if not summary:
        return False

    words = summary.split()

    # Require enough meaningful content for a substantial summary.
    if len(words) < MIN_WORDS or len(words) > MAX_WORDS:
        return False
    if any(
        re.search(r"(?<![A-Za-z0-9])" + re.escape(word) + r"(?![A-Za-z0-9])",
                  summary, re.IGNORECASE)
        for word in FORBIDDEN_WORDS
    ):
        return False

    # Require at least two complete sentences.
    sentences = re.findall(r"[.!?]+(?=\s|$)", summary.strip())

    if len(sentences) < MIN_SENTENCES:
        return False

    # Reject common third-person introductions.
    if re.match(
        r"^(?:the candidate|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+"
        r"(?:is|has been|was)\b",
        summary.strip(),
        re.IGNORECASE,
    ):
        return False

    return True


def fallback_summary(top_projects: list) -> str:
    skills = load_skills()
    languages = ", ".join(skills.get("languages", [])[:2]) or "Python"
    titles = [
        project.get("title", "").split(" – ")[0].split(" - ")[0].strip()
        for project in (top_projects or [])
        if isinstance(project, dict) and project.get("title")
    ][:2]
    built = " and ".join(titles) if titles else "AI and backend projects"
    return (
        f"Final-year Computer Science student with hands-on skills in "
        f"{languages}, databases, REST APIs and cloud deployment. Built "
        f"{built} using these skills, and wants to help teams solve "
        "technical problems and grow as a software professional."
    )


def generate_summary(
    job_description: str,
    top_projects: list,
):
    profile = load_profile()
    skills = load_skills()

    prompt = SUMMARY_PROMPT.format(
        profile=json.dumps(profile, indent=2, ensure_ascii=False),
        skills=json.dumps(skills, indent=2, ensure_ascii=False),
        projects=json.dumps(top_projects, indent=2, ensure_ascii=False),
        job_description=(job_description or "").strip()
        or "No specific job description provided.",
    )

    for attempt in range(MAX_ATTEMPTS):
        summary = analyze(prompt, max_output_tokens=1000).strip()

        # Remove accidental surrounding quotation marks.
        summary = summary.strip("\"'").strip()

        if is_valid_summary(summary):
            return summary
        print(
            f"[summary rejected] attempt {attempt + 1}: "
            f"{len(summary.split())} words -> {summary!r}"
        )

        if attempt < MAX_ATTEMPTS - 1:
            prompt += """

IMPORTANT: Your previous response did not meet the required
length or sentence count. Rewrite it as exactly 2 complete
sentences containing 40–75 words. Include at least 40 words,
use evidence from the supplied candidate information,
and do not begin with the candidate's name. Return only the
corrected summary paragraph.
"""

    return fallback_summary(top_projects)

import json
from pathlib import Path

from backend.ai.analyzer import analyze



ROOT_DIR = Path(__file__).resolve().parents[2]

PROFILE_FILE = ROOT_DIR / "data" / "personal" / "profile.json"
SKILLS_FILE = ROOT_DIR / "data" / "personal" / "skills.json"


SUMMARY_PROMPT = """
You are an expert ATS Resume Writer and Technical Recruiter.

You will receive:

1. Candidate Profile
2. Resume Skills
3. Top Ranked Projects
4. Job Description

IMPORTANT RULES:

- Never invent technologies or project experience.
- Mention only skills or technologies supported by the candidate profile, skills, or projects.
- If a technology exists only in the skills section, do not claim it was used in a project.
- Keep the tone professional and ATS-friendly.

Write a professional resume summary.

Rules:

- 2 to 3 sentences only.
- Maximum 80 words.
- Tailor it specifically for the job description.
- Highlight the candidate's strongest and most relevant skills.
- Mention the most relevant projects naturally.
- Use ATS-friendly keywords.
- Do NOT invent experience.
- Do NOT mention years of experience unless provided.
- Do NOT use first person ("I", "My").
- Return ONLY the summary text.
- Do NOT return JSON.

Candidate Profile:

{profile}

Resume Skills:

{skills}

Top Projects:

{projects}

Job Description:

{job_description}
"""


def load_profile():

    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_skills():

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_summary(
    job_description: str,
    top_projects: list,
):

    profile = load_profile()

    skills = load_skills()

    
    prompt = SUMMARY_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        skills=json.dumps(skills, indent=2),
        projects=json.dumps(top_projects, indent=2),
        job_description=job_description,
    )

    summary = analyze(prompt)

    return summary.strip()
import json
from pathlib import Path

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

SKILLS_FILE = ROOT_DIR / "data" / "personal" / "skills.json"
PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"


SKILL_MATCH_PROMPT = """
You are an expert ATS Resume Reviewer and Technical Recruiter.

You will receive:

1. Candidate Resume Skills
2. Candidate Resume Projects
3. Job Requirements

Your task is to identify:

1. Which job requirements are genuinely supported by the candidate.
2. Which job requirements are missing.
3. Which EXISTING candidate skills should be emphasized in the
   final resume.

==================================================
PROGRAMMING LANGUAGES — STRICT RULE
==================================================

Programming languages must be handled strictly.

A programming language can ONLY be considered a candidate skill
if it is explicitly present in the Candidate Resume Skills.

Example:

Candidate languages:

Python
SQL
HTML
CSS

Job requires:

Java
C++
C
Python

Correct:

matching_skills:
Python

missing_skills:
Java
C++
C

Do NOT add:

Java
C++
C

Do not infer programming languages from frameworks.

React does NOT mean JavaScript.

Node.js does NOT mean JavaScript.

FastAPI does NOT mean Python should be inferred if Python is not
explicitly present in the candidate's languages.

==================================================
CANDIDATE SKILLS
==================================================

Candidate skills explicitly listed in Resume Skills are valid
candidate skills.

Examples:

Python
SQL
FastAPI
React
Node.js
Express
MongoDB
Git
Microsoft Azure
Problem Solving

==================================================
PROJECT TECHNOLOGIES
==================================================

Technologies explicitly listed inside Candidate Resume Projects
may also be considered candidate-supported skills.

Examples from the supplied projects include:

PostgreSQL
Scikit-learn
SHAP
Machine Learning
Vision AI
Razorpay
FFmpeg
Whisper
Ollama
Gemini API
TensorFlow
OpenCV
Faster-Whisper
Piper TTS
Stellar Blockchain

Only use a project technology if it is explicitly present in the
supplied project data.

Never invent project technologies.

The Job Requirements JSON may contain:

- "skills": explicitly stated technical requirements.
- "inferred_skills": likely relevant skills inferred from the job title, responsibilities, and technical context.
- "keywords": relevant ATS terms.
- "responsibilities": the main duties of the role.

Follow this decision process:

1. If explicit technical skills are present and sufficient, prioritize those skills when matching the candidate.
2. If explicit skills are missing or incomplete, use "inferred_skills" and relevant keywords to identify additional skills that fit the role.
3. If both explicit and inferred skills exist, consider both, but prioritize explicit requirements and the strongest role-relevant inferred requirements.
4. Match these requirements against the candidate's supplied skills and project technologies. Programming languages must still follow the strict programming-language rules below.
5. Inferred job requirements are NOT proof that the candidate has those skills. Only mark a skill as matching when the candidate's supplied data supports it.
6. Do not list every candidate skill. Return only the strongest, relevant, evidence-supported skills in "additional_resume_skills", with a maximum of 10.
7. Do not claim that an inferred skill was explicitly required by the employer. Missing or unsupported skills must not be added to the resume.

==================================================
MATCHING SKILLS
==================================================

"matching_skills" contains job requirements that are genuinely
supported by the candidate.

Example:

Job:
Python
SQL
Java
Algorithms

Candidate:
Python
SQL

Return:

matching_skills:
Python
SQL

missing_skills:
Java
Algorithms

Do not put unsupported requirements into matching_skills.

==================================================
MISSING SKILLS
==================================================

"missing_skills" contains job requirements that are not genuinely
supported by the candidate's supplied data.

Missing skills are ONLY for analysis.

They must NEVER be added to the candidate's resume.

==================================================
ADDITIONAL RESUME SKILLS
==================================================

"additional_resume_skills" contains EXISTING candidate skills
that are relevant to the job and should be emphasized in the
Technical Skills section.

These may come from:

1. Candidate Resume Skills
2. Explicit project technologies

Do NOT return every candidate skill.

Only return skills that are relevant to the current job.

Maximum 10 skills.

Examples:

If the job emphasizes backend development and the candidate has:

Python
FastAPI
React
PostgreSQL
Tailwind CSS
Git

then relevant additional resume skills could be:

FastAPI
PostgreSQL
Git

Do not include Tailwind CSS just because it exists.

==================================================
CS FUNDAMENTALS
==================================================

Do NOT infer CS fundamentals from technologies alone.

Python does NOT automatically prove:

Algorithms
Data Structures
Operating Systems
Complexity Analysis

FastAPI does NOT automatically prove:

Distributed Systems
System Design
Microservices

MongoDB does NOT automatically prove:

Relational Databases

Only mark these as matching if the candidate's supplied skills
or project information explicitly supports them.

==================================================
SOFT SKILLS
==================================================

Only use soft skills explicitly present in candidate data.

For example:

Candidate:
Problem Solving
Analytical Thinking
Quick Learner

If the job asks for problem solving, it can match.

Do NOT add:

Communication
Leadership
Teamwork

unless supported by candidate data.

==================================================
MATCHING SCORE
==================================================

Calculate match_percentage based on genuinely supported job
requirements.

Do not artificially increase the score.

==================================================
MATCHING CS FUNDAMENTALS
==================================================

Return "matching_cs_fundamentals" as a list of CS fundamentals
that are both relevant to the job and explicitly supported by
the candidate's supplied skills or project data.

Candidate-listed examples include:
- Data Structures
- Algorithms
- DBMS
- Operating Systems
- OOP
- Computer Networks
- Computer Architecture

Do not infer a fundamental from a programming language,
framework, or database technology alone.

Never include a required fundamental that the candidate
does not have evidence for.

Missing fundamentals belong in "missing_skills", not in
"matching_cs_fundamentals".

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Return exactly:

{{
    "matching_skills": [],
    "matching_cs_fundamentals": [],
    "missing_skills": [],
    "additional_resume_skills": [],
    "match_percentage": 0,
    "recommendations": []
}}

Important:

Do NOT return ordered_skills.

Do NOT return all candidate skills.

Do NOT add missing skills to additional_resume_skills.

Do NOT invent skills.

==================================================
CANDIDATE RESUME SKILLS
==================================================

{resume_skills}

==================================================
CANDIDATE RESUME PROJECTS
==================================================

{resume_projects}

==================================================
JOB REQUIREMENTS
==================================================

{job_skills}
"""


def load_resume_skills() -> dict:
    """Load only enabled skill categories and individual skills."""
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        raw_skills = json.load(file)

    if not isinstance(raw_skills, dict):
        raise ValueError("skills.json must contain a JSON object.")

    enabled_skills = {}

    for category, category_data in raw_skills.items():
        # Backward compatibility with the old format.
        if isinstance(category_data, list):
            enabled_skills[category] = [
                skill.strip()
                for skill in category_data
                if isinstance(skill, str) and skill.strip()
            ]
            continue

        if not isinstance(category_data, dict):
            continue

        # Skip the entire category when disabled.
        if category_data.get("enabled", True) is not True:
            continue

        skills = category_data.get("skills", [])

        if not isinstance(skills, list):
            continue

        category_skills = []

        for skill in skills:
            if not isinstance(skill, dict):
                continue

            # Skip an individually disabled skill.
            if skill.get("enabled", True) is not True:
                continue

            name = skill.get("name")

            if isinstance(name, str) and name.strip():
                category_skills.append(name.strip())

        enabled_skills[category] = category_skills

    return enabled_skills


def load_resume_projects() -> list:

    with open(
        PROJECTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def match_skills(job_requirements: dict) -> dict:

    resume_skills = load_resume_skills()
    resume_projects = load_resume_projects()

    prompt = SKILL_MATCH_PROMPT.format(
        resume_skills=json.dumps(
            resume_skills,
            indent=2
        ),
        resume_projects=json.dumps(
            resume_projects,
            indent=2
        ),
        job_skills=json.dumps(
            job_requirements,
            indent=2
        )
    )

    response = analyze(prompt, json_mode=True, max_output_tokens=1500)

    response = response.replace(
        "```json",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "Gemini did not return valid JSON."
        )

    try:

        result = json.loads(
            response[start:end + 1]
        )

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid skill match JSON: {str(e)}"
        )

    result.setdefault(
        "matching_skills",
        []
    )

    result.setdefault(
        "matching_cs_fundamentals",
        []
    )

    result.setdefault(
        "missing_skills",
        []
    )

    result.setdefault(
        "additional_resume_skills",
        []
    )

    result.setdefault(
        "match_percentage",
        0
    )

    result.setdefault(
        "recommendations",
        []
    )

    return result

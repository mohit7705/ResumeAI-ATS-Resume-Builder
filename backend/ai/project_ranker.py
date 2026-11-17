import json
from pathlib import Path
from typing import Any

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"


PROJECT_RANK_PROMPT = """
You are an expert Technical Recruiter and ATS Resume Reviewer.

Your task is to evaluate ONE resume project against a Job Description.

IMPORTANT:

The Project JSON is the ONLY source of truth about the candidate's
actual project experience.

You MUST NOT assume technologies, skills, architecture, responsibilities,
or implementation details that are not explicitly present in the project.

For example:

If the project contains Python:
    Python experience may be matched.

If the project contains FastAPI:
    FastAPI / backend / API experience may be matched.

If the project contains MongoDB:
    MongoDB / NoSQL database experience may be matched.

If the project does NOT explicitly mention:
    Java
    C++
    Operating Systems
    Data Structures
    Algorithms
    Distributed Systems
    System Design
    SQL
    Docker

then you MUST NOT claim that the project demonstrates those skills.

----------------------------------------
SCORING
----------------------------------------

Score the project from 0 to 100.

Consider:

1. Explicit technology overlap       40%
2. Explicit skill overlap             25%
3. Explicit keyword/concept overlap   15%
4. Demonstrated project impact        10%
5. Project complexity                 10%

Only award points when there is evidence
in the Project JSON.

Do NOT increase the score simply because
a concept appears in the Job Description.

----------------------------------------
SEMANTIC MATCHING
----------------------------------------

Semantic matching is allowed only when the
project evidence genuinely supports the concept.

For example:

FastAPI can support:
- API development
- backend development

Gemini / Ollama can support:
- LLM
- Generative AI

Whisper can support:
- speech-to-text

FFmpeg can support:
- video processing

TensorFlow can support:
- machine learning

But:

FastAPI does NOT automatically mean:
- distributed systems
- microservices
- system design

Python does NOT automatically mean:
- algorithms
- data structures
- operating systems

MongoDB does NOT automatically mean:
- relational databases
- SQL

----------------------------------------
IMPORTANT FOR ATS
----------------------------------------

The goal is NOT to maximize the score.

The goal is to accurately identify how relevant
the project actually is to the job.

A project with a lower score is acceptable if
the project genuinely has fewer matching skills.

Never fabricate experience to improve ATS matching.

----------------------------------------
OUTPUT
----------------------------------------

Return ONLY valid JSON.

Return exactly:

{{
    "score": 0,
    "reason": "",
    "matched_skills": [],
    "matched_keywords": []
}}

The "reason" must be concise and evidence-based.

"matched_skills" must contain only skills that are
actually supported by the Project JSON.

"matched_keywords" must contain only concepts that
are actually supported by the Project JSON.

----------------------------------------
JOB DESCRIPTION
----------------------------------------

{job_description}

----------------------------------------
PROJECT
----------------------------------------

{project}

Remember:

The Project JSON is the ONLY source of truth.

Do not invent experience.
Do not assume missing technologies.
Do not keyword-stuff the project.
"""


def load_projects() -> list[dict[str, Any]]:
    """
    Load all resume projects.
    """

    with open(PROJECTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def score_project(
    job_description: str,
    project: dict[str, Any]
) -> dict[str, Any]:

    prompt = PROJECT_RANK_PROMPT.format(
        job_description=job_description,
        project=json.dumps(project, indent=2)
    )

    response = analyze(prompt, json_mode=True, max_output_tokens=1200)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"Gemini did not return JSON.\n\n{response}"
        )

    json_text = response[start:end + 1]

    try:
        result = json.loads(json_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid project ranking JSON: {str(e)}"
        )

    # Validate score
    score = result.get("score", 0)

    if not isinstance(score, int):
        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

    result["score"] = max(0, min(100, score))

    # Validate arrays
    if not isinstance(result.get("matched_skills"), list):
        result["matched_skills"] = []

    if not isinstance(result.get("matched_keywords"), list):
        result["matched_keywords"] = []

    if not isinstance(result.get("reason"), str):
        result["reason"] = ""

    return result


def rank_projects(
    job_description: str
) -> dict[str, list[dict[str, Any]]]:

    projects = load_projects()

    ranked: list[dict[str, Any]] = []

    for project in projects:

        result = score_project(
            job_description,
            project
        )

        ranked.append({
            "title": project["title"],
            "score": result["score"],
            "reason": result["reason"],
            "matched_skills": result["matched_skills"],
            "matched_keywords": result["matched_keywords"]
        })

    ranked.sort(
        key=lambda x: (
            x["score"],
            len(x["matched_skills"]),
            len(x["matched_keywords"])
        ),
        reverse=True
    )

    top_projects = ranked[:4]

    return {
        "ranked_projects": ranked,
        "top_projects": top_projects
    }
import json
from pathlib import Path
from typing import Any

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"


PROJECT_RANK_PROMPT = """
You are an expert Technical Recruiter.

You will receive:

1. A Job Description
2. One Resume Project

Your task is to score ONLY this project.

Score must be an integer between 0 and 100.

Guidelines:

95-100 = Exceptional match
85-94 = Strong match
70-84 = Good match
50-69 = Partial match
30-49 = Weak match
0-29 = Poor match

Consider:

- Technology match (40%)
- Required skills match (25%)
- Keywords match (15%)
- Business impact (10%)
- Project complexity (10%)

Return ONLY valid JSON.

Do NOT explain outside JSON.
Return score as an integer between 0 and 100.

{{
    "score": 0,
    "reason": "",
    "matched_skills": [],
    "matched_keywords": []
}}

Job Description:

{job_description}

Project:

{project}
"""


def load_projects() -> list[dict[str, Any]]:
    """
    Load all resume projects.
    """

    with open(PROJECTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def score_project(job_description: str, project: dict[str, Any]) -> dict[str, Any]:

    prompt = PROJECT_RANK_PROMPT.format(
        job_description=job_description,
        project=json.dumps(project, indent=2)
    )

    response = analyze(prompt)

    print("\n========== PROJECT RANK RESPONSE ==========")
    print(response)
    print("===========================================\n")

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

    return json.loads(json_text)


def rank_projects(job_description: str) -> dict[str, list[dict[str, Any]]]:

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

    top_projects = ranked[:3]

    return {
        "ranked_projects": ranked,
        "top_projects": top_projects
    }
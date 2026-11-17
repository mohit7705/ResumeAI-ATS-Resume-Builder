import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from backend.ai.analyzer import analyze, with_context
from backend.ai.keyword_guard import (
    MAX_BULLETS,
    display_technologies,
    fallback_bullets,
    proper_case,
    usable_keywords,
    validate_bullets,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"

PROJECT_REWRITE_PROMPT = """
You are a Senior Technical Recruiter and Staff Software Engineer at Google.
Rewrite project bullets so they pass both an ATS keyword filter and a 6-second
engineering hiring manager scan.

TASK
Write exactly 3 concise, high-impact engineering bullets for the project below,
tailored to the target job description.

BULLET STRUCTURE (Action + Architecture + Impact)
- 16 to 28 words per bullet.
- Start with a strong systems-engineering verb: Engineered, Architected, Built,
  Automated, Integrated, Optimized, Designed, Deployed, or Implemented.
- Specify the technical mechanism (APIs, pipelines, data stores, models) and
  the concrete outcome or capability.
- Never use empty fluff: leveraged, spearheaded, orchestrated, utilized,
  synergy, seamless, cutting-edge, innovative, state-of-the-art, or passionate.

STRICT GROUNDING RULES
- Use ONLY facts, tools, architecture details, and metrics present in PROJECT DATA.
- NEVER invent numbers, latency figures, user counts, or technologies not in PROJECT DATA.
- If metrics exist in PROJECT DATA, include them accurately.

KEYWORD ALIGNMENT
- Naturally weave 1 to 2 of these verified job keywords into each bullet:
  {keywords}
- Use exact capitalization (e.g., FastAPI, PostgreSQL, Vertex AI, RAG, LangGraph).

{critique_block}

OUTPUT
Return valid JSON only: {{"highlights": ["bullet 1", "bullet 2", "bullet 3"]}}

JOB DESCRIPTION
{job_description}

PROJECT DATA (only source of truth)
{project}
"""


def load_projects():
    with open(PROJECTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _parse_highlights(response: str) -> list:
    response = response.replace("```json", "").replace("```", "").strip()
    start = response.find("{")
    end = response.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM did not return valid JSON.")

    result = json.loads(response[start:end + 1])
    highlights = result.get("highlights")
    if not isinstance(highlights, list):
        raise ValueError("LLM returned invalid highlights list.")
    return [str(value).strip() for value in highlights if str(value).strip()]


def rewrite_project(
    job_description: str,
    project: dict,
    analysis: dict | None = None,
    retrieved_evidence: list[str] | None = None,
    max_reflection_turns: int = 2,
):
    analysis = analysis or {}
    project_data = {
        "title": proper_case(project.get("title", "")),
        "technologies": project.get("technologies", []),
        "highlights": project.get("highlights", []),
        "architecture": project.get("architecture", ""),
        "metrics": project.get("metrics", []),
        "matched_evidence_chunks": retrieved_evidence or [],
    }

    keywords_str = ", ".join(usable_keywords(project, analysis)) or "(none)"
    project_json = json.dumps(project_data, indent=1, ensure_ascii=False)

    bullets = []
    critiques = []

    for attempt in range(max_reflection_turns):
        critique_block = ""
        if critiques:
            critique_block = (
                "PREVIOUS DRAFT REJECTED — FIX THESE ISSUES:\n- "
                + "\n- ".join(critiques)
            )

        prompt = PROJECT_REWRITE_PROMPT.format(
            keywords=keywords_str,
            critique_block=critique_block,
            job_description=job_description,
            project=project_json,
        )

        try:
            raw_bullets = _parse_highlights(
                analyze(prompt, json_mode=True, max_output_tokens=700)
            )
            bullets, critiques = validate_bullets(raw_bullets, project, analysis)
            if len(bullets) == MAX_BULLETS:
                break
        except (RuntimeError, ValueError, json.JSONDecodeError) as err:
            critiques = [f"JSON parse/API error: {err}"]

    if len(bullets) < MAX_BULLETS:
        for extra in fallback_bullets(project):
            if extra not in bullets:
                bullets.append(extra)
            if len(bullets) == MAX_BULLETS:
                break

    return {
        "title": proper_case(project.get("title", "")),
        "highlights": bullets,
        "display_technologies": display_technologies(project, analysis),
        "reflection_attempts": attempt + 1,
    }


def rewrite_projects(
    job_description: str,
    top_projects: list,
    analysis: dict | None = None,
    evidence_map: dict[str, list[str]] | None = None,
):
    all_projects = load_projects()
    evidence_map = evidence_map or {}
    selected = [
        next(project for project in all_projects if project["title"] == ranked["title"])
        for ranked in top_projects
    ]

    with ThreadPoolExecutor(max_workers=max(1, len(selected))) as pool:
        futures = [
            pool.submit(
                with_context(rewrite_project),
                job_description,
                project,
                analysis,
                evidence_map.get(project["title"], []),
            )
            for project in selected
        ]
        results = [future.result() for future in futures]

    return [
        {**project, **result}
        for project, result in zip(selected, results)
    ]
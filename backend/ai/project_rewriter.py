import json
from pathlib import Path

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"


PROJECT_REWRITE_PROMPT = """
You are an expert Technical Recruiter who has reviewed more than 50,000 software engineering resumes at Google, Microsoft, Amazon, Meta and Salesforce.

Your task is to rewrite ONE resume project for maximum ATS compatibility while remaining 100% truthful.

You will receive:

1. Job Description
2. One Resume Project

The project contains:

- title
- technologies
- highlights
- keywords

These are the ONLY source of truth.

----------------------------------------
RULES
----------------------------------------

Never invent:

- technologies
- frameworks
- databases
- cloud providers
- APIs
- deployment methods
- architecture
- programming languages
- measurable numbers
- business impact that is not supported

Never claim:

Designed REST APIs
Docker
AWS
Kubernetes
Microservices
GraphQL
CI/CD

unless they already exist inside the project.

----------------------------------------
WHAT YOU MAY DO
----------------------------------------

Rewrite the wording.

Use stronger action verbs.

Improve ATS keywords.

Improve readability.

Merge duplicate ideas.

Highlight technical complexity.

Highlight engineering decisions.

Highlight automation.

Highlight AI usage.

Highlight backend/frontend responsibilities.

Highlight scalability only if supported.

Highlight machine learning only if supported.

Highlight business value already present.

----------------------------------------
WRITING STYLE
----------------------------------------

Every bullet should:

Start with a strong verb.

Examples:

Engineered

Architected

Developed

Designed

Built

Implemented

Integrated

Optimized

Automated

Leveraged

Each bullet:

15–30 words.

Professional.

ATS friendly.

No buzzwords.

No unnecessary adjectives.

No repeated information.

Maximum 3 bullets.

Choose ONLY the three strongest and most relevant achievements for the target job.

Do not repeat information.

Prioritize:
1. Technical complexity
2. Business impact
3. Technologies matching the job description

----------------------------------------
JOB MATCHING
----------------------------------------

If the job asks for a missing skill:

DO NOT invent it.

Instead emphasize the closest related experience.

Example:

Job asks Docker.

Project has Azure deployment.

Mention deployment experience.

Do NOT mention Docker.

----------------------------------------
OUTPUT
----------------------------------------

Return ONLY valid JSON.

{{
    "highlights":[]
}}

Job Description

{job_description}

Project

{project}
"""
def load_projects():

    with open(PROJECTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def rewrite_project(job_description: str, project: dict):

    prompt = PROJECT_REWRITE_PROMPT.format(
        job_description=job_description,
        project=json.dumps(project, indent=2)
    )

    response = analyze(prompt)

    print("\n========== PROJECT REWRITE ==========")
    print(response)
    print("====================================\n")

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Gemini did not return valid JSON.")

    return json.loads(response[start:end + 1])


def rewrite_projects(
    job_description: str,
    top_projects: list,
 ):

    

    rewritten = []

    all_projects = load_projects()

    for ranked_project in top_projects:

        project = next(
            p for p in all_projects
            if p["title"] == ranked_project["title"]
        )

        result = rewrite_project(
            job_description,
            project
        )

        rewritten.append({
            **project,
            "highlights": result["highlights"]
        })

    return rewritten
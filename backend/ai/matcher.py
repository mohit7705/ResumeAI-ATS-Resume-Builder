import json
from pathlib import Path

from backend.ai.analyzer import analyze


ROOT_DIR = Path(__file__).resolve().parents[2]

SKILLS_FILE = ROOT_DIR / "data" / "personal" / "skills.json"
PROJECTS_FILE = ROOT_DIR / "data" / "projects" / "projects.json"


SKILL_MATCH_PROMPT = """
You are an expert ATS Resume Reviewer, Technical Recruiter, and Hiring Manager.

You will receive:

1. Resume Skills
2. Resume Projects
3. Job Skills

Your task is to compare them intelligently using semantic understanding.

Never rely only on exact keyword matching.

Infer skills from projects, technologies, architecture, and accomplishments.

Examples:

• FastAPI → REST API Development
• Gemini API / Ollama / OpenAI → LLM Experience
• Whisper → Speech AI
• OpenCV → Computer Vision
• FFmpeg → Video Processing
• TensorFlow → Machine Learning
• React + Node.js → JavaScript
• React + TypeScript → TypeScript
• MongoDB → NoSQL Database
• Azure / Vercel / Render → Cloud Deployment
• GitHub → Git Version Control

Return ONLY valid JSON.

{{
    "matching_skills": [],
    "missing_skills": [],
    "additional_resume_skills": [],
    "match_percentage": 0,
    "recommendations": []
}}

Recommendation Rules

1. NEVER recommend adding a skill if the resume or projects already demonstrate it.

2. If experience already exists but is hidden, recommend emphasizing it.

Example:

BAD
Add JavaScript.

GOOD
Highlight your JavaScript experience demonstrated through your React and Node.js projects.

BAD
Add TypeScript.

GOOD
Emphasize your TypeScript experience from the ResumeAI project.

BAD
Add REST API.

GOOD
Highlight your FastAPI backend development as REST API experience.

3. Only recommend learning skills that are genuinely missing.

Example:

Docker
AWS
Kubernetes
CI/CD

4. If the candidate has closely related experience, explain how it transfers.

Example:

Azure → AWS

Good recommendation:

You already have experience deploying applications on Azure, Vercel, and Render. Highlight your cloud architecture knowledge while mentioning your ability to adapt quickly to AWS environments.

5. Recommendations should be actionable.

Do NOT say:

Improve JavaScript.

Instead say:

Highlight your JavaScript development experience from React and Node.js projects.

6. Never invent experience.

7. Maximum 5 recommendations.

Resume Skills

{resume_skills}

Resume Projects

{resume_projects}

Job Skills

{job_skills}
"""

def load_resume_skills() -> dict:

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_resume_projects() -> list:

    with open(PROJECTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def match_skills(job_skills: list[str]) -> dict:

    resume_skills = load_resume_skills()
    resume_projects = load_resume_projects()

    prompt = SKILL_MATCH_PROMPT.format(
        resume_skills=json.dumps(resume_skills, indent=2),
        resume_projects=json.dumps(resume_projects, indent=2),
        job_skills=json.dumps(job_skills, indent=2)
    )

    response = analyze(prompt)

    print("\n========== SKILL MATCH RESPONSE ==========")
    print(response)
    print("==========================================\n")

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Gemini did not return valid JSON.")

    return json.loads(response[start:end + 1])
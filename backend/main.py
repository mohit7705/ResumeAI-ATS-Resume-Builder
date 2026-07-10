from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.ai.routes import router as ai_router
from backend.api.achievements import router as achievements_router
from backend.api.certifications import router as certifications_router
from backend.api.contact import router as contact_router
from backend.api.education import router as education_router
from backend.api.experience import router as experience_router
from backend.api.personal import router as personal_router
from backend.api.summary import router as summary_router
from backend.api.projects import router as projects_router
from backend.api.schemas import JobDescriptionRequest
from backend.api.skills import router as skills_router
from backend.resume.engine import generate_resume
from backend.generator.html_generator import generate_html
from backend.generator.pdf_generator import generate_pdf

app = FastAPI(
    title="ResumeAI",
    version="1.0.0"
)

app.mount(
    "/generated",
    StaticFiles(directory="generated"),
    name="generated",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(achievements_router)
app.include_router(certifications_router)
app.include_router(contact_router)
app.include_router(education_router)
app.include_router(experience_router)
app.include_router(personal_router)
app.include_router(summary_router)
app.include_router(projects_router)
app.include_router(skills_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "ResumeAI Backend"
    }


@app.post("/generate")
def generate(request: JobDescriptionRequest):

    result = generate_resume(request.job_description)

    resume = result["resume"]

    html_file = generate_html(resume)

    pdf_file = generate_pdf(html_file)

    return {
    "resume": resume,
    "validation": result["validation"],

    "ats_score": result["ats_score"]["ats_score"],
    "skill_score": result["ats_score"]["skill_score"],
    "project_score": result["ats_score"]["project_score"],

    "skill_match": result["skill_match"],

    "top_projects": result["project_ranking"]["top_projects"],

    "html": str(html_file),
    "pdf": str(pdf_file),
}
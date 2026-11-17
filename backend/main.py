import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.ai.routes import router as ai_router
from backend.ai.analyzer import active_provider, provider_status, use_provider
from backend.api.achievements import router as achievements_router
from backend.api.certifications import router as certifications_router
from backend.api.contact import router as contact_router
from backend.api.education import router as education_router
from backend.api.experience import router as experience_router
from backend.api.personal import router as personal_router
from backend.api.summary import router as summary_router
from backend.api.projects import router as projects_router
from backend.api.schemas import ConfirmedResumeRequest, TitleResumeRequest
from backend.api.skills import router as skills_router
from backend.ai.title_profile import (
    build_job_description_from_title,
    clean_title,
)
from backend.resume.engine import generate_resume
from backend.resume.highlighter import collect_keywords
from backend.generator.html_generator import generate_html
from backend.generator.pdf_generator import generate_pdfs
from backend.utils.timing import timed


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(message)s",
)

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


def run_resume_pipeline(
    job_description: str,
    confirmed_skills: list[str],
    highlight: bool,
    target_title: str | None = None,
    extra: dict | None = None,
    include_photo: bool = True,
):
    """Generate the resume files and build the API response.

    Shared by /generate (pasted job description) and /generate/title
    (job title only), so both return the same response shape.
    """
    started_at = time.perf_counter()
    try:
        # Run resume generation and AI analysis only once.
        result = generate_resume(
            job_description,
            confirmed_skills=confirmed_skills,
            target_title=target_title,
        )
        resume = result["resume"]

        # Job keywords to bold. Empty when the user unticked the box,
        # in which case the HTML is generated exactly as before.
        keywords = (
            collect_keywords(result["analysis"]) if highlight else []
        )
        highlighted_keywords: list[str] = []

        with timed("html"):
            html_file = generate_html(
                resume,
                template_name="ats_one_page.html",
                highlight_keywords=keywords,
                highlight_report=highlighted_keywords,
            )
            photo_html_file = (
                generate_html(
                    resume,
                    template_name="ats_one_page_photo.html",
                    highlight_keywords=keywords,
                )
                if include_photo
                else None
            )

        pdf_jobs = [(html_file, "resume.pdf")]
        if photo_html_file:
            pdf_jobs.append((photo_html_file, "resume_photo.pdf"))
        with timed("pdf"):
            pdf_files = generate_pdfs(pdf_jobs)

        pdf_file = pdf_files[0]
        photo_pdf_file = pdf_files[1] if photo_html_file else None

        response = {
            "resume": resume,
            "validation": result["validation"],
            "recruiter_check": result["recruiter_check"],
            "ats_score": result["ats_score"]["ats_score"],
            "skill_score": result["ats_score"]["skill_score"],
            "project_score": result["ats_score"]["project_score"],
            "skill_match": result["skill_match"],
            "skill_gap_recommendations": result[
                "skill_gap_recommendations"
            ],
            "top_projects": result["project_ranking"]["top_projects"],
            # Keywords that were actually bolded (empty when highlighting
            # is off or nothing matched).
            "highlighted_keywords": highlighted_keywords,
            # Existing response fields — preserved.
            "html": str(html_file),
            "pdf": str(pdf_file),
            "pages": 1,
            # New response fields for the photo version.
            "photo_html": str(photo_html_file) if photo_html_file else None,
            "photo_pdf": str(photo_pdf_file) if photo_pdf_file else None,
            "provider": active_provider(),
            "model": provider_status()[active_provider()]["model"],
            "seconds": round(time.perf_counter() - started_at, 1),
        }

        if extra:
            response.update(extra)

        return response
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e
    except Exception as e:
        import logging

        logging.getLogger(__name__).exception(
            "Resume generation failed"
        )
        raise HTTPException(
            status_code=500,
            detail="Unable to generate resume. Check backend logs.",
        ) from e


@app.post("/generate")
def generate(request: ConfirmedResumeRequest):
    try:
        with use_provider(request.provider):
            return run_resume_pipeline(
                request.job_description,
                confirmed_skills=request.confirmed_skills,
                highlight=request.highlight,
                include_photo=request.include_photo,
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/generate/title")
def generate_from_title(request: TitleResumeRequest):
    try:
        with use_provider(request.provider):
            title = clean_title(request.title)
            job_description = build_job_description_from_title(
                title,
                request.level,
            )

            return run_resume_pipeline(
                job_description,
                confirmed_skills=[],
                highlight=request.highlight,
                target_title=title,
                extra={
                    "target_title": title,
                    "generated_job_description": job_description,
                },
                include_photo=request.include_photo,
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e
    except Exception as e:
        import logging

        logging.getLogger(__name__).exception(
            "Job title profile generation failed"
        )
        raise HTTPException(
            status_code=500,
            detail="Unable to build a job profile for this title.",
        ) from e

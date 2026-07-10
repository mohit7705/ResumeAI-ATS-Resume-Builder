import traceback

from fastapi import APIRouter, HTTPException

from backend.ai.analyzer import analyze_job_description
from backend.ai.matcher import match_skills
from backend.ai.schemas import (
    JobDescriptionRequest,
    JobDescriptionResponse,
    SkillMatchRequest,
    SkillMatchResponse,
)
from backend.ai.schemas import (
    ProjectRankingRequest,
    ProjectRankingResponse,
    SummaryRequest,
    SummaryResponse,
    ProjectRewriteRequest,
    ProjectRewriteResponse,
    ATSScoreRequest,
    ATSScoreResponse,
    OptimizedResumeRequest,
    OptimizedResumeResponse,
)
from backend.ai.project_ranker import rank_projects
from backend.ai.summary_generator import generate_summary
from backend.ai.project_rewriter import rewrite_projects
from backend.ai.ats_score import calculate_ats_score
from backend.ai.matcher import match_skills
from backend.ai.project_ranker import rank_projects
from backend.ai.resume_optimizer import optimize_resume

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/job-description/analyze",
    response_model=JobDescriptionResponse
)
def analyze_job(request: JobDescriptionRequest):
    try:
        result = analyze_job_description(
            request.job_description
        )

        return JobDescriptionResponse(**result)

    except Exception as e:
        print("\n========== AI ERROR ==========")
        traceback.print_exc()
        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/skill-match",
    response_model=SkillMatchResponse
)
def skill_match(request: SkillMatchRequest):
    try:
        result = match_skills(request.job_skills)

        return SkillMatchResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/project-rank",
    response_model=ProjectRankingResponse
)
def project_rank(request: ProjectRankingRequest):
    try:
        result = rank_projects(request.job_description)

        return ProjectRankingResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/generate-summary",
    response_model=SummaryResponse
)
def generate_ai_summary(request: SummaryRequest):
    try:
        summary = generate_summary(
            request.job_description
        )

        return SummaryResponse(
            summary=summary
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/rewrite-projects",
    response_model=ProjectRewriteResponse
)
def rewrite_ai_projects(request: ProjectRewriteRequest):
    try:

        projects = rewrite_projects(
            request.job_description
        )

        return ProjectRewriteResponse(
            projects=projects
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/ats-score",
    response_model=ATSScoreResponse
)
def ats_score(request: ATSScoreRequest):
    try:

        analysis = analyze_job_description(
            request.job_description
        )

        skill_match = match_skills(
            analysis["skills"]
        )

        project_ranking = rank_projects(
            request.job_description
        )

        result = calculate_ats_score(
            skill_match,
            project_ranking,
        )

        return ATSScoreResponse(
            **result
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.post(
    "/optimize-resume",
    response_model=OptimizedResumeResponse
)
def optimize_ai_resume(request: OptimizedResumeRequest):
    try:

        result = optimize_resume(
            request.job_description
        )

        return OptimizedResumeResponse(
            **result
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
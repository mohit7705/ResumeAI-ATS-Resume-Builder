from pydantic import BaseModel, Field
from typing import List


class JobDescriptionRequest(BaseModel):
    job_description: str = Field(
        ...,
        min_length=20,
        description="Complete job description pasted by the user."
    )


class JobDescriptionResponse(BaseModel):
    role: str
    experience: str
    skills: List[str]
    inferred_skills: List[str] = Field(default_factory=list)
    needed_categories: List[str] = Field(default_factory=list)
    keywords: List[str]
    responsibilities: List[str]

class ConfirmedResumeRequest(JobDescriptionRequest):
    confirmed_skills: list[str] = Field(
        default_factory=list,
        description="Missing skills the candidate explicitly confirms knowing."
    )

class SkillMatchRequest(BaseModel):
    job_skills: list[str]


class SkillMatchResponse(BaseModel):
    matching_skills: list[str]
    missing_skills: list[str]
    additional_resume_skills: list[str]
    match_percentage: int
    recommendations: list[str]
    
class RankedProject(BaseModel):
    title: str
    score: int
    reason: str
    matched_skills: list[str]
    matched_keywords: list[str]


class ProjectRankingRequest(BaseModel):
    job_description: str


class ProjectRankingResponse(BaseModel):
    ranked_projects: list[RankedProject]
    top_projects: list[RankedProject]

class SummaryRequest(BaseModel):
    job_description: str


class SummaryResponse(BaseModel):
    summary: str

class ProjectRewriteRequest(BaseModel):
    job_description: str


class RewrittenProject(BaseModel):
    title: str
    github: str
    live_demo: str
    technologies: list[str]
    highlights: list[str]
    keywords: list[str]
    featured: bool


class ProjectRewriteResponse(BaseModel):
    projects: list[RewrittenProject]

class ATSScoreRequest(BaseModel):
    job_description: str


class ATSScoreResponse(BaseModel):
    ats_score: int
    skill_score: int
    project_score: int

class OptimizedResumeRequest(BaseModel):
    job_description: str


class OptimizedResumeResponse(BaseModel):
    analysis: dict
    skill_match: dict
    project_ranking: dict
    summary: str
    projects: list[RewrittenProject]
    ats_score: dict


class SkillPreviewResponse(BaseModel):
    analysis: dict
    skill_match: dict


class ConfirmedSkillsRequest(BaseModel):
    job_description: str = Field(
        ...,
        min_length=20,
        description="Complete job description pasted by the user."
    )
    confirmed_skills: list[str] = Field(
        default_factory=list,
        description=(
            "Skills the candidate explicitly confirms knowing. "
            "Do not include unconfirmed job requirements."
        )
    )

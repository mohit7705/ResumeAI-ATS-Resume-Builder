from typing import Literal

from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    job_description: str


class ConfirmedResumeRequest(JobDescriptionRequest):
    confirmed_skills: list[str] = Field(default_factory=list)
    # Bold the job keywords in the resume. Mirrors the frontend checkbox.
    highlight: bool = True
    include_photo: bool = True
    # AI provider for this one request. None = use LLM_PROVIDER from .env.
    provider: Literal["gemini", "meta"] | None = None


class DefaultResumeRequest(BaseModel):
    include_photo: bool = True
    # AI provider for this one request. None = use LLM_PROVIDER from .env.
    provider: Literal["gemini", "meta"] | None = None


class TitleResumeRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=80)
    level: Literal["Fresher", "Junior"] = "Fresher"
    # Bold the job keywords in the resume. Mirrors the frontend checkbox.
    highlight: bool = True
    include_photo: bool = True
    # AI provider for this one request. None = use LLM_PROVIDER from .env.
    provider: Literal["gemini", "meta"] | None = None

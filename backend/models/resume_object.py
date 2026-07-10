from pydantic import BaseModel, Field
from typing import List, Dict, Any


class ResumeObject(BaseModel):
    header: Dict[str, Any] = Field(default_factory=dict)

    summary: Dict[str, Any] = Field(default_factory=dict)

    skills: Dict[str, List[str]] = Field(default_factory=dict)

    projects: List[Dict[str, Any]] = Field(default_factory=list)

    experience: List[Dict[str, Any]] = Field(default_factory=list)

    education: List[Dict[str, Any]] = Field(default_factory=list)

    certifications: List[Dict[str, Any]] = Field(default_factory=list)

    achievements: List[Dict[str, Any]] = Field(default_factory=list)
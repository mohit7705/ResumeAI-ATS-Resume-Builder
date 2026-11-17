import copy

from backend.models.resume_object import ResumeObject


def build_resume(
    personal,
    summary,
    skills,
    projects,
):

    return ResumeObject(

        header={
            **personal.get("profile", {}),
            **personal.get("contact", {}),
        },

        summary={
            "content": summary
        },

        skills=skills,

        projects=(projects or [])[:3],

        education=personal.get(
            "education",
            []
        ),

        experience=copy.deepcopy(
            personal.get("experience", [])
        ),

        certifications=personal.get(
            "certifications",
            []
        ),

        achievements=personal.get(
            "achievements",
            []
        ),
    )

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

        projects=projects,

        education=personal.get(
            "education",
            []
        ),

        experience=personal.get(
            "experience",
            []
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
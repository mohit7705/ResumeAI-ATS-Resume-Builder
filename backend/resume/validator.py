REQUIRED_HEADER = [
    "full_name",
    "professional_title",
    "email",
    "phone",
]


def validate_resume(resume, source_experience=None):
    """Check the header and that Experience is exactly what was saved."""
    missing = [
        field for field in REQUIRED_HEADER
        if not resume.header.get(field)
    ]
    experience_unchanged = (
        True
        if source_experience is None
        else resume.experience == source_experience
    )
    return {
        "valid": len(missing) == 0 and experience_unchanged,
        "missing": missing,
        "experience_unchanged": experience_unchanged,
    }

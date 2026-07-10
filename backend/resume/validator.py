REQUIRED_HEADER = [
    "full_name",
    "professional_title",
    "email",
    "phone",
]


def validate_resume(resume):

    missing = []

    header = resume.header

    for field in REQUIRED_HEADER:

        if not header.get(field):
            missing.append(field)

    return {
        "valid": len(missing) == 0,
        "missing": missing,
    }
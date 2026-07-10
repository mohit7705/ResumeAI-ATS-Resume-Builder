def calculate_ats_score(
    skill_match: dict,
    project_ranking: dict,
):
    """
    Calculate ATS score.

    Weightage:
    - Skill Match : 45%
    - Project Match : 45%
    - Resume Completeness Bonus : 10%
    """

    skill_score = skill_match["match_percentage"]

    projects = project_ranking["top_projects"]

    if projects:
        project_score = round(
            sum(project["score"] for project in projects)
            / len(projects)
        )
    else:
        project_score = 0

    # Bonus for strong profile
    bonus = 0

    if skill_score >= 70:
        bonus += 5

    if project_score >= 80:
        bonus += 5

    ats_score = round(
        (skill_score * 0.45)
        + (project_score * 0.45)
        + bonus
    )

    ats_score = min(100, ats_score)

    return {
        "ats_score": ats_score,
        "skill_score": skill_score,
        "project_score": project_score,
    }
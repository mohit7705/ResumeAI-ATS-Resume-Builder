from backend.resume.scorer import score_project


def select_projects(projects: list, keywords: list, limit: int = 3):
    ranked = []

    for project in projects:
        ranked.append(
            {
                "score": score_project(project, keywords),
                "project": project
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        item["project"]
        for item in ranked[:limit]
        if item["score"] > 0
    ]
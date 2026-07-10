def score_project(project: dict, keywords: list[str]) -> int:
    score = 0

    project_keywords = [
        k.lower()
        for k in project.get("keywords", [])
    ]

    technologies = [
        t.lower()
        for t in project.get("technologies", [])
    ]

    for keyword in keywords:
        if keyword in project_keywords:
            score += 10

        if keyword in technologies:
            score += 8

    if project.get("featured"):
        score += 5

    return score
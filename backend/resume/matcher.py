def match_skills(job_keywords: list[str], skills: dict):
    matched = {}

    keywords = [k.lower() for k in job_keywords]

    for category, items in skills.items():
        matched_items = []

        for item in items:
            if isinstance(item, dict):
                name = item["name"]
            else:
                name = str(item)

            # Handle comma-separated skills
            parts = [s.strip() for s in name.split(",")]

            for skill in parts:
                if any(keyword in skill.lower() or skill.lower() in keyword for keyword in keywords):
                    matched_items.append(skill)

        if matched_items:
            matched[category] = matched_items

    return matched
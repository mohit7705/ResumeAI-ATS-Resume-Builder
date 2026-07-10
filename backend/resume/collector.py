from pathlib import Path
import json


DATA = Path("data")


def load(relative_path, default):

    file = DATA / relative_path

    if not file.exists():
        return default

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_resume_data():

    return {

        "profile": load("personal/profile.json", {}),

        "contact": load("personal/contact.json", {}),

        "education": load("personal/education.json", []),

        "experience": load("personal/experience.json", []),

        "skills": load("personal/skills.json", {}),

        "projects": load("personal/projects.json", []),

        "certifications": load("personal/certifications.json", []),

        "achievements": load("personal/achievements.json", [])

    }
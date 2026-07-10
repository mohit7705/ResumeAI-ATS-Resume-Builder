from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader

# ============================
# Directories
# ============================

OUTPUT_HTML = Path("generated/html")
OUTPUT_CSS = Path("generated/css")

OUTPUT_HTML.mkdir(parents=True, exist_ok=True)
OUTPUT_CSS.mkdir(parents=True, exist_ok=True)

TEMPLATE_HTML = Path("templates/html")
TEMPLATE_CSS = Path("templates/css")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_HTML)
)


def generate_html(resume):
    template = env.get_template("ats_one_page.html")

    html = template.render(
        header=resume.header,
        summary=resume.summary,
        skills=resume.skills,
        projects=resume.projects,
        education=resume.education,
        experience=resume.experience,
        certifications=resume.certifications,
        achievements=resume.achievements,
    )

    output_file = OUTPUT_HTML / "resume.html"

    output_file.write_text(
        html,
        encoding="utf-8"
    )

    # ============================
    # Copy CSS automatically
    # ============================

    shutil.copy(
        TEMPLATE_CSS / "ats.css",
        OUTPUT_CSS / "ats.css"
    )

    if (TEMPLATE_CSS / "print.css").exists():
        shutil.copy(
            TEMPLATE_CSS / "print.css",
            OUTPUT_CSS / "print.css"
        )

    themes_src = TEMPLATE_CSS / "themes"
    themes_dst = OUTPUT_CSS / "themes"

    if themes_src.exists():
        shutil.copytree(
            themes_src,
            themes_dst,
            dirs_exist_ok=True
        )

    return output_file
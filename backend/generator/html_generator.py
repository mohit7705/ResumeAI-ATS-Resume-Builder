from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader

from backend.core.config import BASE_DIR
from backend.resume.highlighter import highlight_html


# =========================================================
# DIRECTORIES
# =========================================================

OUTPUT_HTML = Path("generated/html")
OUTPUT_CSS = Path("generated/css")
OUTPUT_ASSETS = Path("generated/assets")

TEMPLATE_HTML = Path("templates/html")
TEMPLATE_CSS = Path("templates/css")

OUTPUT_HTML.mkdir(parents=True, exist_ok=True)
OUTPUT_CSS.mkdir(parents=True, exist_ok=True)
OUTPUT_ASSETS.mkdir(parents=True, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_HTML)
)

from datetime import datetime


def month_year(value):
    """'2026-11' -> 'Nov 2026'. Empty value -> ''."""
    if not value:
        return ""
    try:
        return datetime.strptime(str(value), "%Y-%m").strftime("%b %Y")
    except ValueError:
        return str(value)


env.filters["month_year"] = month_year


# =========================================================
# COPY CSS FILES AND THEMES
# =========================================================

def copy_css_assets(template_name):
    """Copy the CSS files required by the selected template."""

    css_files = ["print.css"]

    if template_name == "ats_one_page_photo.html":
        css_files.append("ats_photo.css")
    else:
        css_files.append("ats.css")

    for filename in css_files:
        source = TEMPLATE_CSS / filename

        if not source.is_file():
            raise FileNotFoundError(
                f"Required CSS file not found: {source}"
            )

        shutil.copy2(
            source,
            OUTPUT_CSS / filename,
        )

    themes_source = TEMPLATE_CSS / "themes"
    themes_output = OUTPUT_CSS / "themes"

    if themes_source.is_dir():
        shutil.copytree(
            themes_source,
            themes_output,
            dirs_exist_ok=True,
        )


# =========================================================
# PROFILE PHOTO
# =========================================================

ASSETS_DIR = BASE_DIR / "assets"
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class PhotoError(ValueError):
    """Photo configuration problem returned to the API as a clear 400."""


def find_profile_photo(assets_dir=None) -> Path:
    """Return the only JPG, JPEG, or PNG in the assets folder."""
    folder = Path(assets_dir) if assets_dir else ASSETS_DIR

    if not folder.is_dir():
        raise PhotoError(f"Assets folder not found: {folder}")

    photos = sorted(
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in PHOTO_EXTENSIONS
    )

    if not photos:
        raise PhotoError(
            f"No photo found in the assets folder ({folder}). "
            "Add one .jpg or .png file."
        )

    if len(photos) > 1:
        names = ", ".join(file.name for file in photos)
        raise PhotoError(
            f"Found {len(photos)} photos in the assets folder: {names}. "
            "Keep only ONE .jpg or .png file there and delete the others."
        )

    return photos[0]


def copy_default_photo(photo_path=None):
    """Copy the profile photo into generated assets."""
    source = Path(photo_path) if photo_path else find_profile_photo()

    if not source.is_file():
        raise PhotoError(f"Profile photo not found: {source}")

    extension = source.suffix.lower()
    if extension not in PHOTO_EXTENSIONS:
        raise PhotoError("Unsupported photo format. Use .jpg or .png.")

    for old in OUTPUT_ASSETS.glob("photo.*"):
        old.unlink(missing_ok=True)

    destination = OUTPUT_ASSETS / f"photo{extension}"

    shutil.copy2(
        source,
        destination,
    )

    # Path relative to generated/html/resume_photo.html
    return f"../assets/photo{extension}"


# =========================================================
# GENERATE RESUME HTML
# =========================================================

def generate_html(
    resume,
    template_name="ats_one_page.html",
    photo_path=None,
    highlight_keywords=None,
    highlight_report=None,
):
    """Generate HTML using the selected resume template.

    highlight_keywords: job keywords to bold. None or empty = no bolding.
    highlight_report: optional list; the keywords actually bolded are
    added to it so the caller can show them.
    """

    allowed_templates = {
        "ats_one_page.html",
        "ats_one_page_photo.html",
    }

    if template_name not in allowed_templates:
        raise ValueError(
            f"Unsupported resume template: {template_name}"
        )

    template = env.get_template(template_name)

    # Copy the header so the original resume data isn't modified.
    original_header = resume.header

    if isinstance(original_header, dict):
        header = original_header.copy()
    else:
        header = original_header.model_dump()

    if template_name == "ats_one_page_photo.html":
        header["photo"] = copy_default_photo(photo_path)

    html = template.render(
        header=header,
        summary=resume.summary,
        skills=resume.skills,
        projects=resume.projects,
        education=resume.education,
        experience=resume.experience,
        certifications=resume.certifications,
        achievements=resume.achievements,
    )

    if highlight_keywords:
        html, bolded = highlight_html(html, highlight_keywords)

        if highlight_report is not None:
            highlight_report.extend(bolded)

    output_name = (
        "resume_photo.html"
        if template_name == "ats_one_page_photo.html"
        else "resume.html"
    )

    output_file = OUTPUT_HTML / output_name

    output_file.write_text(
        html,
        encoding="utf-8",
    )

    copy_css_assets(template_name)

    return output_file

"""Bold the job-description keywords in a rendered resume.

This runs AFTER the template has been rendered, so the saved resume data is
never touched and the same code works for every template. Bold is plain
formatting: ATS software reads exactly the same text with or without it. The
only goal is to help a recruiter spot the matching words during a quick skim.

Rules (kept deliberately conservative so the page does not look cluttered):
  * Only explicit job keywords are used, never "inferred" ones.
  * Technical Skills section: every matching skill is bold.
  * Summary and bullets: only the FIRST mention of each keyword is bold,
    at most MAX_PER_BLOCK per bullet and MAX_PROSE_HIGHLIGHTS in total.
  * Names, links, education and other sections are never touched.
"""

import re

from bs4 import BeautifulSoup, Comment, NavigableString

MAX_PROSE_HIGHLIGHTS = 8
MAX_PER_BLOCK = 2
MAX_KEYWORD_WORDS = 4
MAX_KEYWORD_LENGTH = 40

# Words that appear in almost every job description and mean nothing to a
# recruiter who is scanning for technical fit.
GENERIC_TERMS = {
    "communication", "teamwork", "team", "collaboration", "leadership",
    "problem solving", "problem-solving", "software", "development",
    "engineering", "experience", "skills", "knowledge", "design",
    "systems", "applications", "application", "technology", "technologies",
    "tools", "work", "project", "projects", "solutions", "environment",
    "agile", "fast-paced", "passion", "learning", "strong", "ability",
}

# Different spellings of the same thing. Any spelling found in the resume is
# bolded when the job description uses any one of them.
ALIAS_GROUPS = [
    ("REST API", "REST APIs", "RESTful API", "RESTful APIs"),
    ("PostgreSQL", "Postgres"),
    ("JavaScript", "JS"),
    ("TypeScript", "TS"),
    ("Scikit-learn", "scikit learn", "sklearn"),
    ("Machine Learning", "ML"),
    ("Node.js", "NodeJS", "Node"),
    ("Express.js", "ExpressJS", "Express"),
    ("React", "React.js", "ReactJS"),
    ("Microsoft Azure", "Azure"),
    ("Google Cloud Platform", "Google Cloud", "GCP"),
    ("Object-Oriented Programming", "Object Oriented Programming", "OOP", "OOPs"),
    ("CI/CD", "CI CD"),
    ("Kubernetes", "K8s"),
    ("DBMS", "Database Management Systems"),
    ("Retrieval-Augmented Generation", "Retrieval Augmented Generation", "RAG"),
    ("Vector Database", "Vector Databases", "Vector DB", "Vector Embeddings"),
    ("Multi-Agent Systems", "Multi-Agent", "Agentic Workflows"),
]

_ALIAS_LOOKUP = {}
for _index, _group in enumerate(ALIAS_GROUPS):
    for _name in _group:
        _ALIAS_LOOKUP[_name.casefold()] = _index


def collect_keywords(analysis: dict) -> list[str]:
    """Pick the keywords worth bolding from the job-description analysis.

    Explicit skills come first, then explicit keywords. Inferred skills are
    ignored because the employer never asked for them.
    """
    if not isinstance(analysis, dict):
        return []

    result = []
    seen = set()

    for field in ("skills", "keywords"):
        values = analysis.get(field, [])

        if not isinstance(values, list):
            continue

        for value in values:
            if not isinstance(value, str):
                continue

            keyword = " ".join(value.split()).strip(" ,.;:()[]")
            key = keyword.casefold()

            if not keyword or not re.search(r"[A-Za-z0-9]", keyword):
                continue

            if key in GENERIC_TERMS or key in seen:
                continue

            if len(keyword) > MAX_KEYWORD_LENGTH:
                continue

            if len(keyword.split()) > MAX_KEYWORD_WORDS:
                continue

            seen.add(key)
            result.append(keyword)

    return result


def _variant_pattern(variant: str) -> str:
    """Regex for one spelling of a keyword."""
    escaped = re.escape(variant).replace(r"\ ", r"\s+")

    # A plural 's' is allowed on longer words (API -> APIs).
    if len(variant) > 2 and variant[-1].isalpha():
        escaped += "s?"

    # One or two letter terms (C, R, Go, JS) must match case exactly,
    # otherwise "r" or "go" in a normal sentence would be bolded.
    if len(variant) <= 2:
        escaped = f"(?-i:{escaped})"

    return escaped


def _build_matcher(keywords: list[str]):
    """Return (compiled regex, variant -> keyword) for the keyword list."""
    variant_to_keyword = {}
    spelling = {}
    group_keyword = {}

    def add(name: str, canonical: str) -> None:
        key = name.casefold()

        if key not in variant_to_keyword:
            variant_to_keyword[key] = canonical
            spelling[key] = name

    for keyword in keywords:
        group = _ALIAS_LOOKUP.get(keyword.casefold())

        if group is None:
            add(keyword, keyword)
            continue

        # Every spelling in the group maps to the first spelling the job
        # description used, so it is reported once.
        canonical = group_keyword.setdefault(group, keyword)

        for name in ALIAS_GROUPS[group]:
            add(name, canonical)

        add(keyword, canonical)

    if not variant_to_keyword:
        return None, {}

    # Longest first, so "Gemini API" wins over "Gemini".
    ordered = sorted(spelling.values(), key=len, reverse=True)

    alternatives = "|".join(_variant_pattern(name) for name in ordered)

    pattern = re.compile(
        rf"(?<![A-Za-z0-9+#\-])(?:{alternatives})(?![A-Za-z0-9+#])",
        re.IGNORECASE,
    )

    return pattern, variant_to_keyword


def _canonical(matched: str, variant_to_keyword: dict) -> str | None:
    """Map matched resume text back to the job keyword it stands for."""
    key = " ".join(matched.split()).casefold()

    if key in variant_to_keyword:
        return variant_to_keyword[key]

    # Plural match, e.g. "APIs" for the keyword "API".
    if key.endswith("s") and key[:-1] in variant_to_keyword:
        return variant_to_keyword[key[:-1]]

    return None


def highlight_html(html: str, keywords: list[str]) -> tuple[str, list[str]]:
    """Bold job keywords in rendered resume HTML.

    Returns (new_html, keywords_that_were_bolded). When there is nothing to
    bold the original HTML is returned unchanged.
    """
    pattern, variant_to_keyword = _build_matcher(keywords)

    if pattern is None:
        return html, []

    soup = BeautifulSoup(html, "html.parser")

    used: list[str] = []
    seen_in_prose: set[str] = set()
    prose_count = 0

    def bold_in_block(block, *, prose: bool) -> None:
        nonlocal prose_count
        block_count = 0

        for node in list(block.find_all(string=True)):
            if isinstance(node, Comment):
                continue

            # Never touch text that is already emphasised or is a link.
            if node.find_parent(["b", "strong", "a", "script", "style"]):
                continue

            text = str(node)
            parts = []
            cursor = 0

            for match in pattern.finditer(text):
                keyword = _canonical(match.group(0), variant_to_keyword)

                if keyword is None:
                    continue

                if prose:
                    if (
                        keyword in seen_in_prose
                        or block_count >= MAX_PER_BLOCK
                        or prose_count >= MAX_PROSE_HIGHLIGHTS
                    ):
                        continue

                    seen_in_prose.add(keyword)
                    block_count += 1
                    prose_count += 1

                if keyword not in used:
                    used.append(keyword)

                tag = soup.new_tag("strong", attrs={"class": "kw"})
                tag.string = match.group(0)

                if match.start() > cursor:
                    parts.append(NavigableString(text[cursor:match.start()]))

                parts.append(tag)
                cursor = match.end()

            if not parts:
                continue

            if cursor < len(text):
                parts.append(NavigableString(text[cursor:]))

            node.replace_with(*parts)

    for section in soup.select("div.section"):
        heading = section.find("h2")
        name = heading.get_text(strip=True).casefold() if heading else ""

        if name == "summary":
            for paragraph in section.find_all("p"):
                bold_in_block(paragraph, prose=True)

        elif name == "technical skills":
            for value in section.select(".skill-value"):
                bold_in_block(value, prose=False)

        elif name == "projects":
            for bullet in section.find_all("li"):
                bold_in_block(bullet, prose=True)

    if not used:
        return html, []

    return str(soup), used

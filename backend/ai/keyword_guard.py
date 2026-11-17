"""Keep project bullets honest, technically sharp, and grounded in project evidence."""

import re

MAX_BULLETS = 3
MAX_WORDS = 28
HARD_MAX_WORDS = 32
MAX_TECH_SHOWN = 6

# Only ban empty marketing buzzwords; keep real systems-engineering adjectives.
BANNED_WORDS = {
    "leveraged", "leveraging", "spearheaded", "orchestrated", "utilized",
    "utilizing", "synergy", "seamless", "seamlessly", "cutting-edge",
    "state-of-the-art", "innovative", "holistic", "dynamic",
    "revolutionary", "game-changing", "passionate", "harnessed", "empowered",
}

HARD_TO_EASY = {
    "leveraged": "used", "leveraging": "using", "utilized": "used",
    "utilizing": "using", "utilised": "used", "spearheaded": "led",
    "orchestrated": "coordinated", "seamless": "smooth",
    "seamlessly": "smoothly", "cutting-edge": "modern",
    "state-of-the-art": "modern", "innovative": "novel",
    "empowered": "enabled", "harnessed": "used",
    "dynamic": "adaptive", "holistic": "complete",
    "pivotal": "key", "proficient": "skilled", "adept": "skilled",
    "passionate": "focused", "revolutionary": "novel",
    "game-changing": "high-impact", "synergy": "collaboration",
}


def simplify(text: str) -> str:
    for hard, easy in HARD_TO_EASY.items():
        text = re.sub(
            r"(?<![A-Za-z0-9])" + re.escape(hard) + r"(?![A-Za-z0-9])",
            easy,
            text,
            flags=re.IGNORECASE,
        )
    return text


PROPER_NAMES = {
    "python": "Python", "fastapi": "FastAPI", "ffmpeg": "FFmpeg",
    "postgresql": "PostgreSQL", "mongodb": "MongoDB", "mysql": "MySQL",
    "react": "React", "scikit-learn": "Scikit-learn", "whisper": "Whisper",
    "sql": "SQL", "api": "API", "apis": "APIs", "ai": "AI", "ml": "ML",
    "youtube": "YouTube", "github": "GitHub", "rag": "RAG", "llm": "LLM",
    "llms": "LLMs", "gcp": "GCP", "aws": "AWS", "langgraph": "LangGraph",
    "chromadb": "ChromaDB", "pgvector": "pgvector", "vertex ai": "Vertex AI",
    "cloud run": "Cloud Run", "docker": "Docker", "typescript": "TypeScript",
    "rest api": "REST API",
}


def proper_case(text: str) -> str:
    # Fix accidental "Al" (A-lowercase-L) typos in AI terms
    text = re.sub(r"\bResumeAl\b", "ResumeAI", text)
    text = re.sub(r"\bAl\b(?=\s+(?:YouTube|ML|app|risk|pipeline|system|model|solution))", "AI", text)
    for low, good in PROPER_NAMES.items():
        text = re.sub(
            r"(?<![A-Za-z0-9])" + re.escape(low) + r"(?![A-Za-z0-9])",
            good,
            text,
            flags=re.IGNORECASE,
        )
    return text


GENERIC_TERMS = {
    "communication", "teamwork", "team", "collaboration", "leadership",
    "problem solving", "problem-solving", "software", "development",
    "engineering", "experience", "skills", "knowledge", "design", "systems",
    "applications", "application", "technology", "technologies", "tools",
    "work", "project", "projects", "solutions", "environment", "agile",
    "learning", "strong", "ability", "programming", "coding",
}

CONCEPTS = {
    "fastapi": ["rest api", "backend", "api", "web services", "microservices"],
    "flask": ["rest api", "backend", "api"],
    "django": ["rest api", "backend", "api"],
    "node.js": ["backend", "rest api", "javascript"],
    "express.js": ["backend", "rest api", "api"],
    "react": ["frontend", "web development", "ui"],
    "tailwind css": ["frontend", "css", "ui"],
    "typescript": ["frontend", "javascript"],
    "python": ["scripting", "automation", "data pipelines"],
    "whisper": ["speech to text", "speech recognition", "audio pipeline"],
    "faster-whisper": ["speech to text", "speech recognition", "low latency"],
    "gemini api": ["llm", "generative ai", "prompt engineering", "ai", "structured output"],
    "gemini ai": ["llm", "generative ai", "prompt engineering", "ai"],
    "vertex ai": ["gcp", "google cloud", "llm", "enterprise ai", "model deployment"],
    "cloud run": ["gcp", "google cloud", "serverless", "docker", "production deployment"],
    "langgraph": ["multi-agent", "agentic workflows", "state management", "self-reflection"],
    "adk": ["multi-agent", "agentic workflows", "google cloud"],
    "chromadb": ["vector database", "rag", "semantic search", "embeddings"],
    "pgvector": ["vector database", "rag", "semantic search", "postgresql", "embeddings"],
    "rag": ["retrieval augmented generation", "vector database", "semantic search"],
    "ollama": ["llm", "generative ai", "local inference"],
    "vision ai": ["computer vision", "ai"],
    "opencv": ["computer vision", "image processing"],
    "ffmpeg": ["video processing", "media pipeline", "automation"],
    "postgresql": ["sql", "database", "relational database", "rdbms"],
    "mysql": ["sql", "database", "relational database", "rdbms"],
    "mongodb": ["nosql", "database"],
    "scikit-learn": ["machine learning", "ml", "model training", "risk scoring"],
    "tensorflow": ["machine learning", "deep learning", "ml"],
    "pytorch": ["machine learning", "deep learning", "ml"],
    "shap": ["explainable ai", "model interpretability"],
    "docker": ["containerization", "deployment", "ci/cd"],
}

ALIASES = {
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "postgres": "postgresql",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "js": "javascript",
    "ts": "typescript",
    "nodejs": "node.js",
    "node": "node.js",
    "expressjs": "express.js",
    "express": "express.js",
    "reactjs": "react",
    "react.js": "react",
    "ml": "machine learning",
    "gemini": "gemini api",
    "google gemini ai": "gemini api",
    "faster whisper": "faster-whisper",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "vector databases": "vector database",
    "vector db": "vector database",
    "multi-agent systems": "multi-agent",
    "agentic": "agentic workflows",
}


def norm(value) -> str:
    if not isinstance(value, str):
        return ""
    key = " ".join(value.strip().casefold().split())
    return ALIASES.get(key, key)


def has_word(text: str, term: str) -> bool:
    return re.search(
        r"(?<![a-z0-9])" + re.escape(term.casefold()) + r"(?![a-z0-9])",
        text.casefold(),
    ) is not None


def job_terms(
    analysis: dict,
    fields=("skills", "inferred_skills", "keywords"),
) -> list:
    out, seen = [], set()
    for field in fields:
        for value in (analysis or {}).get(field, []) or []:
            key = norm(value)
            if (
                not key
                or key in GENERIC_TERMS
                or key in seen
                or len(key) > 40
                or len(key.split()) > 3
            ):
                continue
            seen.add(key)
            out.append(key)
    return out


def project_terms(project: dict) -> set:
    terms = set()
    for field in ("technologies", "keywords"):
        for value in project.get(field, []) or []:
            key = norm(value)
            terms.add(key)
            terms.update(CONCEPTS.get(key, []))
    return terms


def usable_keywords(project: dict, analysis: dict) -> list:
    supported = project_terms(project)
    return [term for term in job_terms(analysis) if term in supported][:10]


def display_technologies(project: dict, analysis: dict) -> list:
    technologies = [
        value for value in project.get("technologies", []) or []
        if isinstance(value, str)
    ]
    wanted = set(job_terms(analysis))

    def relevant(technology):
        key = norm(technology)
        return key in wanted or any(
            concept in wanted for concept in CONCEPTS.get(key, [])
        )

    ordered = sorted(
        technologies,
        key=lambda technology: (
            0 if relevant(technology) else 1,
            technologies.index(technology),
        ),
    )
    return ordered[:MAX_TECH_SHOWN]


def _shorten(bullet: str) -> str:
    bullet = " ".join(bullet.split()).rstrip(" .;")
    words = bullet.split()
    if len(words) <= MAX_WORDS:
        return bullet

    cut = ", ".join(bullet.split(", ")[:-1]) if ", " in bullet else ""
    if cut and 12 <= len(cut.split()) <= HARD_MAX_WORDS:
        return cut
    return " ".join(words[:HARD_MAX_WORDS])


def validate_bullets(bullets: list, project: dict, analysis: dict) -> tuple[list, list]:
    """Validate generated bullets and return (accepted_bullets, critique_reasons)."""
    supported = project_terms(project)
    asked_technologies = [
        term
        for term in job_terms(analysis, ("skills", "inferred_skills"))
        if term not in supported and term not in GENERIC_TERMS
    ]

    accepted = []
    critiques = []

    for raw in bullets or []:
        if not isinstance(raw, str) or not raw.strip():
            continue
        text = simplify(_shorten(raw))

        bad_words = [w for w in BANNED_WORDS if has_word(text, w)]
        if bad_words:
            critiques.append(f"Bullet '{text[:40]}...' used banned buzzwords: {bad_words}")
            continue

        hallucinated = [t for t in asked_technologies if has_word(text, t)]
        if hallucinated:
            critiques.append(
                f"Bullet '{text[:40]}...' claimed unsupported JD technologies: {hallucinated}"
            )
            continue

        accepted.append(proper_case(text))

    if len(accepted) < MAX_BULLETS and not critiques:
        critiques.append(f"Returned {len(accepted)} valid bullets; need exactly {MAX_BULLETS}.")

    return accepted[:MAX_BULLETS], critiques


def clean_bullets(bullets: list, project: dict, analysis: dict) -> list:
    accepted, _ = validate_bullets(bullets, project, analysis)
    return accepted


def fallback_bullets(project: dict) -> list:
    out = []
    for line in project.get("highlights", []) or []:
        if isinstance(line, str) and line.strip():
            first = re.split(r"(?<=[.!?])\s", line.strip())[0]
            out.append(proper_case(_shorten(first)))
    return out[:MAX_BULLETS]

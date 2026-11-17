import contextlib
import contextvars
import inspect
import json
import logging
import os
import threading
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.ai.meta_client import meta_available, meta_generate, meta_settings

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

log = logging.getLogger("resumeai.llm")
_client = None
_client_lock = threading.Lock()


def _get_client():
    global _client
    with _client_lock:
        if _client is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError("GOOGLE_API_KEY not found in .env")
            _client = genai.Client(api_key=api_key)
        return _client


def _model() -> str:
    model = os.getenv("GOOGLE_MODEL")
    if not model:
        raise RuntimeError("GOOGLE_MODEL not found in .env")
    return model


_working_level = 0
_level_lock = threading.Lock()


def _config(json_mode: bool, max_output_tokens: int, level: int):
    kwargs = {
        "temperature": 0.2,
        "max_output_tokens": max_output_tokens,
    }
    if json_mode and level <= 1:
        kwargs["response_mime_type"] = "application/json"
    if level == 0:
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
    return types.GenerateContentConfig(**kwargs)


def _is_temporary(message: str) -> bool:
    upper = message.upper()
    return any(
        code in upper
        for code in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500", "DEADLINE")
    )


def _is_bad_argument(message: str) -> bool:
    upper = message.upper()
    return "INVALID_ARGUMENT" in upper or "400" in upper


def _gemini_analyze(
    prompt: str,
    json_mode: bool = False,
    max_output_tokens: int = 1200,
) -> str:
    """Send one prompt to Gemini with compatible settings and retries."""
    global _working_level

    client = _get_client()
    model = _model()
    started = time.perf_counter()
    temporary_retries = 0

    while True:
        with _level_lock:
            level = _working_level
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=_config(json_mode, max_output_tokens, level),
            )
            log.info(
                "gemini ok %.1fs level=%d json=%s prompt_chars=%d",
                time.perf_counter() - started,
                level,
                json_mode,
                len(prompt),
            )
            return str(response.text or "").strip()
        except Exception as error:
            message = str(error)
            if _is_bad_argument(message) and level < 2:
                with _level_lock:
                    _working_level = max(_working_level, level + 1)
                log.warning(
                    "model rejected a setting (level %d), retrying simpler: %s",
                    level,
                    message[:150],
                )
                continue
            if _is_temporary(message) and temporary_retries < 2:
                temporary_retries += 1
                log.warning(
                    "gemini temporary error, retry in %ss: %s",
                    temporary_retries,
                    message[:200],
                )
                time.sleep(temporary_retries)
                continue
            raise RuntimeError(f"Gemini API Error: {message}") from error


PROVIDERS = ("gemini", "meta")
_request_provider = contextvars.ContextVar("request_provider", default=None)
_GEMINI_ACCEPTS = set(inspect.signature(_gemini_analyze).parameters)


def set_request_provider(name):
    """Choose the provider for the current request (None = use .env)."""
    if name is not None and name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Use gemini or meta.")
    return _request_provider.set(name)


def default_provider() -> str:
    value = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if value not in PROVIDERS:
        raise ValueError(f"LLM_PROVIDER must be gemini or meta, not '{value}'")
    return value


def active_provider() -> str:
    return _request_provider.get() or default_provider()


def provider_status() -> dict:
    """Return configured provider status without exposing API keys."""
    gemini_model = os.getenv("GOOGLE_MODEL", "").strip()
    return {
        "default": default_provider(),
        "gemini": {
            "available": bool(os.getenv("GOOGLE_API_KEY", "").strip() and gemini_model),
            "model": gemini_model,
        },
        "meta": {"available": meta_available(), "model": meta_settings()["model"]},
    }


@contextlib.contextmanager
def use_provider(name):
    """Select a configured provider for the duration of one request."""
    if name is None:
        yield
        return

    if name not in PROVIDERS:
        raise ValueError(f"Unknown AI provider: {name}. Use gemini or meta.")

    if not provider_status()[name]["available"]:
        label = "Meta" if name == "meta" else "Gemini"
        keys = "META_API_KEY and META_MODEL" if name == "meta" else "GOOGLE_API_KEY and GOOGLE_MODEL"
        raise ValueError(f"{label} is not set up. Add {keys} to the .env file.")

    token = _request_provider.set(name)
    try:
        yield
    finally:
        _request_provider.reset(token)


def with_context(function):
    """Carry the current request context into a worker thread."""
    context = contextvars.copy_context()

    def run(*args, **kwargs):
        return context.run(function, *args, **kwargs)

    return run


def _run_provider(name, prompt, json_mode, max_output_tokens):
    if name == "meta":
        return meta_generate(
            prompt,
            max_output_tokens=max_output_tokens,
            json_mode=json_mode,
        )

    extras = {
        key: value
        for key, value in (
            ("json_mode", json_mode),
            ("max_output_tokens", max_output_tokens),
        )
        if key in _GEMINI_ACCEPTS
    }
    return _gemini_analyze(prompt, **extras)


def analyze(
    prompt: str,
    json_mode: bool = False,
    max_output_tokens: int = 1200,
) -> str:
    """Send a prompt to the selected provider and return plain text."""
    primary = active_provider()
    fallback = os.getenv("LLM_FALLBACK", "").strip().lower()
    started = time.perf_counter()

    try:
        text = _run_provider(primary, prompt, json_mode, max_output_tokens)
        log.info("llm provider=%s %.1fs", primary, time.perf_counter() - started)
        return text
    except Exception as error:
        if fallback in PROVIDERS and fallback != primary:
            log.warning(
                "%s failed (%s). Trying %s.",
                primary,
                str(error)[:200],
                fallback,
            )
            text = _run_provider(fallback, prompt, json_mode, max_output_tokens)
            log.info(
                "llm provider=%s (fallback) %.1fs",
                fallback,
                time.perf_counter() - started,
            )
            return text
        raise



JOB_DESCRIPTION_PROMPT = """
You are an expert technical recruiter and resume analyst.

Analyze the complete job description and identify the most relevant
technical requirements for tailoring a candidate's resume.

Return valid JSON only, without Markdown or additional commentary.

CONDITIONAL SKILL ANALYSIS RULES:

1. FIRST, CHECK FOR EXPLICIT TECHNICAL KEYWORDS.
   - If the job description contains a technical skills list or clearly
     mentions programming languages, frameworks, tools, or technologies,
     extract them into "skills".
   - Analyze the responsibilities and context to determine relevance.
   - Do not automatically add inferred skills when the explicit
     requirements are already sufficient.

   - An explicit list is sufficient only when it adequately covers
     the technical requirements supported by the job description.
   - If responsibilities reveal important technical requirements
     missing from the explicit list, infer only those relevant gaps.
   - Do not infer a technology merely because it is common for the role.


2. IF EXPLICIT KEYWORDS ARE MISSING OR INCOMPLETE:
   - Analyze the job title, responsibilities, engineering practices,
     and technical context.
   - Infer likely relevant technical skills and ATS keywords.
   - Put inferred skills in "inferred_skills", not "skills".
   - Rank inferred skills by relevance.
   - Return no more than 12 inferred skills.
   - Do not assume that every common industry skill is relevant.

2A. HANDLE VAGUE OR AMBIGUOUS REQUIREMENTS:
   - Phrases such as "strong programming skills", "coding ability",
     "software development experience" do not name a language.
   - Do NOT put a language in "skills" or "inferred_skills" for these
     phrases. Instead add "languages" to "needed_categories".
   - The candidate's own languages will be chosen later from the
     candidate's real data.
   - Infer a specific language only when a named framework or tool
     clearly indicates it (for example Django -> Python).


3. IF EXPLICIT KEYWORDS ARE PRESENT BUT INCOMPLETE:
   - Preserve explicitly mentioned skills in "skills".
   - Infer only important missing requirements in "inferred_skills".
   - Do not duplicate explicit skills in the inferred list.

4. EXTRACT ATS KEYWORDS:
   - Include relevant technical concepts, engineering practices,
     tools, systems, and responsibilities supported by the description.
   - Remove duplicates and generic marketing language.
   - Do not invent specific technologies as explicit requirements.

5. EXTRACT RESPONSIBILITIES:
   - Summarize up to 8 important responsibilities.
   - Preserve the technical meaning of the job description.

6. CANDIDATE EVIDENCE AND RESUME ACCURACY:
   - The extracted and inferred skills describe the job, not the
     candidate's proficiency.
   - Never assume the candidate possesses a skill just because
     the role commonly uses it.
   - Candidate skill selection must be handled separately by checking
     the candidate's saved profile, skills, education, and projects.
   - Only relevant, evidence-supported skills should be selected
     for the final resume.
   - Never include the candidate's entire skill list automatically.

6A. NEEDED CATEGORIES (for a fresher resume):
   - Return "needed_categories": choose ONLY from
     [languages, ai_ml, databases, tools, cloud, cs_fundamentals, soft_skills].
   - Include a category when the job names a skill in it OR clearly
     needs it (for example "good programming skills" needs languages;
     "backend role" needs languages, databases, tools; "ML engineer"
     needs ai_ml).
   - Do NOT include a category the job gives no reason for.
     No cloud unless cloud/AWS/Azure/deployment is mentioned.
     No ai_ml unless AI/ML/data science/LLM work is mentioned.
   - Maximum 4 categories.

7. NORMALIZATION:
   - Normalize skill names.
   - Remove duplicates within each list.
   - Keep inferred skills focused, relevant, and ranked by importance.

Return exactly this JSON structure:

{
  "role": "",
  "experience": "",
  "skills": [],
  "inferred_skills": [],
  "needed_categories": [],
  "keywords": [],
  "responsibilities": []
}
"""

# --------------------------------------------------
# Job Description Analyzer
# --------------------------------------------------

def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a Job Description and return structured JSON.
    """

    prompt = (
        f"{JOB_DESCRIPTION_PROMPT}\n\n"
        f"JOB DESCRIPTION TO ANALYZE:\n{job_description}"
    )

    response = analyze(prompt, json_mode=True, max_output_tokens=1500)

    # Remove markdown formatting if Gemini adds it
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # Extract JSON object only
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Gemini did not return a valid JSON object."
        )

    json_text = response[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by Gemini: {str(e)}"
        )

"""Calls the Meta (Muse) chat API and returns plain text.

Works like the Gemini helper: text in, text out. Key, model and URL come
from the .env file in the project root:

    META_API_KEY=...
    META_MODEL=muse-spark-1.1
    META_API_BASE=https://api.meta.ai/v1      (optional)
    META_REASONING_EFFORT=minimal             (optional: minimal|low|medium|high)
    META_JSON_MODE=0                          (optional: 1 = send response_format json)
"""

import logging
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

log = logging.getLogger("resumeai.meta")

ROOT_DIR = Path(__file__).resolve().parents[2]       # same rule as analyzer.py
load_dotenv(ROOT_DIR / ".env")

DEFAULT_BASE = "https://api.meta.ai/v1"
TIMEOUT_SECONDS = 60.0
MAX_TEMPORARY_RETRIES = 2
MAX_TOKEN_GROWTHS = 2          # if the answer is cut off, ask again with more room
TOKEN_GROWTH = 3
TOKEN_CAP = 8000

_transport = None        # tests can put a fake transport here


def meta_settings() -> dict:
    """Read the settings each time, so a changed .env is used after restart only,
    and a missing key is reported when Meta is used (not at server start)."""
    return {
        "api_key": os.getenv("META_API_KEY", "").strip(),
        "model": os.getenv("META_MODEL", "").strip(),
        "base": (os.getenv("META_API_BASE", "").strip() or DEFAULT_BASE).rstrip("/"),
        "reasoning": os.getenv("META_REASONING_EFFORT", "").strip(),
        "json_mode": os.getenv("META_JSON_MODE", "0").strip() == "1",
    }


def meta_available() -> bool:
    s = meta_settings()
    return bool(s["api_key"] and s["model"])


def _build_payload(s: dict, prompt: str, max_output_tokens: int,
                   json_mode: bool, simple: bool, token_key: str) -> dict:
    payload = {
        "model": s["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        token_key: max_output_tokens,
    }
    if not simple:
        # Optional extras. Dropped automatically if the API refuses them.
        if s["reasoning"]:
            payload["reasoning_effort"] = s["reasoning"]
        if json_mode and s["json_mode"]:
            payload["response_format"] = {"type": "json_object"}
    return payload


def _extract_text(data: dict) -> str:
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Meta API returned an unexpected answer: {str(data)[:300]}") from e

    if isinstance(content, list):          # list of parts -> join the text parts
        content = "".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    return str(content or "").strip()


def meta_generate(prompt: str, max_output_tokens: int = 1200, json_mode: bool = False) -> str:
    s = meta_settings()

    if not s["api_key"]:
        raise RuntimeError("META_API_KEY not found in .env")
    if not s["model"]:
        raise RuntimeError("META_MODEL not found in .env")

    url = f"{s['base']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {s['api_key']}",
        "Content-Type": "application/json",
    }

    simple = False                 # step 1: drop optional extras on a 400
    token_key = "max_tokens"       # step 2: try max_completion_tokens on a 400
    temporary = 0
    growths = 0
    started = time.perf_counter()

    with httpx.Client(timeout=TIMEOUT_SECONDS, transport=_transport) as client:
        while True:
            payload = _build_payload(s, prompt, max_output_tokens, json_mode, simple, token_key)

            try:
                response = client.post(url, headers=headers, json=payload)
            except httpx.HTTPError as e:
                if temporary < MAX_TEMPORARY_RETRIES:
                    temporary += 1
                    time.sleep(temporary)
                    continue
                raise RuntimeError(f"Meta API connection error: {e}") from e

            code = response.status_code

            if code == 200:
                data = response.json()
                text = _extract_text(data)
                finish = (data.get("choices") or [{}])[0].get("finish_reason")
                usage = data.get("usage") or {}

                # Cut off because the token limit was reached (the model's own
                # "thinking" also uses these tokens). Ask again with more room.
                if finish in ("length", "max_tokens") and growths < MAX_TOKEN_GROWTHS:
                    growths += 1
                    max_output_tokens = min(max_output_tokens * TOKEN_GROWTH, TOKEN_CAP)
                    log.warning("meta answer cut off (%s), retrying with max tokens=%d usage=%s",
                                finish, max_output_tokens, usage)
                    continue

                log.info("meta ok %.1fs model=%s finish=%s usage=%s prompt_chars=%d",
                         time.perf_counter() - started, s["model"], finish, usage, len(prompt))
                return text

            body = response.text[:400]

            if code in (401, 403):
                raise RuntimeError(f"Meta API key rejected ({code}). Check META_API_KEY. {body}")

            if code == 404:
                raise RuntimeError(f"Meta API 404. Check META_MODEL and META_API_BASE. {body}")

            if code == 400:
                if not simple:
                    simple = True
                    log.warning("meta 400, retrying without optional settings: %s", body[:150])
                    continue
                if token_key == "max_tokens":
                    token_key = "max_completion_tokens"
                    log.warning("meta 400, retrying with max_completion_tokens: %s", body[:150])
                    continue
                raise RuntimeError(f"Meta API Error 400: {body}")

            if code in (429, 500, 502, 503, 504) and temporary < MAX_TEMPORARY_RETRIES:
                temporary += 1
                time.sleep(temporary)           # 1 s, then 2 s
                continue

            raise RuntimeError(f"Meta API Error {code}: {body}")
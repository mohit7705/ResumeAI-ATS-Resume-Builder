import copy
import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any, TypedDict

import chromadb
from langgraph.graph import END, START, StateGraph

from backend.ai.analyzer import active_provider, analyze_job_description
from backend.ai.ats_score import calculate_ats_score
from backend.ai.matcher import match_skills
from backend.ai.project_ranker import rank_projects
from backend.ai.project_rewriter import rewrite_projects
from backend.ai.summary_generator import generate_summary
from backend.utils.timing import timed

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_FILES = (ROOT_DIR / "data" / "personal", ROOT_DIR / "data" / "projects")
CACHE_SIZE = 16
_cache: dict[tuple, dict] = {}
_cache_lock = threading.Lock()

# --- Vector RAG Indexer (ChromaDB) ---
_chroma_client = chromadb.Client()
_last_indexed_stamp = 0.0
_index_lock = threading.Lock()


def _data_stamp() -> float:
    latest = 0.0
    for folder in DATA_FILES:
        if folder.exists():
            for file in folder.glob("*.json"):
                latest = max(latest, file.stat().st_mtime)
    return latest


def _get_rag_collection():
    """Index projects and experience into ChromaDB whenever JSON data updates."""
    global _last_indexed_stamp
    stamp = _data_stamp()

    with _index_lock:
        collection = _chroma_client.get_or_create_collection(name="candidate_evidence")
        if stamp <= _last_indexed_stamp and collection.count() > 0:
            return collection

        if collection.count() > 0:
            existing = collection.get()["ids"]
            if existing:
                collection.delete(ids=existing)

        docs, metadatas, ids = [], [], []

        projects_path = ROOT_DIR / "data" / "projects" / "projects.json"
        if projects_path.exists():
            projects = json.loads(projects_path.read_text(encoding="utf-8"))
            for idx, proj in enumerate(projects):
                title = proj.get("title", f"Project-{idx}")
                techs = ", ".join(proj.get("technologies", []))
                for h_idx, highlight in enumerate(proj.get("highlights", [])):
                    docs.append(f"{title} ({techs}): {highlight}")
                    metadatas.append({"source": "project", "title": title})
                    ids.append(f"proj_{idx}_{h_idx}")
                if proj.get("architecture"):
                    docs.append(f"{title} Architecture ({techs}): {proj['architecture']}")
                    metadatas.append({"source": "project", "title": title})
                    ids.append(f"proj_{idx}_arch")

        exp_path = ROOT_DIR / "data" / "personal" / "experience.json"
        if exp_path.exists():
            experiences = json.loads(exp_path.read_text(encoding="utf-8"))
            if isinstance(experiences, list):
                for idx, exp in enumerate(experiences):
                    role = exp.get("role") or exp.get("title", f"Role-{idx}")
                    for b_idx, bullet in enumerate(exp.get("highlights", []) or exp.get("bullets", [])):
                        docs.append(f"{role}: {bullet}")
                        metadatas.append({"source": "experience", "title": role})
                        ids.append(f"exp_{idx}_{b_idx}")

        if docs:
            collection.add(documents=docs, metadatas=metadatas, ids=ids)
        _last_indexed_stamp = stamp
        return collection


def retrieve_evidence(job_description: str, top_k: int = 8) -> dict[str, list[str]]:
    """Semantic vector retrieval mapping project titles -> top relevant evidence chunks."""
    collection = _get_rag_collection()
    if collection.count() == 0:
        return {}

    results = collection.query(
        query_texts=[job_description],
        n_results=min(top_k, collection.count()),
    )
    evidence_map: dict[str, list[str]] = {}
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        if meta.get("source") == "project":
            evidence_map.setdefault(meta["title"], []).append(doc)
    return evidence_map


# --- LangGraph Agent State & Nodes ---
class ResumeGraphState(TypedDict):
    job_description: str
    analysis: dict[str, Any]
    evidence_map: dict[str, list[str]]
    skill_match: dict[str, Any]
    project_ranking: dict[str, Any]
    summary: str
    projects: list[dict[str, Any]]
    ats_score: dict[str, Any]
    revision_count: int
    telemetry: dict[str, float]


def _node_analyze_jd(state: ResumeGraphState) -> dict:
    t0 = time.perf_counter()
    with timed("analysis"):
        analysis = analyze_job_description(state["job_description"])
    return {
        "analysis": analysis,
        "telemetry": {**state.get("telemetry", {}), "analysis_ms": round((time.perf_counter() - t0) * 1000, 1)},
    }


def _node_rag_retrieve(state: ResumeGraphState) -> dict:
    t0 = time.perf_counter()
    evidence_map = retrieve_evidence(state["job_description"], top_k=10)
    return {
        "evidence_map": evidence_map,
        "telemetry": {**state.get("telemetry", {}), "rag_retrieval_ms": round((time.perf_counter() - t0) * 1000, 1)},
    }


def _node_rank_and_match(state: ResumeGraphState) -> dict:
    t0 = time.perf_counter()
    with timed("ranking_and_matching"):
        project_ranking = rank_projects(state["job_description"])
        skill_match = match_skills(state["analysis"])
    return {
        "project_ranking": project_ranking,
        "skill_match": skill_match,
        "telemetry": {**state.get("telemetry", {}), "rank_match_ms": round((time.perf_counter() - t0) * 1000, 1)},
    }


def _node_generate_content(state: ResumeGraphState) -> dict:
    t0 = time.perf_counter()
    top_projects = state["project_ranking"]["top_projects"]
    with timed("rewrite_and_summary"):
        projects = rewrite_projects(
            state["job_description"],
            top_projects,
            state["analysis"],
            state["evidence_map"],
        )
        summary = generate_summary(state["job_description"], top_projects)
    return {
        "projects": projects,
        "summary": summary,
        "revision_count": state.get("revision_count", 0) + 1,
        "telemetry": {**state.get("telemetry", {}), "generation_ms": round((time.perf_counter() - t0) * 1000, 1)},
    }


def _node_evaluate_ats(state: ResumeGraphState) -> dict:
    score_data = calculate_ats_score(state["skill_match"], state["project_ranking"])
    return {"ats_score": score_data}


def _should_refine(state: ResumeGraphState) -> str:
    """Self-reflection edge: retry content generation once if ATS score < 75 and bullets are thin."""
    score = state.get("ats_score", {}).get("ats_score", 0)
    if score < 75 and state.get("revision_count", 0) < 2:
        return "refine"
    return "done"


def _build_optimizer_graph():
    builder = StateGraph(ResumeGraphState)
    builder.add_node("analyze_jd", _node_analyze_jd)
    builder.add_node("rag_retrieve", _node_rag_retrieve)
    builder.add_node("rank_and_match", _node_rank_and_match)
    builder.add_node("generate_content", _node_generate_content)
    builder.add_node("evaluate_ats", _node_evaluate_ats)

    builder.add_edge(START, "analyze_jd")
    builder.add_edge("analyze_jd", "rag_retrieve")
    builder.add_edge("rag_retrieve", "rank_and_match")
    builder.add_edge("rank_and_match", "generate_content")
    builder.add_edge("generate_content", "evaluate_ats")
    builder.add_conditional_edges(
        "evaluate_ats",
        _should_refine,
        {"refine": "generate_content", "done": END},
    )
    return builder.compile()


_OPTIMIZER_GRAPH = _build_optimizer_graph()


def optimize_resume(job_description: str) -> dict:
    key = (
        hashlib.sha256(job_description.strip().encode("utf-8")).hexdigest(),
        _data_stamp(),
        active_provider(),
    )
    with _cache_lock:
        if key in _cache:
            return copy.deepcopy(_cache[key])

    final_state = _OPTIMIZER_GRAPH.invoke(
        {
            "job_description": job_description,
            "revision_count": 0,
            "telemetry": {},
        }
    )

    result = {
        "analysis": final_state["analysis"],
        "skill_match": final_state["skill_match"],
        "project_ranking": final_state["project_ranking"],
        "summary": final_state["summary"],
        "projects": final_state["projects"],
        "ats_score": final_state["ats_score"],
        "telemetry": final_state["telemetry"],
    }

    with _cache_lock:
        if len(_cache) >= CACHE_SIZE:
            _cache.pop(next(iter(_cache)))
        _cache[key] = copy.deepcopy(result)

    return result
"""
core/task_planner.py
Domain-agnostic task planner: decompose user tasks, assign skills, resolve conflicts.

Each domain provides its own planner prompts via domains/<name>/planner_prompts.py
or via domain.yaml. This module provides the generic orchestration framework.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
from pathlib import Path

from core.llm import call_llm

log = logging.getLogger("task_planner")


def _extract_json(raw: str) -> str:
    """Extract JSON from potential markdown fences."""
    if "```json" in raw:
        raw = raw.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in raw:
        raw = raw.split("```", 1)[1].split("```", 1)[0]
    return raw.strip()


# ---------------------------------------------------------------------------
# Generic task planning
# ---------------------------------------------------------------------------

def plan_task(
    task: str,
    domain_config: dict,
    *,
    library_dir: Path,
    n_steps: int = 8,
    backend: str = "gemini",
) -> dict:
    """Plan a task: decompose into steps and assign skills.

    Args:
        task: User task description.
        domain_config: Loaded domain configuration.
        n_steps: Suggested number of steps.
        library_dir: Path to skill library.
        backend: LLM backend to use.

    Returns:
        Task plan dict with steps and assigned skills.
    """
    domain_name = domain_config["name"]
    persona = domain_config.get("persona", "You are a helpful expert.")

    # Try to load domain-specific planner prompts.
    planner_prompts = _load_planner_prompts(domain_config)

    # Step 1: Decompose task into steps.
    decompose_system = planner_prompts.get("decompose_system", f"""\
{persona} Given a task description, decompose it into {n_steps} ordered steps.

Output strict JSON:
```json
{{
  "steps": [
    {{"index": 0, "action": "short action description", "details": "what needs to happen"}}
  ]
}}
```""")

    decompose_prompt = f"Task: {task}\nNumber of steps: {n_steps}\n\nDecompose into steps:"
    raw = call_llm(decompose_prompt, decompose_system, backend=backend)

    try:
        steps = json.loads(_extract_json(raw))
    except json.JSONDecodeError:
        log.error(f"Failed to parse task decomposition: {raw[:200]}")
        steps = _fallback_steps(task, n_steps)

    # Step 2: For each step, retrieve relevant skills.
    from core.skill_retriever import SkillRetriever
    try:
        rerank_prompt = domain_config.get("rerank_prompt", None)
        retriever = SkillRetriever(library_dir, rerank_prompt=rerank_prompt)
        for step in steps.get("steps", []):
            try:
                candidates = retriever.retrieve(step["action"], top_k=5)
                step["suggested_skills"] = [
                    {"skill_id": c["skill_id"], "skill_name": c.get("skill_name", "")}
                    for c in candidates[:3]
                ]
            except Exception as e:
                log.warning(f"Retrieval failed for step {step.get('index', '?')}: {e}")
                step["suggested_skills"] = []
    except Exception as e:
        log.warning(f"Could not initialize retriever: {e}")

    return {
        "task": task,
        "domain": domain_name,
        "total_steps": len(steps.get("steps", [])),
        "steps": steps.get("steps", []),
    }


def _fallback_steps(task: str, n_steps: int) -> dict:
    """Generate basic steps without LLM."""
    return {
        "steps": [
            {"index": i, "action": f"Step {i+1}", "details": f"Part {i+1} of: {task}"}
            for i in range(n_steps)
        ]
    }


def _load_planner_prompts(domain_config: dict) -> dict:
    """Try to load domain-specific planner prompts."""
    domain_dir = domain_config.get("_domain_dir")
    if not domain_dir:
        return {}

    prompts_path = Path(domain_dir) / "planner_prompts.py"
    if not prompts_path.exists():
        return {}

    # Load as a module.
    import importlib.util
    spec = importlib.util.spec_from_file_location("planner_prompts", prompts_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = {}
    for attr in ["decompose_system", "assign_system", "fallback_steps"]:
        if hasattr(mod, attr):
            result[attr] = getattr(mod, attr)
    return result

"""
domains/blender/agent_hooks.py
Blender domain agent hooks — auto-verification + progress tracking.

auto_verify: called after every tool call, can make live MCP calls.
  - After execute_blender_code / add_object_from_skill: get scene info and
    viewport screenshot, send to GPT-5.4 vision for QA.
progress_check: called every 10 iterations, reports scene state.
"""
import logging
import json
import re

log = logging.getLogger("blender_hooks")

_added_objects: list[str] = []
_viewport_issue_count = 0

_VISUAL_QA_PROMPT = """\
You are a Blender 3D scene reviewer. Check this viewport screenshot for SERIOUS issues only.

Expected action: {action}
Expected object: {object_name}

Only flag SERIOUS problems — minor shading differences are OK. Check:
1. MISSING OBJECT: Is the expected object visibly absent from the viewport? (SERIOUS)
2. BROKEN GEOMETRY: Are there obvious mesh artifacts, inverted normals (black faces), or degenerate geometry? (SERIOUS)
3. EMPTY SCENE: Is the viewport showing essentially nothing (just grid)? (SERIOUS)
4. MATERIAL ERROR: Is the object entirely pink/magenta (missing texture) or pure black (no lighting)? (SERIOUS)
5. SCALE ISSUE: Is the object absurdly large (fills entire viewport) or invisibly small? (SERIOUS)

Reply "PASS" if no serious problems.
Reply "ISSUE: [problem]" ONLY for serious visual failures.
Do NOT flag minor aesthetic preferences, camera angle choices, or subtle color differences.
"""

_PROGRESS_PROMPT = """\
Scene state summary:
{scene_info}

Objects added so far: {object_list}
Iteration: {iteration} of budget

Assess: Is the scene progressing well? Any objects that look misplaced or missing?
Provide a 1-2 sentence status report.
"""

_VIEWPORT_READY_PROMPT = """\
You are reviewing a Blender viewport preview before final render.

Flag only artifact-score blockers that should be fixed before rendering:
1. Large empty foreground or no clear focal hero object.
2. Scene reads as primitive blockout/default cubes/flat planes.
3. Requested environment details are missing or barely visible (pipes, signage, props, atmosphere, repeated motifs, layered foreground/midground/background).
4. Materials look mostly default/flat, with little roughness/metal/glass/wet/emissive variation.
5. Camera framing hides important details, is too dark, or crops awkwardly.

Reply exactly "PASS" if it is render-ready.
Otherwise reply "ISSUE: " followed by 2-4 concrete fixes the agent can implement with execute_blender_code/material/lighting tools before rendering.
"""


def _call_vision_llm(b64_png: str, action: str, object_name: str) -> str:
    """Call GPT-5.4 vision to evaluate a viewport screenshot."""
    try:
        from core.llm import call_azure_openai
    except ImportError:
        return ""

    prompt = _VISUAL_QA_PROMPT.format(
        action=action[:80], object_name=object_name[:60]
    )
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_png}",
                    },
                },
            ],
        }
    ]

    try:
        resp = call_azure_openai(
            messages, model="gpt-5.4", reasoning_effort="low"
        )
        return resp.get("content", "")
    except Exception as e:
        log.warning("Vision QA failed: %s", e)
        return ""


def _call_viewport_ready_llm(b64_png: str) -> str:
    """Vision QA for final-render readiness after get_viewport_screenshot."""
    try:
        from core.llm import call_azure_openai
    except ImportError:
        return ""

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": _VIEWPORT_READY_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_png}",
                    },
                },
            ],
        }
    ]
    try:
        resp = call_azure_openai(
            messages, model="gpt-5.4", reasoning_effort="low"
        )
        return resp.get("content", "")
    except Exception as e:
        log.warning("Viewport readiness QA failed: %s", e)
        return ""


def _preview_path_from_result(result_text: str) -> str:
    preview_path = ""
    try:
        payload = json.loads(result_text)
        if isinstance(payload, dict):
            preview_path = str(
                payload.get("_image_attachment")
                or payload.get("path")
                or ""
            )
    except Exception:
        pass
    if not preview_path:
        path_match = re.search(r"saved to (.+\.png)", result_text or "")
        if path_match:
            preview_path = path_match.group(1).strip()
    return preview_path


async def auto_verify(tool_name, tool_args, result_text, mcp):
    """Auto-verify after object-creation operations with scene info + visual QA."""

    if tool_name == "get_viewport_screenshot":
        global _viewport_issue_count
        try:
            import os
            import base64
            preview_path = _preview_path_from_result(result_text or "")
            if not preview_path or not os.path.exists(preview_path):
                return None
            with open(preview_path, "rb") as f:
                b64_png = base64.b64encode(f.read()).decode("ascii")
            qa_result = _call_viewport_ready_llm(b64_png)
            if not qa_result:
                return None
            if "pass" in qa_result.lower()[:15]:
                log.info("Viewport readiness QA PASS")
                return None
            if _viewport_issue_count >= 1:
                return (
                    "Viewport readiness QA still sees polish issues, but one "
                    "focused fix pass has already been requested. Do one "
                    "final `apply_scene_polish_pack(scene_type=\"auto\")`, then "
                    "render instead of looping on screenshots."
                )
            _viewport_issue_count += 1
            return (
                f"Viewport readiness QA: {qa_result}\n"
                "Do not render yet. Make one focused polish pass with "
                "execute_blender_code/material/lighting tools, then take "
                "another get_viewport_screenshot."
            )
        except Exception as e:
            log.warning("Viewport readiness QA error: %s", e)
            return None

    # Only trigger on object-creation tools
    if tool_name not in (
        "execute_blender_code",
        "add_object_from_skill",
    ):
        return None

    # Check for errors in the result
    if re.search(r"(?i)error|traceback|exception", result_text):
        return (
            f"The last {tool_name} call failed with an error. "
            "Review the traceback and try a different approach."
        )

    # Track added objects
    obj_name = tool_args.get("object_name", "")
    if tool_name == "add_object_from_skill":
        skill_id = tool_args.get("skill_id", "")
        obj_name = obj_name or skill_id
        if obj_name:
            _added_objects.append(obj_name)

    # --- Scene info verification ---
    try:
        scene_info = await mcp.call_tool("get_scene_info", {})
    except Exception as exc:
        log.warning("get_scene_info failed: %s", exc)
        scene_info = ""

    # Parse object count from scene info
    obj_count_match = re.search(r"Objects:\s*(\d+)", scene_info or "")
    if obj_count_match:
        obj_count = int(obj_count_match.group(1))
        if obj_count == 0:
            return (
                "Warning: scene has 0 objects after the last operation. "
                "Something went wrong — the object was not created."
            )

    # For add_object_from_skill, verify the named object exists
    if tool_name == "add_object_from_skill" and obj_name:
        if scene_info and obj_name not in scene_info:
            # Blender may have auto-suffixed the name; only warn, don't block
            log.info(
                "Object '%s' not found verbatim in scene info (may be suffixed)",
                obj_name,
            )

    # --- Visual QA via viewport screenshot ---
    try:
        screenshot_result = await mcp.call_tool(
            "get_viewport_screenshot", {}
        )
        if not screenshot_result or "Error" in (screenshot_result or ""):
            return None

        # The unified server saves preview to a file; read it for vision QA
        import os
        import base64
        preview_path = _preview_path_from_result(screenshot_result)
        if not preview_path:
            return None
        if not os.path.exists(preview_path):
            return None

        with open(preview_path, "rb") as f:
            b64_png = base64.b64encode(f.read()).decode("ascii")

        # Build action description
        if tool_name == "add_object_from_skill":
            action = f"Added object from skill '{tool_args.get('skill_id', '?')}'"
        else:
            code_snippet = (tool_args.get("code", "") or "")[:120]
            action = f"Executed bpy code: {code_snippet}"

        qa_result = _call_vision_llm(
            b64_png, action, obj_name or "(custom code)"
        )
        if not qa_result:
            return None

        if "pass" in qa_result.lower()[:15]:
            log.info("Visual QA PASS for %s", tool_name)
            return None

        log.warning("Visual QA ISSUE after %s: %s", tool_name, qa_result[:200])
        return (
            f"Visual QA after {tool_name}: {qa_result}\n"
            "Consider fixing the issue with execute_blender_code."
        )
    except Exception as e:
        log.warning("Visual QA error: %s", e)
        return None


async def progress_check(mcp, invocations, iteration):
    """Every 10 iterations, report scene state and progress."""
    if iteration % 10 != 0:
        return None

    # Get current scene state
    try:
        scene_info = await mcp.call_tool("get_scene_info", {})
    except Exception as exc:
        log.warning("progress_check: get_scene_info failed: %s", exc)
        scene_info = "(unable to retrieve scene info)"

    object_list = ", ".join(_added_objects) if _added_objects else "(none tracked)"

    try:
        from core.llm import call_azure_openai
    except ImportError:
        # Fallback: just return raw scene info
        return (
            f"[Progress check @ iteration {iteration}]\n"
            f"Scene: {scene_info}\n"
            f"Objects added: {object_list}"
        )

    prompt = _PROGRESS_PROMPT.format(
        scene_info=scene_info or "(empty)",
        object_list=object_list,
        iteration=iteration,
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        resp = call_azure_openai(
            messages, model="gpt-5.4", reasoning_effort="low"
        )
        summary = resp.get("content", "")
    except Exception as e:
        log.warning("progress_check LLM failed: %s", e)
        summary = ""

    report = (
        f"[Progress check @ iteration {iteration}]\n"
        f"Scene: {scene_info}\n"
        f"Objects added: {object_list}"
    )
    if summary:
        report += f"\nAssessment: {summary}"

    return report

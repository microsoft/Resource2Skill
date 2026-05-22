"""
domains/web/agent_hooks.py
Web (HTML/CSS/JS) domain agent hooks — auto-verification + progress tracking.

auto_verify: called after every tool call, can make live MCP calls.
  - After write_file / add_component_from_skill: renders page screenshot,
    inspects DOM for errors, sends screenshot to GPT-5.4 vision for QA.
progress_check: called every 10 iterations, reports project health.
"""
from __future__ import annotations

import logging
import re

log = logging.getLogger("web_hooks")

# Track used skills to encourage diversity
_used_skills: set[str] = set()

# Tools that modify visual output and should trigger verification
_VERIFY_TRIGGERS = {"write_file", "add_component_from_skill"}

# ---------------------------------------------------------------------------
# Visual QA prompt for GPT-5.4 vision
# ---------------------------------------------------------------------------

_VISUAL_QA_PROMPT = """\
You are a web frontend design reviewer. Examine this browser screenshot of a \
web page and check for SERIOUS issues only.

Context: {context}

Only flag SERIOUS problems — minor stylistic preferences are OK. Check:
1. LAYOUT BROKEN: Overlapping elements, content overflowing containers, \
or major alignment issues? (SERIOUS)
2. BLANK PAGE: Is the page mostly empty/white when it should have content? (SERIOUS)
3. UNREADABLE TEXT: Is any text invisible, too small, or illegible due to \
poor color contrast? (SERIOUS)
4. MISSING COMPONENTS: Are expected sections (hero, nav, cards, etc.) \
visually absent? (SERIOUS)
5. SPACING: Are there abnormally large gaps or elements crammed together \
with no breathing room? (SERIOUS)
6. COLORS: Do the colors clash badly or fail to form a cohesive palette? (MODERATE)

Reply "PASS" if no serious problems.
Reply "ISSUE: [problem]" ONLY for serious layout/rendering failures.
Do NOT flag minor content differences, placeholder text, or stylistic preferences.\
"""


def _call_vision_llm(b64_png: str, context: str) -> str:
    """Call GPT-5.4 vision to evaluate a rendered page screenshot."""
    try:
        from core.llm import call_azure_openai
    except ImportError:
        return ""

    prompt = _VISUAL_QA_PROMPT.format(context=context[:200])
    messages = [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_png}"}},
    ]}]

    try:
        resp = call_azure_openai(
            messages,
            model="gpt-5.4",
            reasoning_effort="low",
            max_completion_tokens=300,
            timeout=30,
            max_retries=2,
        )
        return (resp.get("content") or "").strip()
    except Exception as e:
        log.warning("Vision QA failed: %s", e)
        return ""


# ---------------------------------------------------------------------------
# auto_verify
# ---------------------------------------------------------------------------

async def auto_verify(
    fn_name: str,
    fn_args: dict,
    result_text: str,
    mcp_wrapper,
) -> str | None:
    """Auto-verify after file writes and component additions with visual QA.

    Called by core/agent_executor.py AFTER each tool call completes.
    Returns a feedback message for the LLM if issues found, or None.
    """
    # Only trigger on tools that modify visual output
    if fn_name not in _VERIFY_TRIGGERS:
        return None

    # Check for obvious errors in the tool result
    if result_text and re.search(r"(?i)^error", result_text.strip()):
        return (
            f"The last {fn_name} call failed: {result_text[:200]}. "
            f"Check the arguments and try a different approach."
        )

    # Skill diversity check for add_component_from_skill
    if fn_name == "add_component_from_skill":
        skill_id = fn_args.get("skill_id", "")
        if skill_id and skill_id in _used_skills:
            return (
                f"Note: skill '{skill_id}' was already used. "
                f"Pick a different skill for visual variety."
            )
        if skill_id:
            _used_skills.add(skill_id)

    # Build context string for the QA prompt
    if fn_name == "add_component_from_skill":
        skill_name = fn_args.get("skill_id", "unknown")
        context = f"Added component from skill '{skill_name}'"
    else:
        filename = fn_args.get("filename", fn_args.get("path", "unknown"))
        context = f"Wrote file '{filename}'"

    # Step 1: Inspect DOM for console errors and structural issues
    project_id = fn_args.get("project_id", "")
    dom_feedback = None
    try:
        dom_args = {"project_id": project_id} if project_id else {}
        dom_result = await mcp_wrapper.call_tool("inspect_dom", dom_args)
        if dom_result:
            # Check for console errors reported by the DOM inspector
            error_match = re.search(r"(\d+)\s+console\s+error", dom_result, re.IGNORECASE)
            if error_match:
                error_count = int(error_match.group(1))
                if error_count > 0:
                    dom_feedback = (
                        f"DOM inspection found {error_count} console error(s). "
                        f"Details: {dom_result[:300]}"
                    )

            # Check for zero elements (broken page)
            elem_match = re.search(r"(\d+)\s+elements?", dom_result, re.IGNORECASE)
            if elem_match:
                elem_count = int(elem_match.group(1))
                if elem_count < 2:
                    return (
                        f"Warning: DOM has only {elem_count} element(s) — the page "
                        f"appears nearly empty. Check your HTML structure."
                    )
    except Exception as e:
        log.debug("DOM inspection failed: %s", e)

    # Step 2: Render page to screenshot for visual QA
    try:
        render_args = {"project_id": project_id} if project_id else {}
        render_result = await mcp_wrapper.call_tool("render_page", render_args)
        if not render_result or re.search(r"(?i)^error", render_result.strip()):
            # Render failed — return DOM feedback if we have it, else None
            if dom_feedback:
                return dom_feedback
            return None

        # Extract base64 PNG from render result
        b64_match = re.search(r"base64,([A-Za-z0-9+/=]+)", render_result)
        if not b64_match:
            if dom_feedback:
                return dom_feedback
            return None

        b64_png = b64_match.group(1)

        # Send to GPT-5.4 vision for QA
        qa_result = _call_vision_llm(b64_png, context)
        if not qa_result:
            if dom_feedback:
                return dom_feedback
            return None

        if qa_result.upper().startswith("PASS"):
            log.info("Visual QA PASS after %s", fn_name)
            # Even on visual PASS, surface DOM errors if present
            if dom_feedback:
                return dom_feedback
            return None

        # Visual QA found issues
        log.warning("Visual QA ISSUE after %s: %s", fn_name, qa_result[:200])
        feedback = f"Visual QA: {qa_result}"
        if dom_feedback:
            feedback = f"{dom_feedback}\n{feedback}"
        feedback += "\nFix the issues before moving to the next section."
        return feedback

    except Exception as e:
        log.warning("Render/visual QA error: %s", e)
        if dom_feedback:
            return dom_feedback
        return None


# ---------------------------------------------------------------------------
# progress_check
# ---------------------------------------------------------------------------

async def progress_check(
    mcp_wrapper,
    invocations: list,
    iteration: int,
) -> str | None:
    """Report project progress every 10 iterations.

    Inspects the current project state: file count, component count,
    DOM health, and recent error rate.
    """
    report_parts = [f"PROGRESS CHECK (iteration {iteration}):"]

    # Inspect DOM for current page state
    # Try to find the active project_id from recent invocations
    active_project_id = ""
    for inv in reversed(invocations):
        if isinstance(inv, dict):
            args = inv.get("args") or inv.get("arguments") or {}
            result = inv.get("result") or ""
        else:
            args = getattr(inv, "arguments", {}) or {}
            result = getattr(inv, "result", "") or ""
        pid = args.get("project_id", "") if isinstance(args, dict) else ""
        if not pid:
            m = re.search(r"\bid:\s*(proj_[A-Za-z0-9_]+)\b", str(result))
            if m:
                pid = m.group(1)
        if pid:
            active_project_id = pid
            break

    if not active_project_id:
        report_parts.append("No active project_id yet; continue with create_project or schema/init.")
        return "\n".join(report_parts)

    try:
        dom_args = {"project_id": active_project_id} if active_project_id else {}
        dom_result = await mcp_wrapper.call_tool("inspect_dom", dom_args)
        if dom_result:
            report_parts.append(f"DOM state: {dom_result[:400]}")

            # Parse element and error counts
            elem_match = re.search(r"(\d+)\s+elements?", dom_result, re.IGNORECASE)
            error_match = re.search(r"(\d+)\s+console\s+error", dom_result, re.IGNORECASE)
            if elem_match:
                report_parts.append(f"Total DOM elements: {elem_match.group(1)}")
            if error_match and int(error_match.group(1)) > 0:
                report_parts.append(
                    f"WARNING: {error_match.group(1)} console error(s) detected"
                )
        else:
            report_parts.append("DOM inspection returned empty (project may not be created yet)")
    except Exception as e:
        report_parts.append(f"DOM inspection unavailable: {e}")

    # Check project files by reading index.html
    try:
        read_args = {"filename": "index.html"}
        if active_project_id:
            read_args["project_id"] = active_project_id
        index_result = await mcp_wrapper.call_tool("read_file", read_args)
        if index_result and not re.search(r"(?i)^error", index_result.strip()):
            # Count sections/components in the HTML
            section_count = len(re.findall(r"<section", index_result, re.IGNORECASE))
            div_count = len(re.findall(r"<div", index_result, re.IGNORECASE))
            lines = index_result.count("\n") + 1
            report_parts.append(
                f"index.html: {lines} lines, {section_count} <section> tags, "
                f"{div_count} <div> tags"
            )
        else:
            report_parts.append("index.html: not found or unreadable")
    except Exception:
        report_parts.append("index.html: could not read")

    # Count skills used so far
    report_parts.append(f"Unique skills used: {len(_used_skills)}")
    if _used_skills:
        report_parts.append(f"Skills: {', '.join(sorted(_used_skills))}")

    # Count recent failures from invocations
    recent = invocations[-10:] if invocations else []
    fail_count = 0
    for inv in recent:
        res = getattr(inv, "result", None) or ""
        if isinstance(res, str) and re.search(r"(?i)^error", res.strip()):
            fail_count += 1
    report_parts.append(f"Recent failures (last 10 calls): {fail_count}")

    if fail_count >= 5:
        report_parts.append(
            "HIGH FAILURE RATE: Consider simplifying your approach or "
            "checking tool arguments carefully."
        )

    return "\n".join(report_parts)

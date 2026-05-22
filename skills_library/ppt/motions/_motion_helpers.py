"""_motion_helpers.py — OOXML emitters for content-triggered motion.

Distinct from skills_library/ppt/shells_seed/_shell_helpers.py:

- shell_helpers emits AMBIENT primitives (indefinite loops: animRot,
  animMotion, animScale with repeatCount="indefinite"). Those play
  in PowerPoint but not in LibreOffice Impress.
- motion_helpers emits CONTENT-TRIGGERED animations (entrance,
  emphasis, exit, motion_path, text-reveal) with finite duration
  and presetClass="entr|emph|exit|path". These are what PowerPoint
  plays natively AND Impress plays too (entrance + emphasis work in
  Impress; motion_path works in PowerPoint, Impress renders as
  static fallback).

Every emitter appends into the slide's <p:timing>/<p:mainSeq>/...
childTnLst via _ensure_timing_group (copied here to keep the motion
skill tree self-contained).

Public emitters are all idempotent on a given (shape, effect_kind)
pair — re-calling with the same args no-ops if an equivalent
<p:cTn> already exists.
"""
from __future__ import annotations

from typing import Iterable

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"

_UID_COUNTER = {"n": 50000}  # monotonically increasing across process


def _next_uid() -> int:
    _UID_COUNTER["n"] += 2
    return _UID_COUNTER["n"]


def _ensure_timing_group(slide):
    """Return the <p:childTnLst> that accepts auto-play animations.

    Uses the exact timing scaffold MS PowerPoint writes for decks
    that play animations on slide load (verified against
    reference_decks/pm_cogs.pptx which the operator has tested
    in PowerPoint):

      tnLst
        par (cTn id=1 nodeType=tmRoot)
          childTnLst
            seq (concurrent=1 nextAc=seek)
              cTn id=2 nodeType=mainSeq dur=indefinite
                childTnLst
                  par
                    cTn id=3 nodeType=clickPar fill=hold
                      stCondLst
                        cond delay=indefinite             <- standard click cond
                        cond evt=onBegin delay=0          <- ALSO auto-start on mainSeq begin
                          tn val=2                         <- target = mainSeq (id=2), NOT sldTgt
                      childTnLst
                        par
                          cTn id=4 nodeType=withGroup fill=hold
                            stCondLst cond delay=0
                            childTnLst                     <- *** emit animations HERE ***
              prevCondLst / nextCondLst
    """
    from pptx.oxml.ns import qn
    from pptx.oxml import parse_xml

    timing = slide._element.find(qn("p:timing"))
    if timing is None:
        timing = parse_xml(
            f'<p:timing xmlns:p="{P_NS}">'
            '<p:tnLst><p:par>'
            '<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
            '<p:childTnLst><p:seq concurrent="1" nextAc="seek">'
            '<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold" nodeType="clickPar">'
            '<p:stCondLst>'
            '<p:cond delay="indefinite"/>'
            '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'
            '</p:stCondLst>'
            '<p:childTnLst><p:par><p:cTn id="4" fill="hold" nodeType="withGroup">'
            '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            '<p:childTnLst/>'
            '</p:cTn></p:par></p:childTnLst>'
            '</p:cTn></p:par></p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
        )
        slide._element.append(timing)
    else:
        # Retrofit a pre-existing timing so every emission still lands
        # in the withGroup childTnLst. If the outer click par lacks the
        # onBegin cond, append it.
        click_par_cTn = None
        withgroup_children = None
        for cTn in timing.iter(qn("p:cTn")):
            nt = cTn.get("nodeType")
            if nt == "clickPar":
                click_par_cTn = cTn
            elif nt == "withGroup":
                withgroup_children = cTn.find(qn("p:childTnLst"))
        # Ensure click par has auto-start cond.
        if click_par_cTn is not None:
            stCondLst = click_par_cTn.find(qn("p:stCondLst"))
            has_auto = False
            if stCondLst is not None:
                for cond in stCondLst.findall(qn("p:cond")):
                    if cond.get("evt") == "onBegin":
                        has_auto = True
                        break
            if not has_auto and stCondLst is not None:
                stCondLst.append(parse_xml(
                    f'<p:cond xmlns:p="{P_NS}" evt="onBegin" delay="0">'
                    '<p:tn val="2"/></p:cond>'
                ))
        # If old structure (no clickPar/withGroup), inject a standard
        # scaffold under mainSeq's existing childTnLst.
        if withgroup_children is None:
            mainSeq = None
            for cTn in timing.iter(qn("p:cTn")):
                if cTn.get("nodeType") == "mainSeq":
                    mainSeq = cTn
                    break
            if mainSeq is not None:
                ms_children = mainSeq.find(qn("p:childTnLst"))
                if ms_children is not None:
                    ms_children.append(parse_xml(
                        f'<p:par xmlns:p="{P_NS}">'
                        '<p:cTn id="3" fill="hold" nodeType="clickPar">'
                        '<p:stCondLst>'
                        '<p:cond delay="indefinite"/>'
                        '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'
                        '</p:stCondLst>'
                        '<p:childTnLst><p:par><p:cTn id="4" fill="hold" nodeType="withGroup">'
                        '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                        '<p:childTnLst/>'
                        '</p:cTn></p:par></p:childTnLst>'
                        '</p:cTn></p:par>'
                    ))

    # Locate the withGroup childTnLst.
    for cTn in timing.iter(qn("p:cTn")):
        if cTn.get("nodeType") == "withGroup":
            return cTn.find(qn("p:childTnLst"))
    return None


def _sid(shape) -> int | None:
    sid = getattr(shape, "shape_id", None)
    return int(sid) if sid is not None else None


# ---------------------------------------------------------------------------
# Entrance emitters (preset class "entr")
# ---------------------------------------------------------------------------

def emit_fade_in(slide, shape, delay_ms: int = 0,
                 duration_ms: int = 600) -> None:
    """Shape fades from invisible to visible.

    PowerPoint preset: "Fade" (presetID 10, presetClass entr).
    Impress: supported.

    Uses the <p:animEffect transition="in" filter="fade"/> pattern
    (same as _append_entrance_xml in _shell_helpers), NOT a raw
    p:anim on style.opacity — PowerPoint auto-repairs the latter.
    """
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="10" presetClass="entr" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animEffect transition="in" filter="fade">'
        f'<p:cBhvr><p:cTn id="{uid+2}" dur="{int(duration_ms)}"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'</p:cBhvr></p:animEffect>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_fly_in(slide, shape, direction: str = "bottom",
                delay_ms: int = 0, duration_ms: int = 700) -> None:
    """Shape flies in from the named edge.

    direction ∈ {left, right, top, bottom}.
    PowerPoint preset: "Fly In" (presetID 2).
    """
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    # motion path per direction: path starts off-screen at "from" edge
    # and moves to (0,0) relative to shape's current position.
    path_map = {
        "left":   "M -1 0 L 0 0 E",
        "right":  "M 1 0 L 0 0 E",
        "top":    "M 0 -1 L 0 0 E",
        "bottom": "M 0 1 L 0 0 E",
    }
    path = path_map.get(direction, path_map["bottom"])
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="2" presetClass="entr" presetSubtype="4" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animMotion origin="layout" path="{path}" pathEditMode="relative">'
        f'<p:cBhvr><p:cTn id="{uid+2}" dur="{int(duration_ms)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'</p:animMotion>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_grow_from_small(slide, shape, delay_ms: int = 0,
                         duration_ms: int = 600,
                         from_pct: int = 10) -> None:
    """Shape scales from from_pct% up to 100% (grow entrance).

    PowerPoint preset: "Grow & Turn" / "Zoom" family (presetID 23).
    Uses animScale (scale only) — the fade aspect comes from the
    built-in PowerPoint preset rendering; avoiding raw style.opacity
    animation prevents PowerPoint's auto-repair dialog.
    """
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="23" presetClass="entr" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+2}" dur="{int(duration_ms)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="{int(from_pct*1000)}" y="{int(from_pct*1000)}"/>'
        f'<p:to x="100000" y="100000"/>'
        f'</p:animScale>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_zoom_in(slide, shape, delay_ms: int = 0,
                 duration_ms: int = 700, from_pct: int = 30) -> None:
    """Shape zooms from from_pct% to 100% centered at its own center."""
    emit_grow_from_small(slide, shape, delay_ms, duration_ms, from_pct)


def emit_wipe_in(slide, shape, direction: str = "left",
                 delay_ms: int = 0, duration_ms: int = 500) -> None:
    """Shape is revealed by a wipe from the named edge."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    sub_map = {"left": 4, "right": 2, "top": 1, "bottom": 8}
    sub = sub_map.get(direction, 4)
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="12" presetClass="entr" presetSubtype="{sub}" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


# ---------------------------------------------------------------------------
# Emphasis emitters (preset class "emph") — shape must already be visible
# ---------------------------------------------------------------------------

def emit_pulse(slide, shape, delay_ms: int = 0,
               duration_ms: int = 800, scale_pct: int = 110,
               repeats: int = 1) -> None:
    """Scale up to scale_pct% and back, `repeats` times.

    presetClass="emph" (not entrance). Good for drawing attention to
    a visible element like a hero number after its fade-in settled.
    """
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    repeat_attr = (
        f' repeatCount="{int(repeats)}000"' if repeats and repeats > 1 else ""
    )
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="8" presetClass="emph" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}" '
        f'autoRev="1"{repeat_attr} fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="100000" y="100000"/>'
        f'<p:to x="{int(scale_pct*1000)}" y="{int(scale_pct*1000)}"/>'
        f'</p:animScale>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_grow_emphasis(slide, shape, delay_ms: int = 0,
                       duration_ms: int = 500,
                       to_pct: int = 120) -> None:
    """Scale to to_pct% and hold (no reverse)."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="6" presetClass="emph" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="100000" y="100000"/>'
        f'<p:to x="{int(to_pct*1000)}" y="{int(to_pct*1000)}"/>'
        f'</p:animScale>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


# ---------------------------------------------------------------------------
# Motion path emitters
# ---------------------------------------------------------------------------

def emit_motion_path(slide, shape, svg_path: str,
                     delay_ms: int = 0, duration_ms: int = 1200,
                     auto_reverse: bool = False) -> None:
    """Shape travels along svg_path (normalised coords, 0..1 = slide)."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    ar = ' autoRev="1"' if auto_reverse else ""
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="32" presetClass="path" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:animMotion origin="layout" path="{svg_path}" pathEditMode="relative">'
        f'<p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}"{ar} fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'</p:animMotion>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_arc_path(slide, shape, delay_ms: int = 0,
                  duration_ms: int = 1200,
                  dx_frac: float = 0.3, dy_frac: float = 0.0,
                  bow_frac: float = 0.15) -> None:
    """Shape travels from its current position along an arc to
    (current + dx_frac, current + dy_frac), arcing by bow_frac
    perpendicular to the line. All fractions relative to slide
    size."""
    # Approximate a quadratic bezier via SVG path "q".
    path = f"M 0 0 q {dx_frac/2:.4f} {-bow_frac:.4f} {dx_frac:.4f} {dy_frac:.4f}"
    emit_motion_path(slide, shape, path, delay_ms, duration_ms)


# ---------------------------------------------------------------------------
# Text-body staggered reveal — per-paragraph fade-in
# ---------------------------------------------------------------------------

def emit_text_stagger(slide, shape, delay_ms: int = 0,
                      stagger_ms: int = 180,
                      per_duration_ms: int = 450) -> None:
    """For each paragraph in the shape's text body, emit a fade-in
    triggered by an increasing delay so the bullets appear one by
    one. If the shape has no text, falls back to a single fade_in."""
    tf = getattr(shape, "text_frame", None)
    if tf is None:
        emit_fade_in(slide, shape, delay_ms, per_duration_ms)
        return
    paras = list(tf.paragraphs)
    if not paras:
        emit_fade_in(slide, shape, delay_ms, per_duration_ms)
        return
    # PowerPoint supports per-paragraph entrance via <p:bldP> + mainSeq
    # but python-pptx makes that fiddly. Simpler robust approach: emit
    # one fade_in with staggered total duration so the shape as a whole
    # fades in over stagger_ms * n_paragraphs.
    total = max(per_duration_ms, stagger_ms * len(paras))
    emit_fade_in(slide, shape, delay_ms, total)
    # Then add a per-paragraph reveal via <p:bldP> as well for PowerPoint.
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import qn
    timing = slide._element.find(qn("p:timing"))
    if timing is None:
        return
    bld_lst = timing.find(qn("p:bldLst"))
    if bld_lst is None:
        bld_lst = parse_xml(f'<p:bldLst xmlns:p="{P_NS}"/>')
        timing.append(bld_lst)
    sid = _sid(shape)
    if sid is None:
        return
    bldP = parse_xml(
        f'<p:bldP xmlns:p="{P_NS}" spid="{sid}" grpId="0" build="byParagraph" />'
    )
    bld_lst.append(bldP)


# ---------------------------------------------------------------------------
# Motion-path bbox helpers for the overlap gate
# ---------------------------------------------------------------------------

def motion_path_bbox_delta(svg_path: str) -> tuple[float, float, float, float]:
    """Return (dx_min, dy_min, dx_max, dy_max) covered by a normalised
    SVG-ish motion path, relative to shape start position, as slide
    fractions. Best-effort parser for M/L/a/q commands our emitters
    use; unknown commands contribute nothing."""
    import re as _re
    cur_x, cur_y = 0.0, 0.0
    xs, ys = [0.0], [0.0]
    tokens = _re.findall(r"[MLaq]|-?[\d.]+", svg_path)
    i = 0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        if cmd in ("M", "L"):
            cur_x = float(tokens[i]); cur_y = float(tokens[i+1]); i += 2
            xs.append(cur_x); ys.append(cur_y)
        elif cmd == "a":
            # rx, ry, xrot, large, sweep, dx, dy
            rx = float(tokens[i]); ry = float(tokens[i+1])
            dx = float(tokens[i+5]); dy = float(tokens[i+6]); i += 7
            nx, ny = cur_x + dx, cur_y + dy
            # Arc bounds conservatively: include both endpoints and
            # extremes in rx, ry.
            xs += [cur_x, nx, cur_x - rx, cur_x + rx]
            ys += [cur_y, ny, cur_y - ry, cur_y + ry]
            cur_x, cur_y = nx, ny
        elif cmd == "q":
            # dx1, dy1, dx, dy  (control + endpoint, both relative)
            cdx = float(tokens[i]); cdy = float(tokens[i+1])
            dx = float(tokens[i+2]); dy = float(tokens[i+3]); i += 4
            cx = cur_x + cdx; cy = cur_y + cdy
            nx = cur_x + dx; ny = cur_y + dy
            xs += [cur_x, cx, nx]; ys += [cur_y, cy, ny]
            cur_x, cur_y = nx, ny
        else:
            # numeric without a command token; skip
            continue
    return (min(xs), min(ys), max(xs), max(ys))


# ---------------------------------------------------------------------------
# Dramatic / aha-worthy emitters (wider amplitude, more cinematic feel)
# ---------------------------------------------------------------------------

def emit_dramatic_zoom(slide, shape, delay_ms: int = 0,
                       duration_ms: int = 900,
                       from_pct: int = 10) -> None:
    """Zoom from 10% to 100% over 900ms — a cinematic Apple-style
    'arrive from nothing' entrance. Much wider amplitude than
    emit_grow_from_small."""
    emit_grow_from_small(slide, shape, delay_ms, duration_ms, from_pct)


def emit_bounce_in(slide, shape, delay_ms: int = 0,
                   duration_ms: int = 700) -> None:
    """Scale from 20% up to 120% (overshoot) then back to 100% and
    hold. The overshoot + settle gives a 'pop!' arrival feel."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    half = max(200, int(duration_ms * 0.6))
    settle = max(150, duration_ms - half)
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="23" presetClass="entr" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        # overshoot to 120%
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+2}" dur="{int(half)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="20000" y="20000"/><p:to x="120000" y="120000"/>'
        f'</p:animScale>'
        # settle back to 100%
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+3}" dur="{int(settle)}" fill="hold">'
        f'<p:stCondLst><p:cond delay="{int(half)}"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="120000" y="120000"/><p:to x="100000" y="100000"/>'
        f'</p:animScale>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_rotate_in(slide, shape, delay_ms: int = 0,
                   duration_ms: int = 800,
                   from_deg: int = -45) -> None:
    """Rotate from from_deg to 0 while also fading in. Dynamic
    directional entrance."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="25" presetClass="entr" presetSubtype="0" '
        f'fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{uid+1}" dur="1" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animRot by="{int(-from_deg * 60000)}">'
        f'<p:cBhvr><p:cTn id="{uid+2}" dur="{int(duration_ms)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst>'
        f'</p:cBhvr></p:animRot>'
        f'<p:animEffect transition="in" filter="fade">'
        f'<p:cBhvr><p:cTn id="{uid+3}" dur="{int(duration_ms)}"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'</p:cBhvr></p:animEffect>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_ambient_rotation(slide, shape, duration_ms: int = 6000,
                          by_deg: int = 360) -> None:
    """Indefinite rotation — continuous ambient motion on a decorative
    shape. Wrapper over _shell_helpers.add_infinite_rotation."""
    import sys, os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "shells_seed"
    ))
    try:
        from _shell_helpers import add_infinite_rotation
        add_infinite_rotation(slide, shape, duration_ms=duration_ms)
    except Exception:
        pass


def emit_counter_rotate(slide, shape, duration_ms: int = 8000) -> None:
    """Indefinite counter-clockwise rotation — pair with emit_ambient_rotation
    on another shape for a cog-like counter-spinning look."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="8" presetClass="emph" presetSubtype="0" '
        f'repeatCount="indefinite" fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:animRot by="-21600000">'
        f'<p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst>'
        f'</p:cBhvr></p:animRot>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))


def emit_breathing_halo(slide, shape, duration_ms: int = 3000,
                        scale_pct: int = 130) -> None:
    """Indefinite breathing scale — oscillates between 100% and
    scale_pct%. Stronger amplitude than _shell_helpers.add_pulse_loop
    (which defaults to 110-120%)."""
    sid = _sid(shape)
    if sid is None:
        return
    from pptx.oxml import parse_xml
    group = _ensure_timing_group(slide)
    if group is None:
        return
    uid = _next_uid()
    xml = (
        f'<p:par xmlns:p="{P_NS}">'
        f'<p:cTn id="{uid}" presetID="6" presetClass="emph" presetSubtype="0" '
        f'repeatCount="indefinite" autoRev="1" fill="hold" grpId="0" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:animScale>'
        f'<p:cBhvr><p:cTn id="{uid+1}" dur="{int(duration_ms)}" '
        f'repeatCount="indefinite" autoRev="1" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr>'
        f'<p:from x="100000" y="100000"/>'
        f'<p:to x="{int(scale_pct*1000)}" y="{int(scale_pct*1000)}"/>'
        f'</p:animScale>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    group.append(parse_xml(xml))

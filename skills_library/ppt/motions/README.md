# Motion Skills — Metadata Schema

Every file in `skills_library/ppt/motions/` (except `_*.py` helpers) is a
motion skill and must export the module-level attributes below. The MCP
server (`domains/ppt/mcp_server/server.py::_load_motions`) reads them
to rank candidates for every slide the agent builds.

## Required attributes

```python
NAME            = "dramatic_zoom"                        # str — unique motion id (usually == filename stem)
CATEGORY        = "entrance"                              # {entrance, emphasis, ambient, transition, text, composite}
DESCRIPTION     = "One-line elevator pitch (<= 120 chars)."

APPLICABILITY = {                                         # hard filters for Pass-0 pruning
    "roles":                   ["cover", "section_divider", ...],
    "anchor_names":            ["headline", "title", ...],           # exact-name allow-list
    "anchor_name_regex":       r"(headline|title|hero_\w+)",          # regex allow-list
    "requires_morph_pair":     False,                                 # only apply on slide B of a morph pair
    "max_per_slide":           1,                                     # hard cap per slide
}

PARAMETERS = {                                            # apply()'s accepted params + defaults + bounds
    "delay_ms":    {"type": "int",   "default": 200, "min": 0,   "max": 4000},
    "duration_ms": {"type": "int",   "default": 900, "min": 300, "max": 3000},
}

def apply(slide, target_shape, params=None):
    ...
```

## New (Phase-A) attributes for semantic ranking

```python
TAGS = [                                                  # list[str] — free-form descriptor keywords
    "dramatic", "cinematic", "hero-reveal", "apple-keynote",
]

INTENSITY = 8                                             # int 1..10 — dramatic amplitude (1=subtle, 10=theatrical)

EMBEDDING_TEXT = """                                      # rich, semantic description for vector search.
Cinematic 10% -> 100% scale-in over 900ms. Best for       # One paragraph. Written for LLM retrieval, not humans.
hero numbers, section dividers, and cover headlines       # Include: what it looks like, when to use it,
that need to feel like they "arrive." Produces an         # typical content signal (digits, headline text,
Apple-keynote product-reveal sensation.                   # icon, etc), and similar/alternative motions.
"""

CONTENT_MATCHERS = {                                      # Signals computed from slot text or shape metadata.
    "digits":      True,                                  # fires when target text contains digits
    "percent_sign": False,
    "all_caps":    False,
    "is_headline": True,                                  # target is a headline-style shape
    "min_chars":   1,
    "max_chars":   120,
}

COMPLEMENTARY_WITH = ["breathing_halo", "orbital_accent"] # list[str] — motion ids that pair well on the same slide

CONFLICTS_WITH = ["grow_reveal", "zoom_from_center"]      # list[str] — never apply alongside any of these
                                                          # (same shape OR same slide depending on CATEGORY)
```

## Notes

- `EMBEDDING_TEXT` is the field the MCP `list_motions` semantic ranker
  embeds via Azure OpenAI. Keep it 2-5 sentences, rich in signal words
  (anchor-name hints, content-shape hints, intensity cues, analogous
  motions). Do NOT just paste `DESCRIPTION`.
- `CONFLICTS_WITH` applies:
  - On the **same shape** for entrance/emphasis categories (can't fade
    AND zoom the same text).
  - On the **same slide** for ambient/transition categories (one orbit
    per slide; two fighting ambients look busy).
- `COMPLEMENTARY_WITH` is used by the picker as a soft boost when one
  of those ids has already been picked on the same slide.
- `CONTENT_MATCHERS` signals are cheap to compute; leave any unused
  keys out of the dict (they default to "don't care").
- New motion skills distilled by `scripts/distill_motion_skills.py`
  are generated with ALL these fields populated.

# Hero Search Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimalist, centered layout featuring a prominent headline and a stylized search bar, ideal for transition slides, posing a core question, or introducing a tutorial step.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_search_divider_0ee5c3/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+search_bar"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "section_divider",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "realistic_typewriter_rhythm_morph_frame__44d189cb"
    }
  },
  "quality": {
    "contrast_ok": true,
    "exec_ok": true,
    "overlap_ok": true,
    "render_ok": true,
    "usage_count": 0
  },
  "skill_type": "shell",
  "slots": [
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "search_query",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
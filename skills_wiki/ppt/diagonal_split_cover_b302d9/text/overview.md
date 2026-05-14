# Diagonal Split Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A simple cover layout with a bold headline, optional subhead, and dynamic diagonal accent shapes on the right to add visual interest.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/diagonal_split_cover_b302d9/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "diagonal-split-title"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "bold",
      "minimal"
    ],
    "slide_role": [
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "modern_diagonal_split_hero_layout_e3e352f8"
    }
  },
  "quality": {
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
      "max_chars": 100,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
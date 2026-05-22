# Geometric Chevron Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold, minimal geometric layout ideal for covers or section dividers, using a large rotated triangle to create a dynamic split background.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/geometric_chevron_cover_afbd78/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold",
      "corporate"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "dynamic_layered_chevron_reveal_ecf2eeb7"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
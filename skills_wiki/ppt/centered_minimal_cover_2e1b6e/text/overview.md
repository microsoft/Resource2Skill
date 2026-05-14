# Centered Minimal Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A classic, minimal cover slide with a large centered headline and an optional subtitle.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_minimal_cover_2e1b6e/render.py",
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
      "corporate",
      "editorial"
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
      "video_id": "strict_5_color_thematic_styling_6f675bf7"
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
      "max_chars": 150,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
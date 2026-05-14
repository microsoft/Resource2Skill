# Minimal Centered Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A clean, minimal cover or section divider with a centered headline and optional subtitle, maximizing whitespace for a modern corporate look.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_centered_cover_e5bcfe/render.py",
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
      "clean"
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
      "video_id": "off_canvas_geometric_masking_4e155db3"
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
      "max_chars": 120,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
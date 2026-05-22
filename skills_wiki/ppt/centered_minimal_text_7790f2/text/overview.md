# Centered Minimal Text

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimal, vertically-centered text layout perfect for section dividers, bold statements, or closing remarks, utilizing an accent color for the subhead to create visual interest.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_minimal_text_7790f2/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "centered-text"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "editorial",
      "corporate"
    ],
    "slide_role": [
      "section_divider",
      "closing",
      "quote"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "asymmetric_tri_panel_pillar_layout_edito_4edf740a"
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
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
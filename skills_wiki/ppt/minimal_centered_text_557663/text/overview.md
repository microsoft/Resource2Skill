# Minimal Centered Text

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A clean, minimal layout focusing on a central message block with an optional accent subhead and supporting body text, ideal for section dividers or impactful statements.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_centered_text_557663/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "centered-text-block"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "editorial",
      "corporate"
    ],
    "slide_role": [
      "section_divider",
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
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 400,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
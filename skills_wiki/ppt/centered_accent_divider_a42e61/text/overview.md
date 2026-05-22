# Centered Accent Divider

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "A bold, centered layout using nested rectangles to draw focus to a short title, ideal for section transitions.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_accent_divider_a42e61/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "nested-rectangles-centered"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold",
      "corporate"
    ],
    "slide_role": [
      "section_divider",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "neumorphic_dual_shadow_card_soft_ui_embo_e8daa7ea"
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
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "subtitle",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
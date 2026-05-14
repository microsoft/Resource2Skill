# Minimal Text Focus

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted from a minimal tutorial slide featuring a prominent central text block and a decorative vertical text column, suitable for a section divider or quote.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_text_focus_7c4428/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "minimal-text-split"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "technical"
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
      "video_id": "dynamic_odometer_morph_b82ac55d"
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
      "name": "decorative_text",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "main_text",
      "required": true,
      "style": "title_xl"
    }
  ],
  "status": "active"
}
```
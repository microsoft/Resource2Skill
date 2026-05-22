# Centered Quote Panel

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the core layout of a prominent central quote block with an optional title, abstracting away the specific animation graphics to create a clean, reusable quote shell.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_quote_panel_2a2563/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+centered-panel"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "editorial",
      "corporate"
    ],
    "slide_role": [
      "quote"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "roll_down_canvas_projector_screen_reveal_d76458a0"
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
      "max_chars": 80,
      "name": "headline",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 250,
      "name": "quote",
      "required": true,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "author",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
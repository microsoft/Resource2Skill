# Pull-down Quote Panel

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the 'pulldown blind' visual into a clean, themeable central panel with an overhanging accent bar, focusing on a prominent quote display.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/pull_down_quote_panel_523246/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+centered-panel"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "editorial"
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
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "quote",
      "required": true,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
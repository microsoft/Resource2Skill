# Blank Canvas

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The provided image is completely blank, so this shell represents a minimal canvas with an optional centered message, suitable for a closing or transition slide.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/blank_canvas_f8a389/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "blank"
    ],
    "density": "low",
    "mood": [
      "minimal"
    ],
    "slide_role": [
      "closing",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "hero_object_showcase_layout_755bd3b7"
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
      "name": "message",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
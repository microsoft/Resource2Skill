# Chevron List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses a chevron overlapping a rounded rectangle to recreate the process-flow visual from the image.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/chevron_list_461f89/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "4-item vertical chevron list"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "bold",
      "technical"
    ],
    "slide_role": [
      "bullet_card_list",
      "agenda"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "interlocking_chevron_progress_agenda_18bb282b"
    }
  },
  "quality": {
    "exec_ok": true,
    "overlap_ok": false,
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
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
# Horizontal Task Progress

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the 3-row task list with horizontal progress/timeline bars into a reusable layout, splitting text on the left and visual bars on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/horizontal_task_progress_f46595/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+3-row-progress"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "minimal",
      "technical"
    ],
    "slide_role": [
      "timeline_horizontal",
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "minimalist_infographic_progress_dashboar_7511aa65"
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
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
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
# Central Circle

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a single large centered circle. Extracted as a minimal section divider with an optional centered headline slot to make it functional as a presentation slide.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/central_circle_a706ac/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "central-circle"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold"
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
      "video_id": "exploded_segmented_process_wheel_f994d439"
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
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
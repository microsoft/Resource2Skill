# Two Column Big Number List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracted the two vertical strips of numbers into a reusable 2-column list layout where the 'title' of each bullet acts as the large metric/number, and an optional 'body' provides context.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_column_big_number_list_be9664/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column list with large numbers"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "corporate"
    ],
    "slide_role": [
      "bullet_card_list",
      "feature_grid"
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
      "max_chars": 80,
      "name": "headline",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 10,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
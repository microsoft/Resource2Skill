# Two-Column Numbered Grid

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Adapts the visual of a large 2-column number sequence into a practical 10-item numbered list shell, using theme typography for the oversized numbers.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_column_numbered_grid_1937f3/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column-numbered-list"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "corporate",
      "technical"
    ],
    "slide_role": [
      "bullet_card_list",
      "feature_grid"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "dynamic_odometer_morph_b82ac55d"
    }
  },
  "quality": {
    "contrast_ok": true,
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
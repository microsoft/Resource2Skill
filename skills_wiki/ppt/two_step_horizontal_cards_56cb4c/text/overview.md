# Two Step Horizontal Cards

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a 2-step horizontal card layout with overlapping circular step indicators and ribbon accents.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_step_horizontal_cards_56cb4c/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-horizontal-cards"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "bold",
      "playful"
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
      "video_id": "12_point_3d_ribbon_agenda_grid_ca5d4bc8"
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
      "bullet_capacity": 2,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "steps",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
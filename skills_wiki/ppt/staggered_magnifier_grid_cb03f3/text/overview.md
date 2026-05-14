# Staggered Magnifier Grid

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses a staggered 3-column layout with custom-drawn magnifying glass graphics to highlight key features or steps in a playful yet structured way.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/staggered_magnifier_grid_cb03f3/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "staggered-3-column-icons"
    ],
    "density": "low",
    "mood": [
      "playful",
      "corporate",
      "bold"
    ],
    "slide_role": [
      "feature_grid",
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "split_pane_b_w_hero_with_oversized_accen_3619ee33"
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
      "name": "features",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
# Left Circular Diagram

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the circular text graphic into a reusable donut diagram with dynamically distributed and rotated labels, paired with a right-aligned text block.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_circular_diagram_a9e486/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "donut+labels+text"
    ],
    "density": "medium",
    "mood": [
      "playful",
      "bold",
      "corporate"
    ],
    "slide_role": [
      "feature_grid",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "rotating_dial_morph_panel_wheel_selector_87d765bb"
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
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": 8,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "labels",
      "required": false,
      "style": null
    }
  ],
  "status": "candidate"
}
```
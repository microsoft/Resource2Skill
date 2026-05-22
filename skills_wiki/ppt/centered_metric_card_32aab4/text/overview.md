# Centered Metric Card

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A high-impact, low-density layout focusing entirely on a single key metric, using a bordered card to draw the eye and separating the value from its unit for typographic contrast.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_metric_card_32aab4/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+metric_card"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "bold",
      "warm"
    ],
    "slide_role": [
      "metric_dashboard"
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
      "max_chars": 60,
      "name": "headline",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 15,
      "name": "metric_value",
      "required": true,
      "style": "metric_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 10,
      "name": "metric_unit",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
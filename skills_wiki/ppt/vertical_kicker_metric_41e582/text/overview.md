# Vertical Kicker Metric

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Abstracts the tutorial slide into a minimal metric layout featuring a stylized vertical text column and a prominent central metric.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_kicker_metric_41e582/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "vertical-text+large-metric"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold",
      "playful"
    ],
    "slide_role": [
      "metric_dashboard",
      "section_divider"
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
      "max_chars": 15,
      "name": "vertical_kicker",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "main_metric",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "caption",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
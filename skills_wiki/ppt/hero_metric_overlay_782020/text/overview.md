# Hero Metric Overlay

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A highly visual, low-density layout focusing entirely on a single massive metric overlaid on a full-bleed background image, ideal for dramatic reveals or key statistics.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_metric_overlay_782020/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "full-bleed-image+giant-metric"
    ],
    "density": "low",
    "mood": [
      "bold",
      "minimal",
      "editorial"
    ],
    "slide_role": [
      "metric_dashboard",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "odometer_morph_reveal_b7b6b050"
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
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "background_image",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 15,
      "name": "metric",
      "required": true,
      "style": "metric_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "label",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
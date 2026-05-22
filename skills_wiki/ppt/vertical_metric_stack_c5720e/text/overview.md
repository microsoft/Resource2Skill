# Vertical Metric Stack

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The slide features a prominent vertical column of large numbers. This is extracted as a 'Vertical Metric Stack' layout, taking a list of metrics and centering them vertically and horizontally using the metric_xl typography style.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_metric_stack_c5720e/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "vertical-stack"
    ],
    "density": "low",
    "mood": [
      "bold",
      "minimal",
      "playful"
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
      "video_id": "odometer_morph_reveal_slot_machine_scrol_a64dadff"
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
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "metrics",
      "required": true,
      "style": "metric_xl"
    }
  ],
  "status": "active"
}
```
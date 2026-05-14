# Waterfall Chart Layout

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A clean, full-slide layout designed to showcase a single complex chart (like a waterfall chart) with a prominent headline.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/waterfall_chart_layout_bee5b6/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+chart"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "minimal"
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
      "video_id": "consulting_style_high_data_to_ink_chart__8824e483"
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
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "chart_data",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
# Dashboard Split with Metrics

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a 3-panel dashboard layout featuring a large primary area on the left, a secondary area top-right, and a 2x2 metric grid bottom-right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/dashboard_split_with_metrics_4b5b71/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "chart+chart+4-metrics"
    ],
    "density": "high",
    "mood": [
      "corporate",
      "technical",
      "bold"
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
      "video_id": "neo_dark_analytics_dashboard_901dde61"
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
      "kind": "chart",
      "max_chars": null,
      "name": "main_chart",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "secondary_chart",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "metrics",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
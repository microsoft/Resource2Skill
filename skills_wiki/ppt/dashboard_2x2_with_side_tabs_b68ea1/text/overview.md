# Dashboard 2x2 with Side Tabs

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A 2x2 dashboard layout with large chart areas on the left and tabbed panels on the right for secondary charts and key metrics.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/dashboard_2x2_with_side_tabs_b68ea1/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2x2-grid-charts-metrics"
    ],
    "density": "high",
    "mood": [
      "technical",
      "corporate",
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
      "kind": "chart",
      "max_chars": null,
      "name": "chart_top_left",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "chart_bottom_left",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "chart_top_right",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "label_top_right",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "label_bottom_right",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": 2,
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
# Metric Doughnut Focus

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a minimal, high-impact metric layout featuring a central doughnut chart, a large metric value, and a rotated sidebar accent.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/metric_doughnut_focus_7a68c5/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+doughnut-metric"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "bold"
    ],
    "slide_role": [
      "metric_dashboard",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "gradient_widesweep_doughnut_dashboards_a34e1e60"
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
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 10,
      "name": "metric",
      "required": true,
      "style": "metric_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "sidebar_text",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
# Centered Metric Ring

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A high-impact, low-density layout focusing on a single key metric surrounded by a decorative ring, ideal for section dividers or dashboard highlights.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_metric_ring_be3c3d/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle+metric-ring"
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
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
    }
  ],
  "status": "active"
}
```
# Triple Gauge Dashboard

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the 3-column gauge dashboard shown in the slide thumbnail, using masked donuts to reliably create semi-circular metric charts across different PowerPoint versions.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/triple_gauge_dashboard_b2d47d/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+3-gauges"
    ],
    "density": "low",
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
      "video_id": "executive_dashboard_gauge_panel_9ab8ceb0"
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
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
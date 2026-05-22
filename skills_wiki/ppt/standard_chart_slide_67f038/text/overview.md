# Standard Chart Slide

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A clean, full-width chart layout with dedicated slots for chart title, subtitle, and a footer, separated by a hairline for a professional corporate look.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/standard_chart_slide_67f038/render.py",
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
      "minimal",
      "technical"
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
      "max_chars": 100,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "chart_title",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "chart_subtitle",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "chart",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "footer",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
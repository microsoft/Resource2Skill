# Chart with Context Header

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Provides a structured header with subtitle and context metadata above a large dedicated chart area, typical for financial or data-heavy presentations.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/chart_with_context_header_cb23d9/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "header+chart+footer"
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
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "context",
      "required": false,
      "style": "caption"
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
      "max_chars": 100,
      "name": "footer",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
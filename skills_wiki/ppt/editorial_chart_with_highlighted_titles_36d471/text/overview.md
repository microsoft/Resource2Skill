# Editorial Chart with Highlighted Titles

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A chart-focused layout with prominent, panel-backed headline and subtitle for editorial emphasis.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/editorial_chart_with_highlighted_titles_36d471/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle+chart"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "corporate",
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
      "video_id": "editorial_data_highlighting_panel_7f1b3b9d"
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
      "max_chars": 80,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "chart_title",
      "required": false,
      "style": "body_bold"
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
      "name": "source",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
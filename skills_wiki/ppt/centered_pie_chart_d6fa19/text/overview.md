# Centered Pie Chart

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the centered pie chart layout with a bottom legend, using a bullet list slot to populate the legend items.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_pie_chart_d6fa19/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "chart+legend"
    ],
    "density": "low",
    "mood": [
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
      "video_id": "interactive_gamified_spinning_wheel_whee_cecf461b"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 14,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "data_points",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
# Dashboard Split

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Adapts the SCADA interface into a generic dashboard layout with a large top visual area and a bottom data table.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/dashboard_split_72fc93/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-image+data-table"
    ],
    "density": "high",
    "mood": [
      "technical",
      "corporate"
    ],
    "slide_role": [
      "metric_dashboard"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "industrial_scada_iiot_dashboard_layout_4632f98a"
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
      "aspect": "16:5",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "data_list",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
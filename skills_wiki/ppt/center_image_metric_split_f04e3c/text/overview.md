# Center Image Metric Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold metric layout with a central overlapping image, separating a large statistic from its descriptive headline.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/center_image_metric_split_f04e3c/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "metric+image+headline"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "editorial"
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
      "video_id": "pictograph_matrix_100_icon_array_percent_822e79f7"
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
      "max_chars": 10,
      "name": "metric",
      "required": true,
      "style": "metric_xl"
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 50,
      "name": "footnote",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 50,
      "name": "footer",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
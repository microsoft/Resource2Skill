# Metric Split with Image

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a clean, corporate metric highlight slide with a prominent title section separated by horizontal rules, and a two-column split for a large metric and a supporting image.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/metric_split_with_image_1ad22b/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+metric_split_image"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "minimal",
      "editorial"
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
      "video_id": "morphing_odometer_reveal_77605ecf"
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
      "max_chars": 60,
      "name": "title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "metric_label",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 10,
      "name": "metric_value",
      "required": true,
      "style": "metric_xl"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
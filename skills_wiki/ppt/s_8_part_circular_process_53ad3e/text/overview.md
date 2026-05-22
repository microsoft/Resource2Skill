# 8-Part Circular Process

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a user constructing an 8-segment circular diagram (donut chart). The shell recreates this using pie shapes with a center cutout, providing slots for a headline, an optional center label, and 8 surrounding text items.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/8_part_circular_process_53ad3e/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "circular-diagram-8-parts"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "bold"
    ],
    "slide_role": [
      "feature_grid",
      "metric_dashboard"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "radial_segmented_infographic_wheel_c09cf8ee"
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
      "max_chars": 80,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "center_label",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": 8,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
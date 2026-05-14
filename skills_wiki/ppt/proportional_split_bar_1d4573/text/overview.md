# Proportional Split Bar

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the proportional horizontal bar chart into a reusable shell that automatically calculates segment widths based on numbers parsed from the segment titles, complete with a bottom bracket for the total.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/proportional_split_bar_1d4573/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "horizontal-stacked-bar"
    ],
    "density": "low",
    "mood": [
      "technical",
      "minimal",
      "corporate"
    ],
    "slide_role": [
      "metric_dashboard",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "60_30_10_proportional_color_harmony_4ab644e5"
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
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "total_label",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "segments",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
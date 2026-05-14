# Comparison Split Charts

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A side-by-side comparison layout ideal for contrasting two data visualizations or concepts, featuring a strong header, subtitle, and a full-width divider.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/comparison_split_charts_00d636/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle+2-charts"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "minimal"
    ],
    "slide_role": [
      "comparison_split"
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
      "max_chars": 120,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "left_chart",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "right_chart",
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
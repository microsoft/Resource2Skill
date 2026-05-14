# Text and Chart Split

## Parameters

```json
{
  "_distill_attempts": 3,
  "_distill_reasoning": "A classic split layout with a prominent centered header, left-aligned explanatory text, and a right-aligned data visualization area.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/text_and_chart_split_6a7639/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "header+text-left+chart-right"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "minimal"
    ],
    "slide_role": [
      "metric_dashboard",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.6499999999999999,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "grid_driven_composition_toolkit_golden_r_758ba0e6"
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
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 600,
      "name": "body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "chart",
      "max_chars": null,
      "name": "chart",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
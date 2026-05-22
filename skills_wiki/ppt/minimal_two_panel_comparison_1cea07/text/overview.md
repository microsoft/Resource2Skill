# Minimal Two-Panel Comparison

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Two large, distinct colored panels suggest a direct comparison or dichotomy, ideal for a minimal comparison split.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_two_panel_comparison_1cea07/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "two large colored panels side-by-side"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "bold"
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
      "video_id": "off_canvas_geometric_masking_4e155db3"
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
      "max_chars": 40,
      "name": "left_title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "left_body",
      "required": true,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "right_title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "right_body",
      "required": true,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
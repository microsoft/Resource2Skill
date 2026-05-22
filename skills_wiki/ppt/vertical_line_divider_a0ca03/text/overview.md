# Vertical Line Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a minimal vertical line being drawn on a blank canvas. This is interpreted as a minimal section divider layout featuring a central accent line and adjacent text.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_line_divider_a0ca03/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "vertical-line+text"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate"
    ],
    "slide_role": [
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "minimalist_spatial_masking_line_reveal_bb618084"
    }
  },
  "quality": {
    "contrast_ok": true,
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
      "style": "body"
    }
  ],
  "status": "active"
}
```
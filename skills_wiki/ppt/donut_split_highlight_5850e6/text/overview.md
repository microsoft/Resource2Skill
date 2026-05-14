# Donut Split Highlight

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A split layout featuring a prominent circular graphic on the left with an intersecting accent bar, balanced by a headline and bulleted list on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/donut_split_highlight_5850e6/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "left-donut-right-text"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "comparison_split",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "rotating_dial_morph_panel_wheel_selector_87d765bb"
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "accent_label",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
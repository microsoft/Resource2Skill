# Donut Split List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A split layout featuring a prominent circular graphic on the left and a highlighted title with supporting bullets on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/donut_split_list_d6da67/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "donut-graphic+highlighted-title+bullets"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "comparison_split",
      "feature_grid"
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
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": "body"
    }
  ],
  "status": "active"
}
```
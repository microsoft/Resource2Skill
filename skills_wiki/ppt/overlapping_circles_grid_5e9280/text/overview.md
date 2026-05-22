# Overlapping Circles Grid

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a 3-item feature grid using overlapping circles to match the visual structure of the source image, drawing the middle circle last so it sits on top.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/overlapping_circles_grid_5e9280/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+3-overlapping-circles"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "feature_grid",
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "dark_neumorphism_soft_ui_interface_f0feaa9c"
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
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
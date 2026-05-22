# Hero with Top Accent

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted from a slide with a prominent bottom-right image and top-right accent shape, adding left-aligned text slots to create a functional cover or divider.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_with_top_accent_a63484/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "text-left+image-right+accent-top-right"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "minimal"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "custom_motion_path_animation_visualizati_a31dbf79"
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
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
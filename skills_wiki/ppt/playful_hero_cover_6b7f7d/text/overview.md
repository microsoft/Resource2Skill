# Playful Hero Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted from a motion-path tutorial slide, adapted into a dynamic cover layout with a floating hero image and top-hanging accent block to balance left-aligned text.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/playful_hero_cover_6b7f7d/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "text-left+floating-hero-right"
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
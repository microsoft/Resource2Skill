# Geometric Hero Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a bold, geometric cover layout by combining standard shapes (Rectangle, Right Triangle, Isosceles Triangle) to recreate the complex diagonal overlays seen in the image, providing a dark container for light text over a full-bleed background image.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/geometric_hero_cover_8dd6fc/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-image+geometric-overlay"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "cool",
      "editorial"
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
      "video_id": "geometric_glass_shard_reveal_08e33e3c"
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
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    },
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
      "max_chars": 120,
      "name": "subtitle",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
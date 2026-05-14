# Full Bleed Image Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The slide consists entirely of a single full-bleed image. Extracted as a cover shell with a required image slot and an optional headline slot to ensure it functions as a reusable template.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/full_bleed_image_cover_2e0554/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "full-bleed-image"
    ],
    "density": "low",
    "mood": [
      "editorial",
      "minimal",
      "cool"
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
      "video_id": "geometric_shape_intersect_parallax_layer_a45c0b73"
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
      "max_chars": 80,
      "name": "headline",
      "required": false,
      "style": "title_xl"
    }
  ],
  "status": "active"
}
```
# Product Reveal Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimal split layout featuring a tall hero image on the left and large, impactful typography on the right, ideal for product reveals or section covers.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/product_reveal_split_195c80/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "image-left+text-right"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "bold"
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
      "video_id": "cinematic_dark_mode_product_reveal_525d9893"
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
      "aspect": "9:16",
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 50,
      "name": "subtitle",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
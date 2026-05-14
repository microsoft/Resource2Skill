# Product Hero Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the classic landing-page hero layout into a presentation slide, featuring a strong left-aligned value proposition, an optional call-to-action button, and a prominent right-aligned product visual.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/product_hero_split_9fb944/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "left-text-cta-right-image"
    ],
    "density": "low",
    "mood": [
      "bold",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "corporate_brand_color_theming_applicatio_beca0d51"
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
      "max_chars": 120,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "cta_text",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": "4:3",
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
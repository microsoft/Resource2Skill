# Centered Photo Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "A minimal cover or section divider featuring a full-bleed background image and a centered, framed title box.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_photo_cover_208e82/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "full-bleed-image+centered-title-box"
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
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "product_feature_magnifying_glass_callout_ce5d7f13"
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
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "background_image",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subtitle",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "footer",
      "required": false,
      "style": "caption"
    }
  ],
  "status": "active"
}
```
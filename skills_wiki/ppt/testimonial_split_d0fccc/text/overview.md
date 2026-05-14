# Testimonial Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A split horizontal layout featuring a hero image header with an overlaid title, and a distinct lower panel for the testimonial quote and author details.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/testimonial_split_d0fccc/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "image-header+quote-panel"
    ],
    "density": "low",
    "mood": [
      "editorial",
      "warm",
      "minimal"
    ],
    "slide_role": [
      "quote"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "horizontal_testimonial_carousel_social_p_19600d28"
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
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": "landscape",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    },
    {
      "aspect": "square",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "author_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "author_name",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "author_title",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "quote",
      "required": true,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
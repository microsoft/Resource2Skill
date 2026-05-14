# Split Banner Testimonial

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Separates the visual context (hero image and headline) from the specific testimonial content (author and quote) using distinct horizontal panels.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/split_banner_testimonial_134c21/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "split-banner+author-quote-panel"
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
      "max_chars": 50,
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
      "aspect": "3:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
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
      "max_chars": 40,
      "name": "author_name",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "author_role",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 250,
      "name": "quote",
      "required": true,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
# Cinematic Split Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Inspired by the UI screenshot's letterboxed layout, this shell uses dark top and bottom panels to frame a central hero image, perfect for dramatic covers or section dividers.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/cinematic_split_cover_7a2759/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "letterbox-image-with-bars"
    ],
    "density": "low",
    "mood": [
      "editorial",
      "bold",
      "minimal"
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
      "video_id": "pop_art_duotone_aesthetic_bd1702bf"
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
      "aspect": "16:6",
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
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
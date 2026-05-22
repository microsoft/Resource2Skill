# Simple Hero Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A highly minimal cover or feature slide consisting of a prominent headline and a large hero image, ideal for impactful visual introductions.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/simple_hero_cover_453db2/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+hero_image"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "editorial",
      "bold"
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
      "video_id": "hero_object_showcase_layout_755bd3b7"
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
      "aspect": "16:9",
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
# Bordered Hero Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "The slide features a large central graphic, which translates well to a hero image slot with an optional headline overlay.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/bordered_hero_cover_462a1f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-image"
    ],
    "density": "low",
    "mood": [
      "bold",
      "playful"
    ],
    "slide_role": [
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "retro_futuristic_flight_perspective_grid_62e4eb2c"
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
      "name": "hero_image",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "headline",
      "required": false,
      "style": "title_xl"
    }
  ],
  "status": "active"
}
```
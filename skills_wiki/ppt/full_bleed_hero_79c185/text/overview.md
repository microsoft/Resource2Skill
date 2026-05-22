# Full Bleed Hero

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the full-bleed cinematic visual into a reusable cover/divider shell, adding optional text slots in the lower third for practical presentation use.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/full_bleed_hero_79c185/render.py",
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
      "bold",
      "minimal",
      "warm"
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
      "video_id": "curated_identity_moodboard_grid_c7632290"
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
      "required": false,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
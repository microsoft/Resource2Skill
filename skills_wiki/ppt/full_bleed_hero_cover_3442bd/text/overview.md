# Full Bleed Hero Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Extracts a full-bleed image cover slide with a massive headline and optional subtitle, matching the visual hierarchy of the 2019 cityscape slide.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/full_bleed_hero_cover_3442bd/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero_image+headline"
    ],
    "density": "low",
    "mood": [
      "bold",
      "editorial",
      "corporate"
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
      "video_id": "dynamic_layered_chevron_reveal_ecf2eeb7"
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
      "max_chars": 30,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subtitle",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
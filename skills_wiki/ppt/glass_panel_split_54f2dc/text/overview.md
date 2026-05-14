# Glass Panel Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold, editorial layout featuring a central rounded panel over a full-bleed background, splitting content between a hero image and text.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/glass_panel_split_54f2dc/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "image+text inside rounded panel"
    ],
    "density": "low",
    "mood": [
      "editorial",
      "bold",
      "playful"
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
      "video_id": "frosted_glassmorphism_reveal_panel_88606e27"
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
      "required": false,
      "style": null
    },
    {
      "aspect": "3:4",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
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
      "max_chars": 300,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
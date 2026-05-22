# Curved Split Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A dynamic cover layout using a large oval overlay to create a curved split between the hero image and the title area.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/curved_split_cover_fa6ce6/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "curved-split-cover"
    ],
    "density": "low",
    "mood": [
      "playful",
      "warm",
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
      "video_id": "unified_master_layout_branding_51b40dd8"
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
      "aspect": "4:3",
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
      "required": true,
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
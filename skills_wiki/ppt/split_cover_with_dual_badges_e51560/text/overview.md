# Split Cover with Dual Badges

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the left-aligned hero image and right-aligned dual square accents into a reusable cover/divider layout with optional text.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/split_cover_with_dual_badges_e51560/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "left-hero+right-badges-and-text"
    ],
    "density": "low",
    "mood": [
      "playful",
      "editorial",
      "bold"
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
      "video_id": "60_30_10_proportional_color_harmony_4ab644e5"
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
      "max_chars": 60,
      "name": "headline",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "badge_1",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "badge_2",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
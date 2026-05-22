# Diamond Focus Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the geometric diamond grid aesthetic, using a central rotated rounded rectangle as a focal point for text, with an optional background image or a surrounding grid pattern fallback.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/diamond_focus_cover_1bb638/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "diamond-grid-hero"
    ],
    "density": "low",
    "mood": [
      "bold",
      "playful",
      "corporate"
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
      "video_id": "interlocking_diamond_mask_reveal_5087eb7a"
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
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "subtitle",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
# Rotating Wheel Bullet List

## Parameters

```json
{
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/rotating_wheel_bullet_list_21bc3f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "ambient_capable": true,
    "compatible_themes": [],
    "content_shape": [
      "ambient-wheel+banners+bullets"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "bullet_card_list",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "notes": "reasoning: The slide features a prominent rotating wheel graphic on the left, a top CTA banner, an arrow-shaped subhead banner, and a bulleted list. The ambient rotation primitives perfectly capture the continuous motion implied by the circular text layout. (attempts: 2)",
    "source": {
      "timestamp": "00:00:01",
      "type": "youtube",
      "video_id": "rotating_dial_orbit_calibration"
    }
  },
  "quality": {
    "contrast_ok": true,
    "exec_ok": true,
    "overlap_ok": true,
    "render_ok": true
  },
  "skill_type": "shell",
  "slots": [
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 25,
      "name": "call_to_action",
      "required": false,
      "style": "title"
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
      "max_chars": 40,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
# Centered Title & Bullets

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimal, low-density layout featuring a prominent centered headline and a block of large bullet points below it, ideal for simple, impactful statements.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_title_bullets_39e368/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+bullets"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold",
      "playful"
    ],
    "slide_role": [
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "seamless_directional_continuity_cross_sl_3495fd00"
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
      "aspect": null,
      "bullet_capacity": 5,
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
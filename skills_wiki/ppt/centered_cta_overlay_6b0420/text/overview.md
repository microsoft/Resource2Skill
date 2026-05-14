# Centered CTA Overlay

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "A bold, centered call-to-action layout with a full-bleed background image, large headline, and a prominent button.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_cta_overlay_6b0420/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-image+centered-title+button"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "closing",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "glassmorphic_concentric_pill_overlay_312de8cf"
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
      "max_chars": 50,
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "button_text",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
# Minimal Central Card

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image displays a single, centered rounded rectangle. This translates perfectly into a minimal central card layout, ideal for section dividers, key takeaways, or quotes.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_central_card_739dff/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "central-card"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "clean"
    ],
    "slide_role": [
      "section_divider",
      "quote"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "neumorphic_dual_shadow_card_soft_ui_embo_e8daa7ea"
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
      "max_chars": 80,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "subhead",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
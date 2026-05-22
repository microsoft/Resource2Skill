# Bottom Banner Focus

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold bottom banner for the primary headline, with an optional central panel for supporting text, inspired by the tutorial's focus state.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/bottom_banner_focus_d6b421/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "bottom-banner+center-panel"
    ],
    "density": "low",
    "mood": [
      "bold",
      "minimal",
      "technical"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
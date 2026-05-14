# Wheel and CTA

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the segmented wheel as a central graphic and the 'SUBSCRIBED' banner as a prominent call-to-action button, suitable for a closing slide.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/wheel_and_cta_e8f788/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "wheel+cta-button"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold"
    ],
    "slide_role": [
      "closing"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "exploded_segmented_process_wheel_f994d439"
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
      "max_chars": 20,
      "name": "headline",
      "required": true,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
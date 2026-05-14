# Scroll Quote Reveal

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Extracted a centered quote layout inspired by the horizontal scroll graphic, using a prominent accent bar and large typography.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/scroll_quote_reveal_1cf6f6/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+centered-quote"
    ],
    "density": "low",
    "mood": [
      "playful",
      "corporate",
      "minimal"
    ],
    "slide_role": [
      "quote"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "roll_down_canvas_projector_screen_reveal_d76458a0"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "quote",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "author",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
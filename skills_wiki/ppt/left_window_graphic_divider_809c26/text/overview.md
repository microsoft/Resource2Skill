# Left Window Graphic Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the prominent window-pane graphic from the tutorial screenshot as a central visual element, adding optional text slots to form a functional section divider layout.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_window_graphic_divider_809c26/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "graphic+text"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "technical"
    ],
    "slide_role": [
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "3d_morphing_reveal_window_spatial_narrat_bdaa833a"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
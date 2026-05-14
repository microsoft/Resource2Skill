# Minimal Circle Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a minimal background with a large off-center circle on the left; inferred a clean section divider layout with text vertically centered in the empty space on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_circle_divider_7ea701/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "cool",
      "editorial"
    ],
    "slide_role": [
      "section_divider",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "neumorphic_soft_ui_styling_a9611a22"
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
      "max_chars": 30,
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
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
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
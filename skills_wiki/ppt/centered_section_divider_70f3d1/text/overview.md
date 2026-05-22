# Centered Section Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimal, centered layout perfect for section transitions, featuring a prominent title, a thick accent divider, a subtitle, and an optional central graphic.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_section_divider_70f3d1/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle+image"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "playful",
      "corporate"
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
      "video_id": "sequential_object_visibility_state_seque_7187b77e"
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
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": "16:9",
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
# Hero Image Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The visible slide content behind the UI menu suggests a simple cover layout with a central hero image (soccer ball) and space for a prominent title at the top.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_image_cover_21c6e5/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+hero_image"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "minimal"
    ],
    "slide_role": [
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "custom_motion_path_animation_visualizati_a31dbf79"
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
      "style": "title_xl"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
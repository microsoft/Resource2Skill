# Left Image Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Based on the visible slide content and the thumbnail preview on the left, the layout is a standard split with a top title, an image on the left half, and text on the right half.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_image_split_4ece67/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+image_left+text_right"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "corporate"
    ],
    "slide_role": [
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "hero_object_showcase_layout_755bd3b7"
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
      "aspect": "4:3",
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
      "max_chars": 500,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
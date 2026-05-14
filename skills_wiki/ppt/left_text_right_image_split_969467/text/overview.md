# Left Text Right Image Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A classic editorial split layout emphasizing a large hero image on the right with descriptive text on the left.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_text_right_image_split_969467/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "text-left+image-right"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "bold",
      "minimal"
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
      "video_id": "full_bleed_split_screen_portfolio_layout_a6c2604b"
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 500,
      "name": "body",
      "required": true,
      "style": "body"
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
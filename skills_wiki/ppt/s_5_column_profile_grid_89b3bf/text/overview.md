# 5-Column Profile Grid

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A 5-column layout ideal for introducing a team or comparing multiple entities, featuring square images and detailed descriptions.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/5_column_profile_grid_89b3bf/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "5-column image and text grid"
    ],
    "density": "high",
    "mood": [
      "editorial",
      "warm"
    ],
    "slide_role": [
      "feature_grid"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "seamless_gradient_image_blending_0cc7d66d"
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
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_1",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_2",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_3",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_4",
      "required": false,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_5",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "profiles",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "footer",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
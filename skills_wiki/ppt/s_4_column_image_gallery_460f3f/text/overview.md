# 4-Column Image Gallery

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the 4-portrait-image layout into a reusable gallery shell, adding an optional headline for versatility.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/4_column_image_gallery_460f3f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "4-image-row"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "minimal"
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
      "video_id": "interactive_morphing_profile_carousel_c9559f8a"
    }
  },
  "quality": {
    "contrast_ok": true,
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
      "aspect": "3:4",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_1",
      "required": true,
      "style": null
    },
    {
      "aspect": "3:4",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_2",
      "required": true,
      "style": null
    },
    {
      "aspect": "3:4",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_3",
      "required": true,
      "style": null
    },
    {
      "aspect": "3:4",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_4",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
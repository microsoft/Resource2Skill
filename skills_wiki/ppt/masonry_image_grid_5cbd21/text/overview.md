# Masonry Image Grid

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the staggered duotone image grid into a 3-column masonry layout, dynamically calculating heights to fit within bounds while preserving the playful, editorial mood.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/masonry_image_grid_5cbd21/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "masonry-6-image-grid"
    ],
    "density": "medium",
    "mood": [
      "playful",
      "bold",
      "editorial"
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
      "video_id": "pop_art_duotone_aesthetic_bd1702bf"
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
      "style": "title"
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
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_1",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_2",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_3",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_4",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_5",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_6",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
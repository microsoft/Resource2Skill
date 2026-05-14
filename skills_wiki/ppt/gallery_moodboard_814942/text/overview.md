# Gallery Moodboard

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the masonry image grid into a structured '1 Hero + 4 Grid' layout, ideal for moodboards or visual portfolios.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/gallery_moodboard_814942/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+hero-image+4-grid-images"
    ],
    "density": "high",
    "mood": [
      "editorial",
      "minimal"
    ],
    "slide_role": [
      "feature_grid",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "architectural_minimalist_chapter_title_b0e88c72"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": "16:9",
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
      "max_chars": 80,
      "name": "hero_caption",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "grid_image_1",
      "required": false,
      "style": null
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "grid_image_2",
      "required": false,
      "style": null
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "grid_image_3",
      "required": false,
      "style": null
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "grid_image_4",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
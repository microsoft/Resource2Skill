# Title and Full Image

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A simple, low-density layout featuring a top-left title block and a large dedicated area for a diagram or image, ideal for technical architecture or visual features.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/title_and_full_image_fe3556/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle+large-image"
    ],
    "density": "low",
    "mood": [
      "technical",
      "minimal",
      "corporate"
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
      "video_id": "isometric_3d_it_infrastructure_mapping_28530083"
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
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "diagram",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
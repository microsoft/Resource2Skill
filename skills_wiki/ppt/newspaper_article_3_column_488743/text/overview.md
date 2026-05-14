# Newspaper Article 3-Column

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a dense, editorial 3-column layout mimicking a newspaper article, featuring a prominent headline, hairlines, and an embedded image in the center column.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/newspaper_article_3_column_488743/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "header+3-columns-with-image"
    ],
    "density": "high",
    "mood": [
      "editorial",
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
      "video_id": "focal_zoom_fade_overlay_contextual_magni_70dd3e66"
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
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 50,
      "name": "byline",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 800,
      "name": "col1_text",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "caption",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 400,
      "name": "col2_text",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 800,
      "name": "col3_text",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
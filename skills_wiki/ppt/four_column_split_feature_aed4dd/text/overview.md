# Four Column Split Feature

## Parameters

```json
{
  "_distill_attempts": 3,
  "_distill_reasoning": "A 4-column editorial layout contrasting a text introduction, a full-bleed image column, and two distinct feature columns with alternating backgrounds.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/four_column_split_feature_aed4dd/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "1-text-col + 1-image-col + 2-feature-cols"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "bold",
      "corporate"
    ],
    "slide_role": [
      "feature_grid",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.6499999999999999,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "asymmetric_tri_panel_pillar_layout_edito_4edf740a"
    }
  },
  "quality": {
    "exec_ok": true,
    "overlap_ok": false,
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
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "intro_body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 2,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "features",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
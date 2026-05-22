# Diagram with Sidebar

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts a complex, full-slide network diagram into a reusable layout featuring a descriptive left sidebar for context and a large primary area on the right for the diagram image, plus an optional highlighted callout box.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/diagram_with_sidebar_65c3e2/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "sidebar-text+main-diagram"
    ],
    "density": "high",
    "mood": [
      "technical",
      "corporate",
      "informational"
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
      "max_chars": 80,
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
      "kind": "text",
      "max_chars": 400,
      "name": "details",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "diagram",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "callout",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
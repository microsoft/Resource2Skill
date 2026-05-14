# Architecture Diagram

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the complex IT architecture diagram into a reusable 3-layer center stack with optional left and right sidebars.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/architecture_diagram_a5836c/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "architecture-diagram-3-layers"
    ],
    "density": "high",
    "mood": [
      "corporate",
      "technical"
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
      "video_id": "monochromatic_hierarchical_architecture__2128c545"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "footer",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "left_title",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "left_items",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "right_title",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "right_items",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "center_layers",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
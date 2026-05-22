# Circular Concept Diagram

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the custom circular diagram into a reusable 'feature_grid' shell using a donut and arrow shape, calculating radial coordinates and dynamic text rotation to distribute items along the ring.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/circular_concept_diagram_949348/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "donut-arrow-diagram"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "feature_grid",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "rotating_dial_morph_panel_wheel_selector_87d765bb"
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
      "max_chars": 30,
      "name": "main_label",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 10,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": "caption"
    }
  ],
  "status": "candidate"
}
```
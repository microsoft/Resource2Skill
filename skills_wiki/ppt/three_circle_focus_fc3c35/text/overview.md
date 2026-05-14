# Three Circle Focus

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the prominent 3-circle layout into a reusable feature or step highlight, capturing the nested circles, step badges, and an optional descriptive footer.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/three_circle_focus_fc3c35/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "3-circle-row+description"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "technical"
    ],
    "slide_role": [
      "feature_grid",
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "glowing_concentric_data_nodes_d5937e44"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "labels",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "description",
      "required": false,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
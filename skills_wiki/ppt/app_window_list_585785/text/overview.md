# App Window List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the UI-like window layout with a numbered list on the left, a floating avatar/image on the right, and an optional action bar at the bottom.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/app_window_list_585785/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "window-panel+list+side-image"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "modern"
    ],
    "slide_role": [
      "bullet_card_list",
      "feature_grid"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "narrative_driven_highlight_chart_data_st_31af71ac"
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
      "max_chars": 100,
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    },
    {
      "aspect": "portrait",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "side_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 50,
      "name": "action_text",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
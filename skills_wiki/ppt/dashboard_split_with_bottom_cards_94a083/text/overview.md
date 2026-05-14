# Dashboard Split with Bottom Cards

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the complex dashboard layout into a reusable split structure with a hero graphic, prominent metric cards, and optional supporting details.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/dashboard_split_with_bottom_cards_94a083/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+left-image+right-metrics+bottom-bullets"
    ],
    "density": "high",
    "mood": [
      "corporate",
      "technical",
      "bold"
    ],
    "slide_role": [
      "metric_dashboard",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "professional_geometric_overlay_title_f9691f73"
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
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": "4:3",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "metric_cards",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bottom_bullets",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
# Metric Dashboard Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A split layout mapping a headline and two detailed metric items (with decorative progress bars) to the left column, balanced by a prominent hero image on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/metric_dashboard_split_3e3228/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+2-metrics+hero-image"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "cool"
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
      "video_id": "minimalist_rule_of_thirds_data_storytell_e27747df"
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
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 2,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "metrics",
      "required": true,
      "style": null
    },
    {
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
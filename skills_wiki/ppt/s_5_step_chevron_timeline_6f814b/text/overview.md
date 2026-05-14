# 5-Step Chevron Timeline

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses interlocking pentagon and chevron shapes to create a continuous horizontal sequence, ideal for 5-step processes.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/5_step_chevron_timeline_6f814b/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "5 interlocking chevron columns"
    ],
    "density": "medium",
    "mood": [
      "bold",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "timeline_horizontal",
      "feature_grid"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "sequential_chevron_tabs_accordion_proces_8db5d1da"
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
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "steps",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
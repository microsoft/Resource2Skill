# Perspective Grid Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the perspective grid motif and floating label into a stylized, animated section divider.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/perspective_grid_divider_ab7005/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "perspective-grid+label"
    ],
    "density": "low",
    "mood": [
      "technical",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "section_divider",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "retro_futuristic_flight_perspective_grid_62e4eb2c"
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
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title"
    }
  ],
  "status": "candidate"
}
```
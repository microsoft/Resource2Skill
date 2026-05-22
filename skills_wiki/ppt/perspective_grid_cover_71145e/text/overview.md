# Perspective Grid Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Extracts the split-horizon perspective drawing into a stylized cover slide with a geometric background.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/perspective_grid_cover_71145e/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "split-background-perspective"
    ],
    "density": "low",
    "mood": [
      "playful",
      "technical",
      "bold"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "retro_futuristic_flight_perspective_grid_62e4eb2c"
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
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
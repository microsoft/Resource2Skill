# Two Circles Comparison

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the two distinct circles into a minimal comparison layout, adding optional text slots inside them to make the shell reusable for abstract concepts.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_circles_comparison_41ff78/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "two-circles"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "playful"
    ],
    "slide_role": [
      "comparison_split"
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
      "max_chars": 20,
      "name": "left_text",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "right_text",
      "required": false,
      "style": "title"
    }
  ],
  "status": "active"
}
```
# 8-Segment Wheel with CTA

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the 8-segment circular diagram and bottom CTA button into a reusable wheel layout, using MSO_SHAPE.PIE with thick borders to create the segmented gaps.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/8_segment_wheel_with_cta_20fffd/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "wheel+button"
    ],
    "density": "low",
    "mood": [
      "bold",
      "playful",
      "corporate"
    ],
    "slide_role": [
      "feature_grid",
      "closing"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "exploded_segmented_process_wheel_f994d439"
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
      "bullet_capacity": 8,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "wheel_items",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "call_to_action",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "candidate"
}
```
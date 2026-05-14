# Two Object Comparison

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The slide displays two distinct objects spaced apart horizontally, suggesting a comparison or state-change layout. Extracted as a split layout with two image slots and optional labels.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_object_comparison_10276b/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "two-images-with-labels"
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
      "video_id": "custom_motion_path_animation_visualizati_a31dbf79"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_left",
      "required": true,
      "style": null
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_right",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "label_left",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "label_right",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
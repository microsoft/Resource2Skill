# Centered Ring Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the central circular graphic and vertical line from the image into a bold, minimalist section divider with centered text.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_ring_divider_cd858b/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "centered-ring-with-text"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "minimal"
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
      "video_id": "segmented_radial_infographic_precision_d_9c5077e4"
    }
  },
  "quality": {
    "contrast_ok": true,
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
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 80,
      "name": "subtitle",
      "required": false,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
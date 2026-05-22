# Central Card Divider

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A minimal central card layout with a distinct top accent band, suitable for bold section dividers or covers.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/central_card_divider_ef8617/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "central-card-with-top-band"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "bold",
      "playful"
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
      "video_id": "3d_isometric_staged_foundation_e9811cde"
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
      "max_chars": 60,
      "name": "headline",
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
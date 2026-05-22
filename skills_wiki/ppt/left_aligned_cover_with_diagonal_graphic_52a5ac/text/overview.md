# Left Aligned Cover with Diagonal Graphic

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a bold, left-aligned cover layout with a dynamic diagonal background element, suitable for high-impact intros.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_aligned_cover_with_diagonal_graphic_52a5ac/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+subtitle"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "modern_diagonal_split_hero_layout_e3e352f8"
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
      "max_chars": 60,
      "name": "subhead",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
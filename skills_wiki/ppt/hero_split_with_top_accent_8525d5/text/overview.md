# Hero Split with Top Accent

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A high-impact split layout featuring a large title anchored in the lower left, a prominent hero image on the right, and a bold top-edge accent block for visual interest.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_split_with_top_accent_8525d5/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "left-title-right-image"
    ],
    "density": "low",
    "mood": [
      "playful",
      "bold",
      "editorial"
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
      "video_id": "cosmic_quiz_layout_sequential_reveal_sta_591baf31"
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
      "aspect": "1:1",
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
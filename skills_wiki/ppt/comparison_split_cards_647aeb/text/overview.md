# Comparison Split Cards

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses two large side-by-side panels to compare two concepts or designs, with the right panel highlighted using the accent color to simulate a 'before/after' or 'A/B' comparison.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/comparison_split_cards_647aeb/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column-cards"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "editorial"
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
      "video_id": "cinematic_picture_in_picture_reveal_85c03192"
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
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "left_headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "left_subhead",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "right_headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "right_subhead",
      "required": false,
      "style": "subtitle"
    }
  ],
  "status": "active"
}
```
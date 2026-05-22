# Simple Bullet List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A classic title and single-column bulleted list layout. Bullets are rendered as separate text boxes to perfectly replicate the sequential entrance animation shown in the source image's animation pane.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/simple_bullet_list_b0ece3/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+bullet-list"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate"
    ],
    "slide_role": [
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "progressive_hierarchical_reveal_sequenti_d03419c7"
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
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 7,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": "body"
    }
  ],
  "status": "active"
}
```
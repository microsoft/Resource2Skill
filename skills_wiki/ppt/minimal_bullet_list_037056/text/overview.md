# Minimal Bullet List

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a minimal presenter view with a single bullet point appearing. This translates to a clean, low-density vertical bullet list layout with an optional title.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/minimal_bullet_list_037056/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+vertical-bullets"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "technical"
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
      "bullet_capacity": 6,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
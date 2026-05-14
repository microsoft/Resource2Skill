# 2x2 Agenda Grid

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A classic 2x2 grid layout for an agenda or table of contents, featuring prominent numbered badges for clear section delineation.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/2x2_agenda_grid_4b4b5f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+2x2-numbered-list"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "warm",
      "corporate"
    ],
    "slide_role": [
      "agenda"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "organic_grid_reveal_sequence_8ed51df6"
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
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "agenda_items",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
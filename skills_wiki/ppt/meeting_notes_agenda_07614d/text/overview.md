# Meeting Notes Agenda

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A high-density text layout suitable for meeting notes or detailed agendas, featuring a meta-information block and a structured list of points.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/meeting_notes_agenda_07614d/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "header+meta+bullets"
    ],
    "density": "high",
    "mood": [
      "corporate",
      "minimal",
      "editorial"
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
      "video_id": "architectural_minimalist_chapter_title_b0e88c72"
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
      "max_chars": 100,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "meta_info",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "content_title",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": 8,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
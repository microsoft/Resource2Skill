# Circular Agenda Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses overlapping geometric circles to create a dynamic left-side focal point, balanced by a structured right-side agenda list with a pill-shaped section number.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/circular_agenda_split_ac6ba0/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "overlapping-circles + right-list"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "playful",
      "bold"
    ],
    "slide_role": [
      "agenda",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "dynamic_circular_split_layout_d3525024"
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
      "max_chars": 50,
      "name": "kicker",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": "1:1",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": false,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "main_title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 5,
      "name": "section_number",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "section_title",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": 6,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "bullets",
      "required": true,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
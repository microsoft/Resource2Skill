# Vertical Node Agenda

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the bold, split-layout agenda with a vertical connecting line and numbered nodes.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_node_agenda_8346d6/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+vertical-nodes"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "bold",
      "minimal"
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
      "video_id": "connected_vertical_flow_agenda_30ff079b"
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
      "max_chars": 30,
      "name": "title",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
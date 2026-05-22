# Vision Overview Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses a central magnifying glass graphic with opposing speech bubbles to present a vision or conceptual overview.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vision_overview_split_de4445/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+two-callouts+graphic"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "playful"
    ],
    "slide_role": [
      "section_divider",
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "monochrome_corporate_node_panels_230454dd"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 60,
      "name": "subtitle",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "callout_left",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "callout_right",
      "required": false,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
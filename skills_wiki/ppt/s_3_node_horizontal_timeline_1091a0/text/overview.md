# 3-Node Horizontal Timeline

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracts the minimal horizontal 3-node timeline structure with a connecting line, accent nodes, and drop-down text areas.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/3_node_horizontal_timeline_1091a0/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "timeline+3-nodes"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "technical"
    ],
    "slide_role": [
      "timeline_horizontal"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "neon_cyberpunk_alternating_timeline_015c752d"
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
      "max_chars": 30,
      "name": "kicker",
      "required": false,
      "style": "caption"
    },
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
      "bullet_capacity": 3,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "timeline_items",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
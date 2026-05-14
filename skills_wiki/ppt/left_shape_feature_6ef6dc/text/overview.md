# Left Shape Feature

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extrapolated a minimal feature/divider slide from the single circle graphic, adding text slots to make it a functional layout.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/left_shape_feature_6ef6dc/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "shape+text"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "technical"
    ],
    "slide_role": [
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "sleek_process_flow_diagramming_d72f66d9"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
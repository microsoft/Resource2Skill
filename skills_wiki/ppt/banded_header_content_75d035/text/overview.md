# Banded Header Content

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted the prominent banded header structure (thick banner flanked by thin lines) to create a versatile, corporate content slide with a strong top anchor.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/banded_header_content_75d035/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+body"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "minimal",
      "cool"
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
      "video_id": "corporate_flow_master_template_46f97206"
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
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 500,
      "name": "body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
# Vertical Split Window

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Interpreted the drawn 'window' shape as a central comparison or feature card split vertically into top and bottom content areas.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_split_window_53c77c/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "headline + vertically split central card"
    ],
    "density": "low",
    "mood": [
      "minimal",
      "corporate",
      "bold"
    ],
    "slide_role": [
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "3d_morphing_reveal_window_spatial_narrat_bdaa833a"
    }
  },
  "quality": {
    "contrast_ok": true,
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "top_title",
      "required": true,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "top_body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "bottom_title",
      "required": true,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 150,
      "name": "bottom_body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
# Media Showcase with Caption

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Extracts the video tutorial layout into a generic media showcase with a top-left brand label, a large central media area, and an overlaid caption box.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/media_showcase_with_caption_383678/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "media+caption"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "minimal",
      "technical"
    ],
    "slide_role": [
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "seamless_device_mockup_integration_80865a4f"
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
      "max_chars": 40,
      "name": "brand",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "media",
      "required": true,
      "style": null
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "caption",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
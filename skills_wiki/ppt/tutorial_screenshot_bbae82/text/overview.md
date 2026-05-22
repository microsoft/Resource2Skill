# Tutorial Screenshot

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A simple layout for displaying a large screenshot or image, typical for software tutorials, with optional headline and caption.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/tutorial_screenshot_bbae82/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "image-only"
    ],
    "density": "low",
    "mood": [
      "technical",
      "minimal"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "realistic_typewriter_rhythm_morph_frame__44d189cb"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": "16:9",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
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
      "style": "caption"
    }
  ],
  "status": "active"
}
```
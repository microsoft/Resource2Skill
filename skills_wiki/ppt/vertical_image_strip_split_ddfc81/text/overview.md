# Vertical Image Strip Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A split layout with a prominent text area on the left and a vertical strip of four images on the right, ideal for team introductions or feature highlights.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/vertical_image_strip_split_ddfc81/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "text+4-image-column"
    ],
    "density": "medium",
    "mood": [
      "editorial",
      "corporate",
      "minimal"
    ],
    "slide_role": [
      "feature_grid",
      "cover"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "vertical_morphing_carousel_profile_deck_1b156b00"
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
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 200,
      "name": "body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "square",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_1",
      "required": false,
      "style": null
    },
    {
      "aspect": "square",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_2",
      "required": false,
      "style": null
    },
    {
      "aspect": "square",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_3",
      "required": false,
      "style": null
    },
    {
      "aspect": "square",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "image_4",
      "required": false,
      "style": null
    }
  ],
  "status": "active"
}
```
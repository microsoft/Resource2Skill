# Hero Overlap Block

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold, editorial layout featuring a large horizontal accent block overlapped by a portrait hero image, with text embedded inside the block.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/hero_overlap_block_2cd4a5/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-image+text-block"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "editorial"
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
      "video_id": "3d_out_of_bounds_profile_card_3d_32551940"
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
      "max_chars": 120,
      "name": "subhead",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "portrait",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "hero_image",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
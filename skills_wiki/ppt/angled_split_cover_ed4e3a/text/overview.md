# Angled Split Cover

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Uses large rotated rectangles to create a dynamic angled split, balancing bold geometric accents with clean typography.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/angled_split_cover_ed4e3a/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "angled-split+title+subtitle"
    ],
    "density": "low",
    "mood": [
      "bold",
      "corporate",
      "modern"
    ],
    "slide_role": [
      "cover",
      "section_divider"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "off_canvas_geometric_masking_4e155db3"
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
      "max_chars": 40,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "subtitle",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
# Centered Split Panel

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image shows a classic centered split layout with a solid color block on the left (likely for text) and an image on the right, forming a cohesive, floating rectangular unit.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_split_panel_7deb94/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "split-panel"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "bold",
      "minimal"
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
      "video_id": "custom_freeform_image_masking_silhouette_1cce09f4"
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
      "max_chars": 150,
      "name": "body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "landscape",
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
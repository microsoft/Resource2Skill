# Tech Hero Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A bold, low-density hero layout with a massive left-aligned headline and right-aligned secondary content, suitable for covers or major section transitions.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/tech_hero_split_c3251e/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "hero-text+right-cta"
    ],
    "density": "low",
    "mood": [
      "bold",
      "technical",
      "cool"
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
      "video_id": "editorial_product_hero_typography_rings_c4483ca5"
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
      "max_chars": 20,
      "name": "logo",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "top_right_nav",
      "required": false,
      "style": "caption"
    },
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
      "max_chars": 100,
      "name": "subhead",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "cta",
      "required": false,
      "style": "body_bold"
    }
  ],
  "status": "active"
}
```
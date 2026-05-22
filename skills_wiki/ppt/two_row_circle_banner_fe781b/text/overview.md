# Two Row Circle Banner

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The layout features two distinct horizontal items, each composed of a prominent circular label overlapping a rectangular content banner. A single 'rows' bullet_list slot perfectly captures this structure, mapping the title to the circle and the body to the banner.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_row_circle_banner_fe781b/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2 rows with circle labels and bullet banners"
    ],
    "density": "low",
    "mood": [
      "corporate",
      "playful",
      "bold"
    ],
    "slide_role": [
      "bullet_card_list",
      "feature_grid"
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
    "overlap_ok": false,
    "render_ok": true,
    "usage_count": 0
  },
  "skill_type": "shell",
  "slots": [
    {
      "aspect": null,
      "bullet_capacity": 2,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "rows",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
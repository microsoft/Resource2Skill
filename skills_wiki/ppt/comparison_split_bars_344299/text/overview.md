# Comparison Split Bars

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "A central-axis comparison layout using horizontal bars extending outwards to contrast two products across multiple metrics.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/comparison_split_bars_344299/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+split-bars"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "technical",
      "cool"
    ],
    "slide_role": [
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "symmetrical_divergent_comparison_dashboa_414e8892"
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
      "max_chars": 30,
      "name": "product_a_name",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "product_a_desc",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "product_b_name",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 100,
      "name": "product_b_desc",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "metrics",
      "required": true,
      "style": null
    }
  ],
  "status": "candidate"
}
```
# Comparison Split

## Parameters

```json
{
  "_distill_attempts": 3,
  "_distill_reasoning": "Uses a central spine and mirrored horizontal pill-shaped bars to create a clear, structured visual comparison between two products, strictly adhering to theme colors.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/comparison_split_2e840c/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "title+2-column-comparison"
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
    "confidence": 0.6499999999999999,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "symmetrical_divergent_comparison_dashboa_414e8892"
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
      "max_chars": 60,
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
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "product_a_desc",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "product_b_name",
      "required": true,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "product_b_desc",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "item_schema": {
        "label": "the dimension being compared (≤25 chars, e.g. 'Latency', 'Supervision')",
        "val_a": "product A's position on this dimension (≤40 chars)",
        "val_b": "product B's position on this dimension (≤40 chars)"
      },
      "kind": "bullet_list",
      "max_chars": null,
      "name": "features",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
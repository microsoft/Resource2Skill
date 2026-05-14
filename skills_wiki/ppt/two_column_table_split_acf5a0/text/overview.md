# Two Column Table Split

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "The image displays a wireframe of a two-column table or split layout, ideal for comparisons or side-by-side lists.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/two_column_table_split_acf5a0/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column-table"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "minimal",
      "technical"
    ],
    "slide_role": [
      "comparison_split"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "cross_functional_swimlane_flowchart_7fed1fa0"
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
      "required": false,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "left_title",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "left_body",
      "required": false,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "right_title",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "right_body",
      "required": false,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
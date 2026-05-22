# Window Pane Comparison

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Abstracts the literal double-door graphic into a functional 2-column comparison layout, using the window panes as distinct title and body text containers.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/window_pane_comparison_a8144d/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column-split-panes"
    ],
    "density": "medium",
    "mood": [
      "playful",
      "corporate",
      "bold"
    ],
    "slide_role": [
      "comparison_split",
      "feature_grid"
    ]
  },
  "provenance": {
    "confidence": 0.85,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "3d_morphing_reveal_window_spatial_narrat_bdaa833a"
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
      "aspect": null,
      "bullet_capacity": 2,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "items",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
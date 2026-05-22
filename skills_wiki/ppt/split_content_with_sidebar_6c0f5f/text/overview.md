# Split Content with Sidebar

## Parameters

```json
{
  "_distill_attempts": 2,
  "_distill_reasoning": "Extracts the 3-column split layout (title/lead, bullets, sidebar) using a colored panel to group the primary content, strictly adhering to palette_color for all fills.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/split_content_with_sidebar_6c0f5f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "2-column-panel+sidebar"
    ],
    "density": "high",
    "mood": [
      "corporate",
      "editorial",
      "technical"
    ],
    "slide_role": [
      "comparison_split",
      "bullet_card_list"
    ]
  },
  "provenance": {
    "confidence": 0.75,
    "distilled_by": "gemini-3.1-pro-preview@distill_shell",
    "source": {
      "timestamp": null,
      "type": "youtube",
      "video_id": "programmatic_sidebar_pagination_text_flo_95db2daf"
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
      "required": true,
      "style": "title"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "lead_text",
      "required": false,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": 4,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "main_bullets",
      "required": true,
      "style": "body"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 40,
      "name": "sidebar_title",
      "required": false,
      "style": "subtitle"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "sidebar_text",
      "required": false,
      "style": "body"
    }
  ],
  "status": "active"
}
```
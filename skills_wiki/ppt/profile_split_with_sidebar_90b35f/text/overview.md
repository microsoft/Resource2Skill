# Profile Split with Sidebar

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Extracted a 3-column profile layout featuring a sidebar for roles, a staggered large typography section for the name, and a hero image on the right.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/profile_split_with_sidebar_90b35f/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "profile-split-with-sidebar"
    ],
    "density": "medium",
    "mood": [
      "corporate",
      "bold",
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
      "video_id": "vertical_morphing_carousel_profile_deck_1b156b00"
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
      "max_chars": 20,
      "name": "first_name",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 20,
      "name": "last_name",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 30,
      "name": "primary_role",
      "required": true,
      "style": "body_bold"
    },
    {
      "aspect": null,
      "bullet_capacity": 5,
      "kind": "bullet_list",
      "max_chars": null,
      "name": "secondary_roles",
      "required": false,
      "style": "caption"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 300,
      "name": "bio",
      "required": false,
      "style": "body"
    },
    {
      "aspect": "9:16",
      "bullet_capacity": null,
      "kind": "image",
      "max_chars": null,
      "name": "photo",
      "required": true,
      "style": null
    }
  ],
  "status": "active"
}
```
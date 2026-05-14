# Wavy Ribbon Split Cover

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "Uses rotated WAVE shapes to ingeniously recreate the dynamic, layered 3D ribbon split seen in the background tutorial, providing a striking left-aligned cover layout.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/wavy_ribbon_split_cover_f3b7c4/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "split-wave-text-left"
    ],
    "density": "low",
    "mood": [
      "bold",
      "playful",
      "editorial",
      "corporate"
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
      "video_id": "animated_paper_fold_reveal_transition_769baf7e"
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
      "max_chars": 60,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    },
    {
      "aspect": null,
      "bullet_capacity": null,
      "kind": "text",
      "max_chars": 120,
      "name": "subhead",
      "required": false,
      "style": "body"
    }
  ],
  "status": "candidate"
}
```
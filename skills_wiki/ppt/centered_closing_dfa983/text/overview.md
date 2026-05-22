# Centered Closing

## Parameters

```json
{
  "_distill_attempts": 1,
  "_distill_reasoning": "A highly minimal layout focusing entirely on a single, large, centered message, typical for closing or transition slides.",
  "implementation": {
    "code_path": "skills_library/ppt/shells_distilled/centered_closing_dfa983/render.py",
    "entrypoint": "render(slide, slots, theme)"
  },
  "intent_tags": {
    "compatible_themes": [],
    "content_shape": [
      "centered-text"
    ],
    "density": "low",
    "mood": [
      "bold",
      "minimal"
    ],
    "slide_role": [
      "closing",
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
      "max_chars": 50,
      "name": "headline",
      "required": true,
      "style": "title_xl"
    }
  ],
  "status": "active"
}
```
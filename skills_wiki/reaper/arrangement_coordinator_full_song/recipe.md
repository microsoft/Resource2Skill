# Recipe: Full-Song Arrangement Coordinator

- skill_id: `arrangement_coordinator_full_song`
- confidence: `source-reported`
- reproducibility: `snippet`

## Mechanism

Run this first for full-song briefs with drums, bass, chords, lead, and pad.
It creates the project spine: intro, verse, chorus, variation, and outro. Use
detail skills afterward only to enrich compatible roles.

## Composable Snippet

```python
apply_skill(
    skill_id="arrangement_coordinator_full_song",
    target_id="project",
    kwargs_json='{"bpm": 124, "key": "D", "scale": "minor", "bars": 36, "genre": "cinematic"}'
)
```

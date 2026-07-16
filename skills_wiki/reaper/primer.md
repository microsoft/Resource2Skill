# Reaper Wiki Primer

Use skills as musical roles inside one project context. Prefer one exact-match
T5 coordinator, then add focused T3/T4 detail skills only when they do not
conflict with the brief.

## Canonical Coordinators

| User need | Canonical skill |
|---|---|
| Ambient / cinematic / no drums / slow drone / sparse piano | `ambient_cinematic_no_drums_coordinator` |
| Lo-fi study beat / Nujabes / J Dilla / warm Rhodes / boom-bap | `lofi_study_beat_coordinator` |
| Future bass / melodic bass / supersaw drop / 808 / vocal chops | `future_bass_drop_coordinator` |
| General full-song scaffold with drums, bass, chords, lead, pad | `arrangement_coordinator_full_song` |

## Composition Rules

1. If the brief says `NO drums`, never apply drum, snare-roll, trap, boom-bap,
   or transient-focused skills.
2. A coordinator counts as the project spine. Add at most 1-3 compatible
   detail skills afterward.
3. Always pass the brief tempo, key, scale, and full bar count in `kwargs_json`.
4. Prefer enriching existing named roles over creating duplicate tracks.
5. Render with a style matching the genre: `lofi_hiphop` for lo-fi, `clean`
   for ambient/cinematic no-drums, `kanye_soul` for trap/808 weight when no
   better preset exists.

## Search Terms

| Role | Terms |
|---|---|
| Full structure | coordinator, arrangement, song form, scaffold |
| Ambient | ambient, drone, pad, no_drums, cinematic, slow_evolution |
| Lo-fi | lofi, study, Rhodes, boom_bap, vinyl, warm_mix |
| Bass | sub, 808, walking_bass, cello_bass, low_end |
| Mix | EQ, compressor, reverb, sidechain, spectrum |

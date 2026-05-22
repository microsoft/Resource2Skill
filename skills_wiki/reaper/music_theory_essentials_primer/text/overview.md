# Music Theory & Mix-Engineering Essentials

A foundational reference for building tracks programmatically. Use these tables to compute MIDI pitches, pick chord voicings, place drum hits on the GM map, choose tempos, and build per-element FX chains.

## Render style picker — IMPORTANT

`render_project(style=...)` accepts these styles. Pick the one that matches the brief's genre — getting this right is worth ~0.5–1 point on `overall_mix` and `low_end_balance`:

| Brief mentions… | Pass `style=` | What it does |
|---|---|---|
| lo-fi, lofi, jazzy hip-hop, dusty drums, neo-soul lo-fi | `lofi_hiphop` | Heavy vinyl crackle, low-pass filter, gentle saturation, warm bottom |
| Kanye, soulful, sample-flip, chipmunk soul, 808s & soul | `kanye_soul` | Tape saturation, vinyl, bass boost, classic soul EQ curve |
| synthwave, retrowave, 80s, neon, cyberpunk synth | `synthwave` | Stereo widen, tape, bright high-end, gated reverb feel |
| trap, drill, modern hip-hop with hi-hats rolls | `kanye_soul` | (closest fit — gives 808 weight) |
| house, deep house, four-on-floor club | `clean` | Light saturation only — preserves transients |
| techno, minimal, hypnotic | `clean` | |
| ambient, cinematic, calm, no-drums | `clean` | |
| anything else / unsure | `auto` | Auto-detects from track names |

**Wrong style choice is the #1 mix-quality footgun**. A clean lo-fi beat passed as `style="clean"` will sound thin; a deep house track passed as `style="lofi_hiphop"` will sound muffled.

## Skill leverage rule

Use `apply_skill` × ≥3 covering distinct musical roles. The recipes are where competitive edge over a from-scratch baseline comes from — without them you're writing generic MIDI like everyone else. Read the full recipe (BPM / key / chord progression / arrangement structure / dynamics) and translate it FAITHFULLY into your `add_midi_notes` calls. Generic C-Am-F-G is the loss condition.

## Scale → MIDI Pitch Lookup

```python
NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

SCALES = {
    "major":            [0, 2, 4, 5, 7, 9, 11],
    "minor":            [0, 2, 3, 5, 7, 8, 10],          # natural minor
    "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor":    [0, 2, 3, 5, 7, 9, 11],
    "dorian":           [0, 2, 3, 5, 7, 9, 10],
    "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    "lydian":           [0, 2, 4, 6, 7, 9, 11],
    "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues":            [0, 3, 5, 6, 7, 10],
}

# MIDI pitch formula:
#   pitch = (octave + 1) * 12 + NOTE_MAP[root_note] + scale_intervals[degree]
# Reference octaves: C4 (middle C) = 60, A4 (concert pitch) = 69, C5 = 72.
# Bass register: octaves 1-2.   Pad register: 3-4.   Lead register: 4-6.
```

## Common Chord Voicings (intervals from root)

```python
CHORDS = {
    "major":   [0, 4, 7],          # I, IV, V in major
    "minor":   [0, 3, 7],          # ii, iii, vi in major / i, iv, v in minor
    "maj7":    [0, 4, 7, 11],      # jazzy, lush
    "min7":    [0, 3, 7, 10],      # neo-soul, lo-fi
    "dom7":    [0, 4, 7, 10],      # blues, funk
    "min9":    [0, 3, 7, 10, 14],  # extended neo-soul
    "maj9":    [0, 4, 7, 11, 14],  # cinematic warmth
    "sus2":    [0, 2, 7],          # ambient, suspended
    "sus4":    [0, 5, 7],          # tension before resolution
    "dim":     [0, 3, 6],          # transitional, half-step movement
    "dim7":    [0, 3, 6, 9],
    "aug":     [0, 4, 8],          # rising tension
    "add9":    [0, 4, 7, 14],      # bright pop
}
```

### Useful chord progressions by mood

- **Sad / introspective lo-fi**: `i — VI — III — VII` (e.g. Am – F – C – G)
- **Soulful neo-soul**: `Imaj7 — vi7 — iimin7 — V7` (e.g. Cmaj7 – Am7 – Dm7 – G7)
- **Synthwave / retrowave**: `i — VII — VI — VII` (e.g. Am – G – F – G)
- **House / four-on-floor**: `i — III — VII — VI` (e.g. Am – C – G – F)
- **Trap / cinematic**: hold one minor chord with bass-octave jumps for tension
- **Boom-bap / hip-hop**: looped `ii7 — V7 — Imaj7` (e.g. Dm7 – G7 – Cmaj7)
- **Drum & bass**: `i — VII` repeated, with rhythmic bass riffs in pentatonic_minor

## General MIDI Program Numbers (`create_track(program=...)`)

When creating non-drum tracks, pass the GM program that matches the brief's instrument. Common picks:

| Program | Instrument | Use for |
|---|---|---|
| 0 | Acoustic Grand Piano | Classical, ballads, neo-soul Rhodes substitute |
| 4 | Electric Piano (Rhodes) | Lo-fi, jazz, neo-soul, R&B |
| 6 | Harpsichord | Cinematic, baroque-flavored |
| 11 | Vibraphone | Lo-fi, jazz, ambient |
| 25 | Steel Acoustic Guitar | Folk, indie |
| 27 | Clean Electric Guitar | Pop, funk |
| 32 | Acoustic Bass | Jazz, classical |
| 33 | Electric Finger Bass | Funk, R&B, pop |
| 38 | Synth Bass 1 | House, techno, synthwave, trap 808 |
| 39 | Synth Bass 2 | Cyberpunk, deep house |
| 48 | String Ensemble | Cinematic, ambient |
| 56 | Trumpet | Jazz, soul |
| 60 | French Horn | Cinematic, orchestral |
| 73 | Flute | Lo-fi, ambient, world |
| 80 | Square Lead (synth) | Synthwave, retro, chiptune |
| 81 | Saw Lead (synth) | Synthwave, EDM lead |
| 84 | Charang Lead | Trance, leads |
| 88 | New-Age Pad (Fantasia) | Ambient, cinematic |
| 89 | Warm Pad | Synthwave, cinematic, ambient |
| 91 | Polysynth Pad | House, techno, cinematic |
| 95 | Sweep Pad | Transitions, ambient |

For drums, pass `is_drum=True` and write notes into the GM drum map (above) — the `program` argument is ignored.

## Standard Drum Map (General MIDI)

```python
DRUMS = {
    "kick":       36,  # C2 — main downbeat
    "kick_alt":   35,  # B1 — softer/sub kick
    "snare":      38,  # D2 — backbeat (2 and 4)
    "snare_alt":  40,  # E2 — sidestick / electronic
    "rim":        37,  # C#2
    "clap":       39,  # D#2 — layered with snare
    "closed_hh":  42,  # F#2 — 8th- or 16th-note grid
    "pedal_hh":   44,  # G#2
    "open_hh":    46,  # A#2 — accents on offbeats
    "crash":      49,  # C#3 — section starts
    "ride":       51,  # D#3 — alternative to hi-hat
    "tom_low":    45,  # A2
    "tom_mid":    47,  # B2
    "tom_high":   50,  # D3
    "shaker":     70,  # A#4 — texture
    "tambourine": 54,  # F#3
}
```

### Common rhythm grids (1 bar = 16 sixteenth-notes)

- **Boom-bap kick**: `[1,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,1,0]`
- **Trap kick**: `[1,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,0]` plus 808 fills
- **Four-on-floor (house/techno)**: `[1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]`
- **Snare backbeat**: `[0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0]`
- **Lo-fi closed hi-hat (16ths with swing)**: every 2nd sixteenth, lighter on the &-of-2/4

## Genre BPM Ranges

| Genre | BPM | Notes |
|---|---|---|
| Lo-fi hip-hop | 70–90 | Often half-time feel; swung 16ths |
| Boom-bap | 85–100 | Straight grid, dusty drums |
| Chipmunk soul | 88–98 | Pitched-up vocal samples, Kanye-style |
| Trap | 130–170 | Half-time hi-hats; rolls and triplets |
| House | 120–130 | Four-on-floor; off-beat open hat |
| Techno | 125–140 | Sparse arrangements, hypnotic |
| Drum & Bass | 170–180 | Half-time feel often |
| Synthwave / retrowave | 100–120 | Gated reverb snare, arpeggios |
| Ambient | 60–100 | Sometimes no drums at all |
| Pop | 95–120 | Hook-driven structure |
| Cinematic / film | 60–110 | Tempo changes welcome |

## FX Chains by Element

Per-track signal chain (left = first plugin, right = last):

```
Kick:    ReaEQ (HP 30Hz, boost 60Hz, cut 200-400Hz mud) → ReaComp (fast attack, 4:1) → ReaLimit
Snare:   ReaEQ (HP 100Hz, boost 5kHz crack) → ReaComp (medium attack, 3:1) → ReaVerb (small room)
Hi-hat:  ReaEQ (HP 200Hz, gentle high-shelf) → ReaComp (slow attack, 2:1)
Bass:    ReaSynth → ReaEQ (LP 300Hz, boost 60-80Hz) → ReaComp (medium attack, 4:1)
Sub-bass: ReaSynth (sine) → ReaEQ (HP 30Hz, LP 100Hz) → ReaLimit (no compression)
Chords:  ReaSynth → ReaEQ (cut <200Hz, gentle high-shelf) → ReaDelay (1/8 note, low-pass on returns) → ReaVerb (large hall, 30% wet)
Lead:    ReaSynth → ReaEQ (presence boost 2-5kHz) → ReaDelay (1/4 dotted, ping-pong) → ReaVerb (plate, 20% wet)
Pad:     ReaSynth → ReaEQ (gentle low-shelf cut) → ReaVerb (large hall, 50% wet) → ReaComp (slow attack, glue)
Master:  ReaEQ (surgical cuts only) → ReaComp (1.5:1 glue, slow attack) → ReaLimit (-1 dB ceiling)
```

### Mix discipline rules

1. **Frequency separation**: bass owns 30–200 Hz, kick 60–80 Hz peak, drums mid-range presence, chords 200–2000 Hz, melody 1–8 kHz, air >8 kHz.
2. **Side-chain when needed**: kick + sub-bass should not fight — duck the sub by ~3 dB on each kick hit.
3. **Reverb on a send, not insert**: long verbs go on a return track so multiple elements share the same space.
4. **No element peaks above -6 dBFS pre-master**: leaves headroom for the master bus.
5. **Stereo image**: keep low-end (bass + kick) mono, spread chords/leads/pads.

## Composition Patterns That Score Well

- **Strong low-end separation + clear drum transients + balanced spectrum + noticeable section changes/dropouts.** This is the clearest high-score formula.
- **Warm full-spectrum mix with punchy rhythmic backbone** wins even when harmonic richness is moderate, as long as no obvious frequency gap.
- Tracks with **dynamic movement** (verse→drop, filter sweeps, mute/unmute) score better than uniform loops.
- 32+ bar arrangements (intro 4 + verse 8 + chorus 8 + variation 8 + outro 4) outperform a single 8-bar loop on `arrangement_dynamics`.

## Recommended Skill Combos

- **lofi hip-hop beat**: 5 skills covering low_end_balance, kick_bass_separation, drum_transient_design, arrangement_variation, harmonic_layering
- **chipmunk soul beat**: 5 skills covering sample_harmonic_control, warm_full_spectrum_mixing, drum_punch, section_contrast, top_end_air
- **synthwave / retrowave beat**: 5 skills covering bass_foundation, rhythmic_consistency, synth_harmonic_richness, dynamic_arrangement, stereo_or_frequency_separation
- **general beat demo**: 4 skills covering low_end_control, transient_clarity, full_spectrum_balance, arrangement_development

## How to apply this primer

1. Pick the genre → look up the BPM and `set_tempo`.
2. Pick the key + scale → derive `scale_intervals` from `SCALES`.
3. Pick a chord progression appropriate for the mood (above) → translate to MIDI via `NOTE_MAP[root] + (octave+1)*12 + chord_intervals`.
4. Lay drums on the GM map using a rhythm grid for the genre.
5. Add bass following the chord progression, one octave below the chord roots.
6. Add melody / lead in the upper register from the same scale.
7. Build sections (intro / verse / chorus / variation / outro).
8. Apply FX chains per element from the table above.
9. Render and review.

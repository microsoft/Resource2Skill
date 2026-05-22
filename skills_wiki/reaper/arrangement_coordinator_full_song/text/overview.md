# Full-Song Arrangement Coordinator

A foundational scaffolding skill. Run this **first**, before any pattern-level skills. It produces a complete 32-bar multi-section song with 5 standard tracks, per-section dynamics, and coordinated FX — analogous to how PPT's structural skills (cover, dividers, closing) lay down the deck spine before content slides fill in.

## What this skill creates

- **5 tracks** (only created if not already present — additive):
  - `Drums` (GM channel 10)
  - `Sub Bass` (GM program 38, finger bass)
  - `Chords` (GM program 4, electric piano)
  - `Lead` (GM program varies by genre)
  - `Pad` (GM program 89, warm pad)

- **5-section, 32-bar structure** (intro 4 + verse 8 + chorus 8 + variation 8 + outro 4):
  - Intro: drums sparse, pad sustained, bass holds root
  - Verse: drums full, bass root-fifth, chords main progression, lead absent
  - Chorus: drums + crash, bass octave-doubled, chords inverted, lead melody enters
  - Variation: drums different feel (e.g. half-time), chord substitution, lead sparse
  - Outro: subtractive, sustained chord, fade-friendly

- **Coordinated FX chain** per track (see primer's per-element table)

- **Tempo and time-signature** set from kwargs

## When NOT to use this skill

- If the brief is a single-instrument piece (solo piano, ambient drone) — use a pattern skill directly
- If the brief is < 16 bars (too short to need full song form)

## How other skills layer on top

After this scaffold runs, subsequent `apply_skill` calls should *enrich* rather than *replace*. For example:
- `boom_bap_drum_pattern` → adds nuance to existing `Drums` track (does not create new "Drums 2")
- `acid_bassline` → replaces or layers on `Sub Bass` track
- `chord_voicings_skill` → can adjust `Chords` track inversions

The agent should call exactly this coordinator + 1-2 detail skills. More than that creates conflicts.

## 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "ArrangementScaffold",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 32,
    genre: str = "general",  # "lofi", "synthwave", "house", "trap", "ambient", or "general"
    **kwargs,
) -> str:
    """Build a 32-bar 5-track multi-section arrangement scaffold."""
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    DRUMS = {"kick": 36, "snare": 38, "clap": 39, "closed_hh": 42,
             "open_hh": 46, "crash": 49, "ride": 51, "tom_low": 45,
             "tom_mid": 47, "tom_high": 50}
    PROG_BY_GENRE = {
        "lofi":      {"chords": 4,  "lead": 5,  "bass": 33, "pad": 89},
        "synthwave": {"chords": 81, "lead": 80, "bass": 38, "pad": 89},
        "house":     {"chords": 4,  "lead": 80, "bass": 38, "pad": 91},
        "trap":      {"chords": 4,  "lead": 81, "bass": 38, "pad": 89},
        "ambient":   {"chords": 89, "lead": 91, "bass": 32, "pad": 89},
        "general":   {"chords": 4,  "lead": 80, "bass": 33, "pad": 89},
    }
    progs = PROG_BY_GENRE.get(genre, PROG_BY_GENRE["general"])

    root = NOTE_MAP.get(key, 0)
    intervals = SCALES.get(scale, SCALES["minor"])
    bass_oct = 36
    chord_oct = 60
    lead_oct = 72

    # i-VI-iv-v-style minor progression by default
    # Degrees of the scale: 1, 6, 4, 5
    deg = [0, 5, 3, 4]
    if scale == "major":
        deg = [0, 5, 3, 4]
    chord_roots = [intervals[d % len(intervals)] for d in deg]

    # === Set tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat = 60.0 / bpm
    bar = beat * 4
    ppq = 960.0
    bar_ppq = ppq * 4

    # === Section boundaries (in bars) ===
    intro_len = 4
    verse_len = 8
    chorus_len = 8
    var_len = 8
    outro_len = 4
    sections = [
        ("intro",     0,            intro_len),
        ("verse",     intro_len,    verse_len),
        ("chorus",    intro_len + verse_len, chorus_len),
        ("variation", intro_len + verse_len + chorus_len, var_len),
        ("outro",     intro_len + verse_len + chorus_len + var_len, outro_len),
    ]
    total_bars = intro_len + verse_len + chorus_len + var_len + outro_len

    # === Helper: ensure track by name (additive — don't duplicate) ===
    track_idx_by_name: dict[str, int] = {}
    n_existing = RPR.RPR_CountTracks(0)
    for i in range(n_existing):
        tr = RPR.RPR_GetTrack(0, i)
        # Try to read name via shim (may be empty in mock)
        result = RPR.RPR_GetTrackName(tr) if hasattr(RPR, "RPR_GetTrackName") else (0, tr, "", 256)
        if isinstance(result, tuple) and len(result) >= 3:
            name = result[2] or ""
            if name:
                track_idx_by_name[name] = i

    def ensure_track(name: str, program: int = 0, is_drum: bool = False) -> int:
        if name in track_idx_by_name:
            return track_idx_by_name[name]
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        track_idx_by_name[name] = idx
        return idx

    def add_take(track_idx: int, start_bar: int, length_bars: int):
        """Add a media item with a take to a track for given bar range. Returns take handle."""
        tr = RPR.RPR_GetTrack(0, track_idx)
        item = RPR.RPR_AddMediaItemToTrack(tr)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_bar * bar)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_bars * bar)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def insert_note(take, start_beat_in_take, len_beats, pitch, vel):
        s_ppq = start_beat_in_take * ppq
        e_ppq = s_ppq + len_beats * ppq
        RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0,
                                int(max(0, min(127, pitch))),
                                int(max(1, min(127, vel))),
                                False)

    drums_idx  = ensure_track("Drums",    program=0,                 is_drum=True)
    bass_idx   = ensure_track("Sub Bass", program=progs["bass"],     is_drum=False)
    chords_idx = ensure_track("Chords",   program=progs["chords"],   is_drum=False)
    lead_idx   = ensure_track("Lead",     program=progs["lead"],     is_drum=False)
    pad_idx    = ensure_track("Pad",      program=progs["pad"],      is_drum=False)

    # === Drums per section ===
    for sec_name, start_bar, length in sections:
        take = add_take(drums_idx, start_bar, length)
        for b in range(length):
            beat0 = b * 4  # 4 beats per bar, beats relative to take start
            if sec_name == "intro":
                # Sparse: just kick on 1, snare on 3
                insert_note(take, beat0,       0.25, DRUMS["kick"], 90)
                insert_note(take, beat0 + 2,   0.25, DRUMS["snare"], 80)
                # Light hat on offbeats
                for sub in (1, 3):
                    insert_note(take, beat0 + sub, 0.15, DRUMS["closed_hh"], 60)
            elif sec_name == "verse":
                # Standard backbeat
                insert_note(take, beat0,       0.25, DRUMS["kick"], 100)
                insert_note(take, beat0 + 2,   0.25, DRUMS["snare"], 100)
                # Sixteenth-note hi-hat
                for s in range(8):
                    vel = 75 if s % 2 == 0 else 60
                    insert_note(take, beat0 + s * 0.5, 0.1, DRUMS["closed_hh"], vel)
                # Ghost kick on offbeat last bar of every 4
                if b % 4 == 3:
                    insert_note(take, beat0 + 3.5, 0.2, DRUMS["kick"], 70)
            elif sec_name == "chorus":
                # Driving: double kick, harder snare, open hat accents
                insert_note(take, beat0,       0.25, DRUMS["kick"], 110)
                insert_note(take, beat0 + 1.5, 0.2,  DRUMS["kick"], 90)
                insert_note(take, beat0 + 2,   0.25, DRUMS["snare"], 110)
                insert_note(take, beat0 + 3.5, 0.2,  DRUMS["kick"], 90)
                for s in range(8):
                    pitch = DRUMS["open_hh"] if s in (3, 7) else DRUMS["closed_hh"]
                    vel = 90 if s % 2 == 0 else 70
                    insert_note(take, beat0 + s * 0.5, 0.12, pitch, vel)
                # Crash on first beat of chorus
                if b == 0:
                    insert_note(take, beat0, 1.0, DRUMS["crash"], 105)
            elif sec_name == "variation":
                # Half-time feel: kick on 1, snare on 3 (single)
                insert_note(take, beat0,       0.25, DRUMS["kick"], 95)
                insert_note(take, beat0 + 2,   0.25, DRUMS["snare"], 90)
                # Ride pattern instead of hi-hat
                for s in range(4):
                    insert_note(take, beat0 + s, 0.2, DRUMS["ride"], 65)
                # Tom fill in last bar
                if b == length - 1:
                    for i, t in enumerate([DRUMS["tom_high"], DRUMS["tom_mid"], DRUMS["tom_low"]]):
                        insert_note(take, beat0 + 3 + i * 0.25, 0.2, t, 90)
            elif sec_name == "outro":
                # Subtractive: kick + light hat only
                insert_note(take, beat0,       0.3, DRUMS["kick"], 80 - b * 15)
                if b < length - 1:
                    for s in range(4):
                        insert_note(take, beat0 + s, 0.15, DRUMS["closed_hh"], 55 - b * 10)
        RPR.RPR_MIDI_Sort(take)

    # === Chords per section ===
    for sec_name, start_bar, length in sections:
        take = add_take(chords_idx, start_bar, length)
        # Choose chord progression — repeat 4-chord cycle through section
        for b in range(length):
            chord_root_offset = chord_roots[b % len(chord_roots)]
            base = chord_oct + chord_root_offset
            if sec_name == "intro":
                # Just root, sustained whole bar, low velocity
                insert_note(take, b * 4, 4, base, 50)
            elif sec_name == "verse":
                # Triad on each downbeat (root, third, fifth)
                triad = [0, 3, 7] if scale != "major" else [0, 4, 7]
                for off in triad:
                    insert_note(take, b * 4, 4, base + off, 70)
            elif sec_name == "chorus":
                # 7th chord with octave doubling
                seventh = [0, 3, 7, 10] if scale != "major" else [0, 4, 7, 11]
                for off in seventh:
                    insert_note(take, b * 4, 4, base + off, 88)
                    insert_note(take, b * 4, 4, base + off + 12, 75)
            elif sec_name == "variation":
                # Substitution: 9th chord
                ninth = [0, 3, 7, 10, 14] if scale != "major" else [0, 4, 7, 11, 14]
                for off in ninth:
                    insert_note(take, b * 4, 4, base + off, 78)
            elif sec_name == "outro":
                # Sustained final chord, decaying velocity
                triad = [0, 3, 7]
                for off in triad:
                    insert_note(take, b * 4, length * 4 - b * 4, base + off, 60 - b * 10)
        RPR.RPR_MIDI_Sort(take)

    # === Bass per section ===
    for sec_name, start_bar, length in sections:
        take = add_take(bass_idx, start_bar, length)
        for b in range(length):
            chord_root_offset = chord_roots[b % len(chord_roots)]
            base = bass_oct + chord_root_offset
            if sec_name == "intro":
                insert_note(take, b * 4, 4, base, 70)
            elif sec_name == "verse":
                # Root + fifth on beats 1 & 3
                insert_note(take, b * 4,     1, base, 95)
                insert_note(take, b * 4 + 2, 1, base + 7, 90)
            elif sec_name == "chorus":
                # Octave doubling, eighth-note pattern
                for s in range(8):
                    pitch = base if s % 4 != 2 else base + 12
                    insert_note(take, b * 4 + s * 0.5, 0.45, pitch, 100)
            elif sec_name == "variation":
                # Walking bass: root → 3rd → 5th → 7th
                walking = [0, 3, 7, 10]
                for i, off in enumerate(walking):
                    insert_note(take, b * 4 + i, 0.9, base + off, 85)
            elif sec_name == "outro":
                insert_note(take, b * 4, 4, base, 70 - b * 12)
        RPR.RPR_MIDI_Sort(take)

    # === Lead per section ===
    for sec_name, start_bar, length in sections:
        if sec_name in ("intro", "verse"):
            continue  # Lead absent in these sections
        take = add_take(lead_idx, start_bar, length)
        for b in range(length):
            chord_root_offset = chord_roots[b % len(chord_roots)]
            base = lead_oct + chord_root_offset
            if sec_name == "chorus":
                # Quarter-note melody from scale degrees 1, 3, 5, 7
                pattern = [intervals[0], intervals[2 % len(intervals)], intervals[4 % len(intervals)], intervals[6 % len(intervals)]]
                for i, off in enumerate(pattern):
                    insert_note(take, b * 4 + i, 0.9, base + off - intervals[0], 95)
            elif sec_name == "variation":
                # Sparse: one held note per bar, higher
                insert_note(take, b * 4, 3.5, base + 7, 70)
            elif sec_name == "outro":
                # Decay note
                insert_note(take, b * 4, length * 4 - b * 4, base, 60 - b * 12)
        RPR.RPR_MIDI_Sort(take)

    # === Pad per section (sustained throughout) ===
    pad_take = add_take(pad_idx, 0, total_bars)
    for b in range(total_bars):
        chord_root_offset = chord_roots[b % len(chord_roots)]
        base = chord_oct + chord_root_offset - 12
        # Held triad, low velocity, gives air
        triad = [0, 3, 7]
        for off in triad:
            insert_note(pad_take, b * 4, 4, base + off, 45)
    RPR.RPR_MIDI_Sort(pad_take)

    # === FX chain per track (from primer guidance) ===
    track_fx = {
        "Drums":   ["ReaEQ", "ReaComp", "ReaLimit"],
        "Sub Bass": ["ReaSynth", "ReaEQ", "ReaComp"],
        "Chords":  ["ReaSynth", "ReaEQ", "ReaDelay", "ReaVerb"],
        "Lead":    ["ReaSynth", "ReaEQ", "ReaDelay", "ReaVerb"],
        "Pad":     ["ReaSynth", "ReaEQ", "ReaVerb"],
    }
    for tname, fx_list in track_fx.items():
        if tname not in track_idx_by_name:
            continue
        idx = track_idx_by_name[tname]
        tr = RPR.RPR_GetTrack(0, idx)
        for fx in fx_list:
            RPR.RPR_TrackFX_AddByName(tr, fx, False, 1)

    return (
        f"Coordinator built {total_bars}-bar arrangement: "
        f"intro({intro_len}) + verse({verse_len}) + chorus({chorus_len}) + "
        f"variation({var_len}) + outro({outro_len}); "
        f"{len(track_idx_by_name)} tracks, BPM={bpm}, key={key} {scale}, genre={genre}"
    )
```

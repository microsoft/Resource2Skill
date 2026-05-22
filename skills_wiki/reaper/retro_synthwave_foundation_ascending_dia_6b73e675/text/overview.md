# Retro Synthwave Foundation (Ascending Diatonic Groove)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Retro Synthwave Foundation (Ascending Diatonic Groove)

* **Core Musical Mechanism**: A 4-on-the-floor drum beat coupled with an ascending diatonic chord progression (I - ii - iii - IV), played by wide, layered synth pads. This is anchored by a highly syncopated bassline hitting the roots on the downbeat and subsequent upbeats (Beat 1, 2&, 3&, 4&), creating a relentless "pushing" forward momentum.
* **Why Use This Skill (Rationale)**: The continuous harmonic ascension naturally builds emotional tension and triumph. Rhythmically, the straight 4/4 kick contrasted with the off-beat syncopated bass provides a classic "push-pull" groove inherent to retro electronic music. Layering different waveform oscillators (saw + square) with varied ADSR envelopes separates the frequency bands (thick pads vs. plucky bass) and creates a lush, retro aesthetic.
* **Overall Applicability**: Perfect for intros, verses, or main hooks in Synthwave, Retro Pop, Dreamwave, and 80s-inspired electronic tracks.
* **Value Addition**: Transforms a blank project into a fully arranged, multitrack groove featuring interlocking rhythms between the drums and bass, layered harmonic sound design, and robust voice leading.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Signature**: ~110 BPM, 4/4 time.
  - **Drums**: Straight quarter-note kicks (beats 1, 2, 3, 4) with steady 8th-note closed hi-hats.
  - **Pads**: Whole notes; one chord per bar, sustained fully.
  - **Bass Rhythm**: Syncopated 8th-note grid. Hits exactly on Beat 1.0, 2.5 (the 'and' of 2), 3.5 (the 'and' of 3), and 4.5 (the 'and' of 4). Note lengths are exactly 1/8th.

* **Step B: Pitch & Harmony**
  - **Progression**: I - ii - iii - IV (e.g., in F Major: Fmaj - Gmin - Amin - Bbmaj).
  - **Pad Voicings**: 4-note voicings spanning two octaves. Root note low + root-position triad an octave higher.
  - **Bass**: Plays only the root notes of the current chord, heavily sequenced.

* **Step C: Sound Design & FX**
  - **Pad 1 (Main)**: Saw-wave dominant synth. Slow attack (~500ms) and slow release to create a swelling wash of sound.
  - **Pad 2 (Layer)**: Square-wave dominant synth. Slightly different ADSR to create timbral width and width when layered with Pad 1.
  - **Bass**: Plucky saw/square mix. Fast attack (0ms), short decay, low sustain, fast release.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Drums, Pads, Bass MIDI | `RPR_CreateNewMIDIItemInProj` & `RPR_MIDI_InsertNote` | Precise velocity and syncopated grid timing (especially the bass offbeats) are required to capture the groove. |
| Synth Sound Design | FX chain (`ReaSynth`) & `RPR_TrackFX_SetParam` | Synthesizes the pad swells and bass plucks natively without requiring the specific third-party VSTs (TyrellN6, Repro) used in the video. |

> **Feasibility Assessment**: 85% — The rhythmic groove, harmonic structure, and core envelope differences (swelling pads vs. plucking bass) are fully reproduced. The specific premium analog character of the external VSTs is approximated using REAPER's native ReaSynth. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "RetroGroove",
    track_name: str = "Synthwave",
    bpm: int = 110,
    key: str = "F",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Retro Synthwave Foundation groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (loops the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_idx = NOTE_MAP.get(key.upper(), 5) # Default to F

    def get_scale_pitch(degree, intervals, root_pitch):
        octave = degree // len(intervals)
        scale_degree = degree % len(intervals)
        return root_pitch + (octave * 12) + intervals[scale_degree]

    def create_track_with_synth(name, is_synth=True):
        idx = RPR.RPR_GetNumTracks()
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        if is_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return track

    def create_midi_take(track, start_sec, end_sec):
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_sec, end_sec, False)
        return RPR.RPR_GetActiveTake(item)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len = 60.0 / bpm
    total_len_sec = bars * 4 * beat_len

    # === Step 2: Track Creation & Sound Design ===
    drum_track = create_track_with_synth(f"{track_name} Drums", is_synth=False)
    
    pad1_track = create_track_with_synth(f"{track_name} Pad Main")
    RPR.RPR_TrackFX_SetParam(pad1_track, 0, 0, 0.3)  # Volume slightly down
    RPR.RPR_TrackFX_SetParam(pad1_track, 0, 2, 0.5)  # Attack slow
    RPR.RPR_TrackFX_SetParam(pad1_track, 0, 5, 0.8)  # Release slow
    RPR.RPR_TrackFX_SetParam(pad1_track, 0, 8, 1.0)  # Saw mix up

    pad2_track = create_track_with_synth(f"{track_name} Pad Layer")
    RPR.RPR_TrackFX_SetParam(pad2_track, 0, 0, 0.3)  # Volume
    RPR.RPR_TrackFX_SetParam(pad2_track, 0, 2, 0.4)  # Attack slow
    RPR.RPR_TrackFX_SetParam(pad2_track, 0, 5, 0.6)  # Release slow
    RPR.RPR_TrackFX_SetParam(pad2_track, 0, 7, 1.0)  # Square mix up (for width difference)

    bass_track = create_track_with_synth(f"{track_name} Bass")
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.5)  # Volume
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.01) # Attack fast
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.2)  # Decay short (plucky)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.1)  # Sustain low
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.1)  # Release fast
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 7, 0.6)  # Square
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 8, 0.6)  # Saw

    # === Step 3: MIDI Generation ===
    drum_take = create_midi_take(drum_track, 0.0, total_len_sec)
    pad1_take = create_midi_take(pad1_track, 0.0, total_len_sec)
    pad2_take = create_midi_take(pad2_track, 0.0, total_len_sec)
    bass_take = create_midi_take(bass_track, 0.0, total_len_sec)

    # 4-bar ascending diatonic progression
    chords_degrees = [[0, 2, 4], [1, 3, 5], [2, 4, 6], [3, 5, 7]]

    notes_created = 0

    for bar in range(bars):
        bar_start_beat = bar * 4
        
        # --- Drums ---
        # Kick on quarters
        for b in range(4):
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, (bar_start_beat + b) * beat_len)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, (bar_start_beat + b + 0.25) * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
            notes_created += 1
            
        # Hat on 8ths
        for hb in range(8):
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, (bar_start_beat + hb * 0.5) * beat_len)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, (bar_start_beat + hb * 0.5 + 0.25) * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 42, int(velocity_base * 0.7), False)
            notes_created += 1

        # --- Pads ---
        prog_step = bar % 4
        chord_deg = chords_degrees[prog_step]
        
        start_ppq_pad = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad1_take, bar_start_beat * beat_len)
        end_ppq_pad = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad1_take, (bar_start_beat + 4) * beat_len)
        
        pitches = [get_scale_pitch(chord_deg[0], scale_intervals, root_idx + 36)] # Bass octave
        for d in chord_deg:
            pitches.append(get_scale_pitch(d, scale_intervals, root_idx + 48)) # Triad
            
        for p in pitches:
            p = max(0, min(127, p))
            RPR.RPR_MIDI_InsertNote(pad1_take, False, False, start_ppq_pad, end_ppq_pad, 0, p, velocity_base - 10, False)
            RPR.RPR_MIDI_InsertNote(pad2_take, False, False, start_ppq_pad, end_ppq_pad, 0, p, velocity_base - 10, False)
            notes_created += 2

        # --- Bass ---
        bass_pitch = get_scale_pitch(chord_deg[0], scale_intervals, root_idx + 24)
        bass_pitch = max(0, min(127, bass_pitch))
        
        # Syncopated rhythm: beats 1.0, 2.5, 3.5, 4.5
        bass_offsets = [0.0, 1.5, 2.5, 3.5]
        
        for offset in bass_offsets:
            start_ppq_bass = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, (bar_start_beat + offset) * beat_len)
            end_ppq_bass = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, (bar_start_beat + offset + 0.5) * beat_len)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq_bass, end_ppq_bass, 0, bass_pitch, velocity_base, False)
            notes_created += 1

    return f"Created Retro Synthwave Foundation: 4 tracks, {notes_created} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```
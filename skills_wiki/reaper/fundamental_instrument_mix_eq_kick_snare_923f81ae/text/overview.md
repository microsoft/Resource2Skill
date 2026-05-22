# Fundamental Instrument Mix EQ (Kick, Snare, Lead/Vocal)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Fundamental Instrument Mix EQ (Kick, Snare, Lead/Vocal)

* **Core Musical Mechanism**: Subtractive and Additive Equalization tailored to specific instrument profiles. The signature of this pattern is identifying where an instrument holds "mud" or "boxiness" (usually low-mids around 300-400Hz) and removing it, while boosting its fundamental weight (lows) and its character/presence (upper-mids/highs).
* **Why Use This Skill (Rationale)**: This is the bedrock of modern mixing. Unprocessed instruments compete for the same frequency real estate, creating masking (where a loud frequency hides a quieter one). By cutting the 400Hz range on a kick, you make room for the bass guitar; by boosting 3kHz on a snare or vocal, you push it to the front of the psychoacoustic depth field without raising the master fader volume.
* **Overall Applicability**: This technique applies to nearly every production across all genres (Hip-Hop, Pop, EDM, Rock). Specific curves included here are designed for Kick Drums, Snare Drums, and Lead Synth/Vocals. 
* **Value Addition**: Compared to a raw mix, this skill encodes professional mixing intuition. It automatically carves out conflicting frequencies and enhances the characteristic "sweet spots" of standard track elements, resulting in a cleaner, punchier mix instantly.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: 120 BPM (Configurable)
  - **Rhythm**: 4-on-the-floor kick, 2 & 4 snare pattern, and a syncopated 1/8th note lead melody to demonstrate the processing in a musical context.
* **Step B: Pitch & Harmony**
  - Uses the provided `key` and `scale` parameters to generate a lead melody. 
  - Generates MIDI notes programmatically using scale degree math.
* **Step C: Sound Design & FX**
  - **Synths**: `ReaSynth` is used as a placeholder sound generator for all tracks.
  - **Kick EQ Chain (`ReaEQ`)**: 
    - Band 1 (Low Shelf): +3.5dB at 120Hz (Weight)
    - Band 2 (Band): -5.0dB at 400Hz (Mud cut)
    - Band 3 (Band): +5.0dB at 3000Hz (Beater click)
  - **Snare EQ Chain (`ReaEQ`)**:
    - Band 1 (Low Shelf): +6.0dB at 150Hz (Body/Chest)
    - Band 3 (Band): +5.0dB at 3000Hz (Crack)
    - Band 4 (High Shelf): +4.0dB at 7000Hz (Sizzle/Air)
  - **Lead/Vocal EQ Chain (`ReaEQ`)**:
    - Band 1 (Low Shelf used as High Pass): -12.0dB at 100Hz (Rumble cut)
    - Band 2 (Band): -3.0dB at 350Hz (Boxiness cut)
    - Band 3 (Band): +3.0dB at 3000Hz (Presence)
    - Band 4 (High Shelf): +4.0dB at 5000Hz (Air)
* **Step D: Mix & Automation**
  - Static mix settings. The focus is entirely on frequency shaping via inserts.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track/Arrangement Generation | `RPR_InsertTrackAtIndex`, `RPR_CreateNewMIDIItemInProj` | Additively creates a multi-track environment to demonstrate the skill. |
| Musical Content | `RPR_MIDI_InsertNote` | Computes scale degrees to create a contextual backing track for the mixing demonstration. |
| Mixing Approach (EQ Curves) | `RPR_TrackFX_AddByName`, `RPR_TrackFX_SetParam` | Directly replicates the exact parametric EQ moves (Frequency and Gain) shown in the video for each specific element. |

> **Feasibility Assessment**: 100% reproduction of the EQ parameter curves demonstrated. Because standard ReaScript API does not expose a straightforward way to change ReaEQ filter *types* (e.g., from Shelf to High Pass) without chunk manipulation, the script simulates the High Pass filter by aggressively cutting the default Low Shelf band.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MixEQ",
    track_name: str = "InstrumentEQ",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Kick, Snare, and Lead track with fundamental instrument-specific EQ curves.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
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

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper(), 0)
    
    def get_pitch(octave, degree):
        octave_shift = degree // len(scale_intervals)
        rem_degree = degree % len(scale_intervals)
        # C4 = 60
        return 12 + (octave + octave_shift) * 12 + root_val + scale_intervals[rem_degree]

    def insert_midi_item(track, start_time, length, notes):
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, start_time + length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        for note in notes:
            start_beat, end_beat, pitch, vel = note
            n_start_time = start_time + (start_beat * (60.0 / bpm))
            n_end_time = start_time + (end_beat * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        
        RPR.RPR_MIDI_Sort(take)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    # === 1. KICK TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name}_Kick", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Set to fast decay sine for kick thud
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 3, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 4, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 6, 0.0) # Square 
    RPR.RPR_TrackFX_SetParam(kick_track, synth_idx, 7, 0.0) # Saw

    eq_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 0, 120.0) # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 1, 3.5)   # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 3, 400.0) # Band 2 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 4, -5.0)  # Band 2 Gain
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 6, 3000.0)# Band 3 Freq
    RPR.RPR_TrackFX_SetParam(kick_track, eq_idx, 7, 5.0)   # Band 3 Gain

    # === 2. SNARE TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    snare_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(snare_track, "P_NAME", f"{track_name}_Snare", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 3, 0.05) # Very fast Decay
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 4, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 6, 0.5)  # Square
    RPR.RPR_TrackFX_SetParam(snare_track, synth_idx, 7, 0.5)  # Saw

    eq_idx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 0, 150.0) # Band 1 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 1, 6.0)   # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 6, 3000.0)# Band 3 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 7, 5.0)   # Band 3 Gain
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 9, 7000.0)# Band 4 Freq
    RPR.RPR_TrackFX_SetParam(snare_track, eq_idx, 10, 4.0)  # Band 4 Gain

    # === 3. LEAD / VOCAL TRACK ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    lead_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", f"{track_name}_Lead", True)

    synth_idx = RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, synth_idx, 7, 1.0) # Saw wave for richness
    
    eq_idx = RPR.RPR_TrackFX_AddByName(lead_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 0, 100.0)  # Band 1 Freq (HPF sim)
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 1, -12.0)  # Band 1 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 3, 350.0)  # Band 2 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 4, -3.0)   # Band 2 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 6, 3000.0) # Band 3 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 7, 3.0)    # Band 3 Gain
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 9, 5000.0) # Band 4 Freq
    RPR.RPR_TrackFX_SetParam(lead_track, eq_idx, 10, 4.0)   # Band 4 Gain

    # === GENERATE MIDI ARANGEMENT ===
    kick_notes = []
    snare_notes = []
    lead_notes = []
    
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        # Kick: 4-on-the-floor
        kick_notes.extend([
            (bar_offset + 0, bar_offset + 0.5, 36, velocity_base),
            (bar_offset + 1, bar_offset + 1.5, 36, velocity_base),
            (bar_offset + 2, bar_offset + 2.5, 36, velocity_base),
            (bar_offset + 3, bar_offset + 3.5, 36, velocity_base),
        ])
        # Snare: Beats 2 and 4 (indices 1 and 3)
        snare_notes.extend([
            (bar_offset + 1, bar_offset + 1.25, 48, velocity_base),
            (bar_offset + 3, bar_offset + 3.25, 48, velocity_base),
        ])
        # Lead: Syncopated melody
        lead_notes.extend([
            (bar_offset + 0.0, bar_offset + 0.5, get_pitch(4, 0), velocity_base),
            (bar_offset + 0.5, bar_offset + 1.0, get_pitch(4, 2), velocity_base),
            (bar_offset + 1.5, bar_offset + 2.0, get_pitch(4, 4), velocity_base),
            (bar_offset + 2.5, bar_offset + 3.0, get_pitch(4, 2), velocity_base),
            (bar_offset + 3.0, bar_offset + 3.5, get_pitch(4, 1), velocity_base),
        ])

    insert_midi_item(kick_track, 0.0, total_length, kick_notes)
    insert_midi_item(snare_track, 0.0, total_length, snare_notes)
    insert_midi_item(lead_track, 0.0, total_length, lead_notes)

    return f"Created 3 Tracks (Kick, Snare, Lead) demonstrating Fundamental Mix EQ over {bars} bars at {bpm} BPM in {key} {scale}."
```
# Authentic Bossa Nova Piano Comping (Decoupled Bass & Syncopated Chords)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Authentic Bossa Nova Piano Comping (Decoupled Bass & Syncopated Chords)

* **Core Musical Mechanism**: The defining technique of this pattern is separating the harmonic rhythm into two distinct roles: a relaxed, unsyncopated bassline (playing sparse half notes or whole notes on beats 1 and 3) and a highly syncopated, forward-leaning chordal rhythm in the right hand (or tenor register). This avoids the amateur "cliché" of playing a bouncy `dum... da-dum` rhythm in the left hand.
* **Why Use This Skill (Rationale)**: In an authentic Brazilian Bossa Nova ensemble, the bass player provides the foundational root/fifth movement, while the guitar or piano handles the cross-rhythmic syncopation (the *partido alto* or bossa clave). On a solo piano, replicating that syncopated bassline makes the groove too rigid and cluttered. By playing relaxed half-notes in the bass and moving the syncopation to extended chord voicings (7ths, 9ths), you create forward momentum, harmonic richness, and a much lighter, breathing groove.
* **Overall Applicability**: This pattern is essential for jazz, Latin, lo-fi hip-hop, and lounge music. It serves as an excellent foundation for verse piano tracks, electric piano/Rhodes beds in neo-soul, or anytime an authentic, flowing Latin groove is required. 
* **Value Addition**: Compared to a standard chord block, this pattern encodes advanced hand-independence, authentic Latin cross-rhythms, and jazz-standard chord voicings (building rootless 3-5-7-9 stacks over the split bass). 


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically played between 100 and 140 BPM (or half-time at 60-70 BPM). 
  - **Grid**: Straight 8th notes. No swing. Bossa nova relies on precise, straight cross-rhythms. 
  - **Bass Rhythm**: Half notes placed squarely on Beat 1 and Beat 3.
  - **Chord Rhythm (2-bar phrase)**:
    - *Bar 1*: Beat 1 (Downbeat), Beat 2& (Upbeat), Beat 4 (Downbeat).
    - *Bar 2*: Beat 1& (Upbeat), Beat 3 (Downbeat), Beat 4& (Upbeat).
  - **Dynamics**: Accents are slightly emphasized on the syncopated upbeats to drive the groove forward.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parameterized. Commonly uses minor keys (e.g., C minor). 
  - **Left Hand**: Plays the Root on Beat 1, and the 5th on Beat 3, roughly two octaves below middle C.
  - **Right Hand (Chords)**: Plays a stacked 3rd, 5th, 7th, and 9th in the middle/tenor register. By omitting the root in the right hand, it achieves a standard Jazz/Bossa voicing with rich tension.

* **Step C: Sound Design & FX**
  - **Instrument**: An electric piano/Rhodes tone or mellow acoustic piano. 
  - **Synthesis**: A blend of square and saw waves with a fast attack, medium decay, and low sustain gives a nice "plucky" comping tone using stock REAPER tools (ReaSynth).

* **Step D: Mix & Automation**
  - No complex automation needed; the groove relies entirely on MIDI velocity humanization and precise straight-8th timing.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bass & Chord Separation | MIDI note insertion | Allows precise, programmatic placement of the 2-bar clave cross-rhythm. |
| Jazz Voicings (3,5,7,9) | Music Theory Logic | Computes scale degrees dynamically so the pattern works in any key/scale parameter. |
| Mellow Piano Tone | FX chain (ReaSynth) | ReaSynth configured with a Square-heavy mix and short decay emulates the percussive, warm tone of a comping keyboard without needing external VSTs. |

> **Feasibility Assessment**: 100% reproducible for the MIDI composition and rhythmic structure. The exact acoustic grand piano resonance shown in the tutorial is approximated using a synthesized electric piano tone built from native REAPER plugins. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bossa_Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create an Authentic Bossa Nova Piano Groove in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (should be even to fit the 2-bar phrase).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # --- Music Theory Lookup Tables ---
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

    # Helper to calculate extended scale degrees (e.g., 9ths, 11ths)
    def get_degree(deg, arr):
        octave_shift = deg // len(arr)
        idx = deg % len(arr)
        return arr[idx] + (12 * octave_shift)

    # --- Project & Track Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- MIDI Item Setup ---
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = bars * beats_per_bar * sec_per_beat
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # --- Pitch Calculation ---
    base_note = 60 + NOTE_MAP.get(key, 0) # Middle C octave
    scale_arr = SCALES.get(scale, SCALES["minor"])
    
    # Bass left hand (Root and 5th, 2 octaves down)
    bass_root = base_note - 24 + get_degree(0, scale_arr)
    bass_5th  = base_note - 24 + get_degree(4, scale_arr)
    
    # Right hand jazz voicing (3rd, 5th, 7th, 9th)
    chord_pitches = [
        base_note + get_degree(2, scale_arr),
        base_note + get_degree(4, scale_arr),
        base_note + get_degree(6, scale_arr),
        base_note + get_degree(8, scale_arr)
    ]

    # --- Rhythm Arrays (Beat relative to bar start, Duration) ---
    bass_rhythm = [
        (0.0, 1.8),  # Beat 1
        (2.0, 1.8)   # Beat 3
    ]
    # Standard 2-bar Bossa syncopation (Clave)
    chord_rhythm_even = [
        (0.0, 1.0),  # Downbeat 1
        (1.5, 1.0),  # Upbeat 2
        (3.0, 1.0)   # Downbeat 4
    ]
    chord_rhythm_odd = [
        (0.5, 1.0),  # Upbeat 1
        (2.0, 1.0),  # Downbeat 3
        (3.5, 1.0)   # Upbeat 4
    ]

    # --- Helper function for inserting notes ---
    def insert_note(start_beat, duration_beats, pitch, velocity):
        start_sec = start_beat * sec_per_beat
        end_sec = (start_beat + duration_beats) * sec_per_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        # Bounds check velocity
        vel = max(1, min(127, int(velocity)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)

    # --- Generate MIDI Events ---
    note_count = 0
    for b in range(bars):
        bar_start_beat = b * 4.0
        
        # Insert Bass Notes (Relaxed Half Notes)
        insert_note(bar_start_beat + bass_rhythm[0][0], bass_rhythm[0][1], bass_root, velocity_base - 5)
        insert_note(bar_start_beat + bass_rhythm[1][0], bass_rhythm[1][1], bass_5th, velocity_base - 5)
        note_count += 2
        
        # Insert Syncopated Chords
        active_chord_rhythm = chord_rhythm_even if (b % 2 == 0) else chord_rhythm_odd
        for beat_offset, duration in active_chord_rhythm:
            # Humanize velocity: upbeats (ending in .5) get slight accents
            is_upbeat = (beat_offset % 1.0) != 0.0
            vel = velocity_base + 12 if is_upbeat else velocity_base
            
            for pitch in chord_pitches:
                insert_note(bar_start_beat + beat_offset, duration, pitch, vel)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # --- FX Setup (ReaSynth for Electric Piano Tone) ---
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth to sound somewhat like a warm Rhodes/Wurlitzer
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.1)  # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.4)  # Square mix (warmth)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.01) # Fast attack
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.3)  # Medium decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.2)  # Low sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 7, 0.4)  # Natural release

    return f"Created Bossa Nova groove track '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```
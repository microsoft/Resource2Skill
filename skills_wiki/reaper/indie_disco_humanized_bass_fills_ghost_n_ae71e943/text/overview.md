# Indie Disco Humanized Bass Fills (Ghost Notes & Syncopation)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Indie Disco Humanized Bass Fills (Ghost Notes & Syncopation)

* **Core Musical Mechanism**: The tutorial demonstrates taking a static, robotic 8th-note MIDI bassline and transforming it into a realistic "played" bassline using generative session features. The underlying musical signature of this technique relies on two key elements: **Ghost/Dead Notes** (low velocity, very short muted string plucks) and **Syncopated 16th-Note Turnaround Fills** (octave jumps and 5th interval bounces at the end of a 4-bar phrase). 

* **Why Use This Skill (Rationale)**: A straight 8th-note bassline provides a solid driving foundation but lacks groove and human feel. By injecting 16th-note syncopations and dead notes at phrase boundaries (turnarounds), you mimic the physical reality of a bassist repositioning their hand on the fretboard. Ghost notes provide percussive rhythmic momentum without interfering with the harmonic structure, filling the "gaps" and interlocking perfectly with a drum groove.

* **Overall Applicability**: This technique is essential for Indie Pop, Nu-Disco, Funk, and Pop Rock. It works best during the transitions between song sections or at the end of an 8/16-bar phrase to build momentum before the downbeat of the next progression.

* **Value Addition**: Instead of a flat, uninspiring MIDI block, this skill encodes real bass articulation. It introduces dynamic velocity mapping (accents vs. ghost notes), phrase-aware rhythm variations (staying solid for 3 bars, filling on the 4th), and automatic voice-leading constraints (keeping bass notes in the "pocket" range of E1 to E2).

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 - 124 BPM (Standard Indie Disco tempo).
  - **Grid**: 8th-note main driving groove. 16th-note grid for the fills and ghost notes.
  - **Durations**: Legato 8th notes for the main groove. Staccato/muted durations (approx. 0.05 seconds) for dead notes.

* **Step B: Pitch & Harmony**
  - **Progression**: Extracted from the video's chord track: F - Am - F - G (Relative VI - I - VI - VII in A minor).
  - **Voice Leading**: Bass notes are mathematically folded into the standard E1 (MIDI 28) to E2 (MIDI 40) range to avoid muddy low frequencies or unnaturally high fundamental pitches.
  - **Fills**: Fills utilize the Octave (+12 semitones) and the Perfect Fifth (+7 semitones) of the current chord, preventing melodic clashes with the vocal or lead lines.

* **Step C: Sound Design & FX**
  - **Synth**: `ReaSynth` configured for a plucky, low-passed bass tone.
  - **Processing**: `ReaEQ` for low-end boost and `ReaComp` to level out the highly dynamic velocities (especially catching the transient of the ghost notes).

* **Step D: Mix & Automation**
  - The humanization comes entirely from MIDI velocity and timing, allowing the compressor to work naturally as it would on a recorded DI bass guitar.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bassline Groove & Fills | MIDI note insertion | Allows precise 16th-note timing, velocity manipulation for ghost notes, and phrase-aware generation (fills only on bar 4). |
| Bass Articulation | MIDI duration control | Native REAPER MIDI allows us to insert extremely short notes to simulate the "dead note" articulation highlighted in the tutorial. |
| Tone / Sound Design | FX chain (ReaSynth + ReaEQ + ReaComp) | Since we don't have Logic's "Studio Bass" VST, we stack stock REAPER plugins to simulate a punchy, compressed indie bass tone. |

> **Feasibility Assessment**: 85% reproduction. While we cannot invoke an AI to generate infinite random fills like Logic's Session Player, we *can* procedurally generate the exact musical output shown in the tutorial: 8th notes interwoven with a dynamic, syncopated 16th-note ghost/octave fill at the turnaround.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Indie Disco Bass",
    bpm: int = 124,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates an Indie Disco bassline with humanized 16th-note fills and ghost notes.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (must be multiple of 4 for best results).
        velocity_base: Base MIDI velocity for accented notes (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Step 2: Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Step 3: Configure MIDI Item
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    item_length = bar_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Base pitch calculation (E1 = 28 to E2 = 40 is the typical bass "pocket")
    root_val = NOTE_MAP.get(key.capitalize(), 9)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_midi_pitch = 24 + root_val # C1 is 24

    # Helper function to insert a single note
    def insert_note(start_beat, length_beats, pitch, velocity):
        start_time = start_beat * beat_sec
        end_time = start_time + (length_beats * beat_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # The progression from the tutorial: VI - I - VI - VII
    # In minor, these are indices 5, 0, 5, 6.
    prog_indices = [5, 0, 5, 6]
    note_count = 0

    for b_idx in range(bars):
        chord_degree_index = prog_indices[b_idx % len(prog_indices)]
        semitone_offset = scale_intervals[chord_degree_index]
        
        chord_pitch = base_midi_pitch + semitone_offset
        # Fold pitch into the bass pocket (prevent playing too high or low)
        while chord_pitch > 40:
            chord_pitch -= 12
        while chord_pitch < 28:
            chord_pitch += 12

        start_beat_of_bar = b_idx * beats_per_bar

        # If it's the 4th bar of the phrase, inject the 16th-note syncopated fill
        if b_idx % 4 == 3:
            # Beats 1 and 2: Standard 8th notes
            for beat_offset in [0.0, 0.5, 1.0, 1.5]:
                insert_note(start_beat_of_bar + beat_offset, 0.45, chord_pitch, velocity_base)
                note_count += 1
            
            # Beat 3 and 4: Indie Disco Fill with Dead Notes
            # 3.0: Octave (Accented)
            insert_note(start_beat_of_bar + 2.0, 0.23, chord_pitch + 12, velocity_base + 10)
            # 3.25: Ghost note on root
            insert_note(start_beat_of_bar + 2.25, 0.05, chord_pitch, 40)
            # 3.5: Perfect 5th
            insert_note(start_beat_of_bar + 2.5, 0.23, chord_pitch + 7, velocity_base - 5)
            # 3.75: Ghost note on root
            insert_note(start_beat_of_bar + 2.75, 0.05, chord_pitch, 40)
            
            # 4.0: Perfect 5th
            insert_note(start_beat_of_bar + 3.0, 0.23, chord_pitch + 7, velocity_base)
            # 4.25: Octave
            insert_note(start_beat_of_bar + 3.25, 0.23, chord_pitch + 12, velocity_base)
            # 4.5: Ghost note on root
            insert_note(start_beat_of_bar + 3.5, 0.05, chord_pitch, 40)
            # 4.75: Pick-up note into the next bar
            insert_note(start_beat_of_bar + 3.75, 0.25, chord_pitch, velocity_base - 10)
            
            note_count += 8
            
        else:
            # Standard driving 8th notes
            for beat_offset in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
                # Slight velocity humanization (accent the downbeats slightly)
                vel = velocity_base if (beat_offset % 1.0 == 0) else velocity_base - 15
                insert_note(start_beat_of_bar + beat_offset, 0.45, chord_pitch, vel)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # Step 4: Add FX Chain (ReaSynth, ReaEQ, ReaComp)
    # ReaSynth for tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth: fast attack, plucky decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.5)  # Square mix
    
    # ReaEQ to boost low end
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Set band 1 to a low shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0) # Tab 1 (Low Shelf)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 100) # Freq 100Hz (normalized value approx 0.2 in some ReaEQ versions, but keeping simple)
    
    # ReaComp to catch the ghost notes and level the performance
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -18.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio 4:1
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 0.01)  # Fast attack for slap/ghosts
    
    return f"Created '{track_name}' with {note_count} notes over {bars} bars (featuring ghost notes and turnaround fills) at {bpm} BPM."
```
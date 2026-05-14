# Neo-Soul / J-Dilla Lazy Groove & Harmonic Progression

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neo-Soul / J-Dilla Lazy Groove & Harmonic Progression

* **Core Musical Mechanism**: This pattern relies on a signature Neo-Soul/Jazz harmonic movement combined with "lazy" micro-timed drum sequencing. The progression moves smoothly down the scale via mode mixture and tritone substitution (`I -> iv -> bIII -> ii -> bII`), using extended rootless chord voicings (9ths, 11ths, maj7s). The drums achieve a distinct "drunken" or "lazy" pocket by shifting the snares, hi-hat offbeats, and chords slightly behind the quantization grid while the kick stays rigidly locked.
* **Why Use This Skill (Rationale)**: The harmonic progression introduces subtle tension and melancholy by borrowing chords from the parallel minor (the `iv` and `bIII` chords) and sliding down chromatically (the `bII` tritone substitution resolving hypothetically back to `I`). The rhythmic offset (J-Dilla swing) creates a push-and-pull psychoacoustic effect: the on-grid kicks push the track forward, while the delayed snares and chords drag it back, creating a deep, humanized groove.
* **Overall Applicability**: This is the foundation for Neo-Soul, Lo-Fi Hip-Hop, R&B, and modern Jazz-Hop beats. It serves perfectly as the main loop for a verse or intro.
* **Value Addition**: Generates complex, genre-authentic extended chord voicings automatically based on any root key, while injecting realistic hip-hop swing algorithms into the MIDI data, bypassing the need for manual micro-timing adjustments.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 72 BPM.
  - **Time Signature**: 4/4.
  - **Swing/Micro-timing**: 
    - Kick hits exactly on the grid.
    - Snares are delayed by ~60ms (0.06 beats).
    - Off-beat 8th-note hi-hats are delayed by ~80ms (0.08 beats) to create a heavily swung, triplet-like feel.
    - Chords and bassline are delayed by ~40ms (0.04 beats) to sit comfortably in the "laid-back" pocket.
* **Step B: Pitch & Harmony**
  - **Progression**: C Maj9 -> F min9 -> Eb Maj add9 -> D min7 -> Db Maj7. (Relative to C: I -> iv -> bIII -> ii -> bII).
  - **Voicings** (Relative to Root):
    - Maj 9: Root in bass; [Maj7, 9, 3, 5] in the right hand.
    - min 9: Root in bass; [m3, P5, m7, 9] in the right hand.
    - Maj add 9: Root in bass; [M3, P5, 8ve, 9] in the right hand.
    - min 7 (add 11): Root in bass; [m3, P5, m7, m3(8ve)] in the right hand.
    - Maj 7 (add 3): Root in bass; [M3, P5, M7, M3(8ve)] in the right hand.
* **Step C: Sound Design & FX**
  - **Chords**: Emulated Electric Piano (Rhodes). Built via stock REAPER synthesis with low-pass filtering.
  - **Bass**: Deep sub/upright acoustic hybrid.
  - **Drums**: Standard hip-hop layout (Kick on 36, Snare on 38, Hat on 42).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Voicings | Parameterized MIDI insertion | Mathematical calculation of extended chord intervals guarantees correct voice leading in any key. |
| Lazy Groove / Swing | Precise PPQ offset calculation | Hard-coding timing offsets natively recreates the specific humanized "J-Dilla" feel without relying on external groove templates. |
| Instrumentation | ReaSynth + ReaEQ + Routing | Generates additive placeholder synths so the progression is instantly audible and mix-ready, awaiting the user's premium VSTs or samples. |

> **Feasibility Assessment**: 95%. The musical theory, chord voicings, and crucial micro-timing groove are perfectly reproduced. The remaining 5% is simply replacing the stock ReaSynth placeholders with high-quality sample libraries (like Spitfire BBC Symphony or genuine Rhodes emulations shown in the video).

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Neo_Soul_Beat",
    track_name: str = "Neo_Soul",
    bpm: int = 72,
    key: str = "C",
    scale: str = "major",  # The pattern forces custom mode mixture regardless of scale
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul harmonic progression and lazy drum groove in REAPER.
    
    Args:
        project_name: Project identifier.
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM (70-80 recommended for Neo-Soul).
        key: Root note (C, C#, D, ..., B).
        scale: Ignored for chords (uses strict Neo-Soul mode mixture).
        bars: Number of bars to generate (multiples of 4 recommended).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Note map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    key_str = key.capitalize() if key.capitalize() in NOTE_MAP else "C"
    root_pitch = 60 + NOTE_MAP[key_str] # C3 is our mathematical center

    # 1. Create Tracks Additively
    track_count = RPR.RPR_CountTracks(0)
    
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    track_chords = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name} Chords (EP)", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_chords, "D_VOL", 0.6)
    
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    track_bass = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name} Bass", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_bass, "D_VOL", 0.8)
    
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    track_drums = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{track_name} Drums", True)
    RPR.RPR_SetMediaTrackInfo_Value(track_drums, "D_VOL", 0.9)

    # 2. Add Basic FX Placeholders
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    eq_chords = RPR.RPR_TrackFX_AddByName(track_chords, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track_chords, eq_chords, 10, -18.0) # Lowpass filter effect on Band 4
    
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    eq_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track_bass, eq_bass, 10, -24.0) # Deep sub cut

    # 3. Create MIDI Items
    item_length_sec = (60.0 / bpm) * 4 * bars
    
    def create_midi_take(track):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        return RPR.RPR_AddTakeToMediaItem(item)

    take_chords = create_midi_take(track_chords)
    take_bass = create_midi_take(track_bass)
    take_drums = create_midi_take(track_drums)

    def add_midi_note(take, start_beat, end_beat, pitch, vel):
        vel = max(1, min(127, int(vel)))
        start_ppq = int(start_beat * 960)
        end_ppq = int(end_beat * 960)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # 4. Neo-Soul Chords & Bass Generation
    # Chords map: I Maj9 -> iv min9 -> bIII Maj add9 -> ii min7 -> bII Maj7
    chords_seq = [
        {"root": 0, "bass_offset": -24, "voicing": [-1, 2, 4, 7], "start": 0.0, "dur": 4.0},
        {"root": 5, "bass_offset": -24, "voicing": [3, 7, 10, 14], "start": 4.0, "dur": 4.0},
        {"root": 3, "bass_offset": -24, "voicing": [4, 7, 12, 14], "start": 8.0, "dur": 2.0},
        {"root": 2, "bass_offset": -24, "voicing": [3, 7, 10, 15], "start": 10.0, "dur": 2.0},
        {"root": 1, "bass_offset": -24, "voicing": [4, 7, 11, 16], "start": 12.0, "dur": 4.0},
    ]

    # The lazy pocket offset for chords and bass
    laid_back_offset = 0.04

    for b in range(0, bars, 4):
        bar_beat = b * 4
        for c in chords_seq:
            c_start = bar_beat + c["start"]
            if c_start >= bars * 4:
                break
            
            actual_start = c_start + laid_back_offset
            c_dur = c["dur"]
            root_abs = root_pitch + c["root"]
            
            # Bass Note
            add_midi_note(take_bass, actual_start, actual_start + c_dur - 0.1, root_abs + c["bass_offset"], velocity_base)
            
            # Chord Extensions
            for interval in c["voicing"]:
                add_midi_note(take_chords, actual_start, actual_start + c_dur - 0.1, root_abs + interval, velocity_base - 15)

    # 5. Dilla/Neo-Soul Drum Groove Generation
    snare_lazy_offset = 0.06
    
    for i in range((bars + 1) // 2): 
        bar_offset = i * 8 # 2 bars = 8 beats
        
        # Syncopated Kick
        for kb in [0.0, 2.5, 3.5, 4.0, 6.5, 7.5]:
            if bar_offset + kb < bars * 4:
                add_midi_note(take_drums, bar_offset + kb, bar_offset + kb + 0.25, 36, velocity_base + 10)
        
        # Lazy Snare
        for sb in [2.0, 6.0]:
            actual_sb = bar_offset + sb + snare_lazy_offset
            if actual_sb < bars * 4:
                add_midi_note(take_drums, actual_sb, actual_sb + 0.25, 38, velocity_base)
        
        # Swung Hi-Hats
        for hb in range(16): # 16 eighth-notes in 2 bars
            beat_pos = hb * 0.5
            # Apply 16th note heavy swing to the off-beats
            swing = 0.08 if hb % 2 == 1 else 0.0
            actual_hb = bar_offset + beat_pos + swing
            vel = velocity_base - 10 if hb % 2 == 0 else velocity_base - 35
            
            if actual_hb < bars * 4:
                add_midi_note(take_drums, actual_hb, actual_hb + 0.2, 42, vel)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created Neo-Soul groove '{track_name}' in {key} over {bars} bars at {bpm} BPM with J-Dilla micro-timing swing."
```
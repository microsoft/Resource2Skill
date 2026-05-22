### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Arrangement & Filter Sweep Transition

* **Core Musical Mechanism**: The tutorial demonstrates a fundamental modern production technique: starting the arrangement process with the highest-energy section (the Chorus) fully fleshed out, and then *subtracting* elements (kicks, bass, hi-hats, melodies) to create lower-energy sections (Verses). To transition back into the high-energy chorus, a Low-Pass Filter sweep is applied to the instruments, accompanied by a custom-shaped automation curve and a physical riser/sweep sample, creating a "vacuum" effect right before the drop.
* **Why Use This Skill (Rationale)**: 
    * **Subtractive Arrangement**: It ensures thematic and harmonic consistency across the track while naturally managing the listener's energy expectations. By removing the driving low-end (kick/bass) in the verse, the eventual return of these elements in the chorus feels exponentially more impactful.
    * **Filter Sweeps**: A low-pass filter rolling down reduces high-frequency energy, creating a psychoacoustic "muffled" or "underwater" effect. This builds intense anticipation. When the filter instantly opens at the downbeat of the chorus, the sudden influx of high frequencies triggers a massive perceived dynamic leap without actually increasing the master volume.
* **Overall Applicability**: Essential for beat-making (Hip-hop, Trap, Boom-bap), EDM drops, and modern Pop song structuring. It is universally used to differentiate Verse/Pre-Chorus sections from Chorus sections.
* **Value Addition**: This skill encodes structural arrangement logic. Instead of just creating an 8-bar loop, it creates a full 16-bar song skeleton (Verse -> Chorus) that automatically manages rhythmic density and automates a tension-building filter riser.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically 110-140 BPM for modern rap/trap beats.
  - **Grid Divisions**: 8-bar sections. 
  - **Arrangement**: 
    - *Verse (Bars 1-8)*: Sparse. Kicks and bass are completely removed in the first half. Hi-hats are introduced halfway through (Bar 5).
    - *Chorus (Bars 9-16)*: Full density. Kick, snare, continuous 8th-note hi-hats, and sub-bass are active simultaneously.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically minor or harmonic minor keys.
  - **Progression**: The chords remain identical between the verse and chorus to anchor the track, generally following a minor progression (e.g., i - VI - III - VII).
* **Step C: Sound Design & FX**
  - **Instruments**: Synthesized chords, deep sub bass, and sharp hip-hop drum samples.
  - **FX Chain (The Transition)**: `ReaEQ` is applied to the instrument/chord bus. 
  - **ReaEQ Setup**: A high band (Band 4) is converted into a high-cut/low-pass filter (or a high-shelf with -inf dB gain).
* **Step D: Mix & Automation**
  - **Automation Curve**: The filter frequency is automated. Over the final bar of the verse (Bar 8), the frequency sweeps smoothly from 20kHz down to ~400Hz.
  - **Curve Shape**: The tutorial specifically notes creating a "curved" (Bezier/Exponential) fade rather than a linear line, making the sweep accelerate exponentially as it approaches the drop. At Bar 9.0 (the drop), it instantly returns to 20kHz.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Subtractive Arrangement | Multiple Media Items + MIDI Note Insertion | Allows us to clearly define "Verse" vs "Chorus" blocks and programatically omit kicks/hats from the verse item. |
| Harmony/Chords | Programmatic Scale Degree Lookup | Ensures the generated chords always fit the user-provided key/scale parameters perfectly. |
| Filter Transition | ReaEQ + Parameter Automation Envelope | Replicates the exact tool used in the tutorial. By dropping Band 4's gain and automating its frequency, we build a native filter sweep without third-party plugins. |
| Curve Shaping | `RPR_InsertEnvelopePoint` (`shape=2`) | The shape parameter `2` creates the non-linear "slow start/end" parabolic curve the creator achieved by holding Alt while dragging the envelope. |

> **Feasibility Assessment**: 90% accurate to the tutorial's logic. We recreate the exact subtractive structure and the automated ReaEQ curve transition. The remaining 10% accounts for the fact that we use generated MIDI and standard `ReaSynth` tones rather than the specific proprietary drum samples and audio risers the creator dragged in.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Arrangement_Tutorial",
    track_name: str = "Beat Skeleton",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Arrangement (Verse -> Chorus) with a ReaEQ Filter Sweep Transition.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for created tracks.
        bpm: Tempo.
        key: Root note.
        scale: Scale type.
        bars: Total bars (16 recommended: 8 Verse, 8 Chorus).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # --- Music Theory Setup ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11]
    }
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # C3 base
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate full scale notes over 2 octaves
    scale_notes = [root_midi + interval + (oct * 12) for oct in range(2) for interval in scale_intervals]
    
    # Chord progression degrees (i - VI - III - VII)
    progression_degrees = [0, 5, 2, 6] 

    # --- Step 1: Initialize Timing ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    track_count = RPR.RPR_CountTracks(0)

    # --- Step 2: Create Chords Track & Filter Automation ---
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chord_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name} - Chords (Filtered)", True)
    
    # Add Synth and EQ
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1)
    
    # Configure ReaEQ Band 4 to act as a Low Pass (High Shelf with -inf gain)
    # Param 10 is Band 4 Gain. 0.0 is -inf dB.
    RPR.RPR_TrackFX_SetParam(chord_track, eq_idx, 10, 0.0) 
    
    # Create Envelope for Band 4 Freq (Param 9)
    env = RPR.RPR_GetFXEnvelope(chord_track, eq_idx, 9, True)
    
    # Filter Sweep Automation Points
    # 1.0 = ~24kHz (Fully Open), 0.2 = ~200Hz (Muffled)
    # Shape 2 = Slow start/end (Curved parabolic transition)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, 7.0 * bar_len, 1.0, 2, 0, False, True) # Start sweep down
    RPR.RPR_InsertEnvelopePoint(env, 8.0 * bar_len - 0.01, 0.2, 0, 0, False, True) # Hit bottom right before drop
    RPR.RPR_InsertEnvelopePoint(env, 8.0 * bar_len, 1.0, 0, 0, False, True) # Instantly open for Chorus
    RPR.RPR_Envelope_Sort(env)

    # Generate Chord MIDI Item (16 bars continuous)
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", 16 * bar_len)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    for i in range(8): # 8 blocks of 2 bars
        degree = progression_degrees[i % 4]
        # Build a basic triad from the scale
        chord_root = scale_notes[degree % len(scale_notes)]
        chord_third = scale_notes[(degree + 2) % len(scale_notes)]
        chord_fifth = scale_notes[(degree + 4) % len(scale_notes)]
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, (i * 2) * bar_len)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, ((i * 2) + 2) * bar_len)
        
        for note in [chord_root, chord_third, chord_fifth]:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, note, int(velocity_base * 0.8), False)

    # --- Step 3: Create Subtractive Drum Tracks ---
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    drum_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums", True)
    
    # Verse Drum Item (Bars 1-8): Subtractive logic (No kick, delayed hi-hats)
    verse_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(verse_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(verse_item, "D_LENGTH", 8 * bar_len)
    verse_take = RPR.RPR_AddTakeToMediaItem(verse_item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(verse_take, "P_NAME", "Verse (No Kick/Bass)", True)
    
    for b in range(8):
        bar_start = b * bar_len
        # Snare on 2 and 4 (plays entire verse)
        for beat in [1, 3]: 
            st = RPR.RPR_MIDI_GetPPQPosFromProjTime(verse_take, bar_start + (beat * beat_len))
            en = RPR.RPR_MIDI_GetPPQPosFromProjTime(verse_take, bar_start + (beat * beat_len) + (beat_len * 0.5))
            RPR.RPR_MIDI_InsertNote(verse_take, False, False, st, en, 0, 38, velocity_base, False)
            
        # Hats on 8th notes (only enter in the 2nd half of the verse, Bar 5-8)
        if b >= 4:
            for half_beat in range(8):
                st = RPR.RPR_MIDI_GetPPQPosFromProjTime(verse_take, bar_start + (half_beat * (beat_len * 0.5)))
                en = RPR.RPR_MIDI_GetPPQPosFromProjTime(verse_take, bar_start + (half_beat * (beat_len * 0.5)) + (beat_len * 0.25))
                RPR.RPR_MIDI_InsertNote(verse_take, False, False, st, en, 0, 42, int(velocity_base*0.7), False)

    # Chorus Drum Item (Bars 9-16): Full Energy (Adds Kicks)
    chorus_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(chorus_item, "D_POSITION", 8 * bar_len)
    RPR.RPR_SetMediaItemInfo_Value(chorus_item, "D_LENGTH", 8 * bar_len)
    chorus_take = RPR.RPR_AddTakeToMediaItem(chorus_item)
    RPR.RPR_GetSetMediaItemTakeInfo_String(chorus_take, "P_NAME", "Chorus (Full Energy)", True)

    for b in range(8):
        bar_start = (8 + b) * bar_len
        
        # Kick on 1 and 3.5
        for k_pos in [0, 2.5]:
            st = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (k_pos * beat_len))
            en = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (k_pos * beat_len) + (beat_len * 0.5))
            RPR.RPR_MIDI_InsertNote(chorus_take, False, False, st, en, 0, 36, velocity_base, False)
            
        # Snare on 2 and 4
        for beat in [1, 3]: 
            st = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (beat * beat_len))
            en = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (beat * beat_len) + (beat_len * 0.5))
            RPR.RPR_MIDI_InsertNote(chorus_take, False, False, st, en, 0, 38, velocity_base, False)
            
        # Hats on 8th notes
        for half_beat in range(8):
            st = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (half_beat * (beat_len * 0.5)))
            en = RPR.RPR_MIDI_GetPPQPosFromProjTime(chorus_take, bar_start + (half_beat * (beat_len * 0.5)) + (beat_len * 0.25))
            RPR.RPR_MIDI_InsertNote(chorus_take, False, False, st, en, 0, 42, int(velocity_base*0.7), False)

    RPR.RPR_UpdateArrange()

    return f"Created 16-bar subtractive arrangement at {bpm} BPM with automated ReaEQ filter transition at bar 8."
```
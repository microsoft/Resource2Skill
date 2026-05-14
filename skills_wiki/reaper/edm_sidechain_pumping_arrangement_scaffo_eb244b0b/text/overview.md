### 1. High-level Design Pattern Extraction

**Skill Name**: EDM Sidechain Pumping Arrangement Scaffold

* **Core Musical Mechanism**: Structural contrast and rhythmic volume ducking. The tutorial demonstrates how to build tension by separating an arrangement into a smooth, rhythm-less "Intro" and an energy-heavy "Verse/Drop." In the Drop, a 4-on-the-floor kick drum is introduced alongside a sidechain compressor that ducks the volume of the chords/melody on every quarter note, creating the quintessential EDM "pumping" or "breathing" effect.
* **Why Use This Skill (Rationale)**: The sidechain "pump" serves two crucial functions. First, it prevents frequency masking between the heavy kick drum and the synths, allowing the kick to punch through the mix. Second, psychoacoustically, the swelling recovery of the synth volume forces the listener to feel the 4/4 grid even when the kick isn't playing, creating an infectious, forward-driving groove. Combining this with an empty/sustained intro maximizes structural impact.
* **Overall Applicability**: Essential for Dance, EDM, Future Bass, House, and Synth-Pop. Used specifically when transitioning from a build-up/intro into a verse or drop where rhythmic energy needs to instantly maximize.
* **Value Addition**: Instead of a static loop, this skill encodes macro-arrangement logic (Intro vs. Drop) and standardizes the rhythmic pumping effect. While the video uses complex track routing and ReaComp, this skill uses MIDI CC11 (Expression) automation to achieve the exact same pumping groove deterministically and without plugin-specific parameter guesswork.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: ~125 BPM (Classic House/EDM tempo).
  - **Grid**: 4/4 time signature.
  - **Arrangement**: Split evenly. The first half is the Intro (sustained chords, no drums). The second half is the Drop (4-on-the-floor kick, pumping chords).
  - **Pumping Groove**: The synth volume drops to ~20% on the exact quarter note (1.1.00), sweeps rapidly up to 100% by the off-beat 8th note (1.1.50), and holds until the next beat.

* **Step B: Pitch & Harmony**
  - **Progression**: A classic 4-bar minor progression `i - VI - III - VII` (e.g., Cm - Ab - Eb - Bb), which provides an emotional, driving foundation perfect for dance music.
  - **Voicings**: Triads held for whole notes (one chord per bar) to leave room for the rhythmic pumping to be the star.

* **Step C: Sound Design & FX**
  - **Instruments**: Stock `ReaSynth` on both the Kick and Chords tracks as placeholders.
  - **FX Alternative**: Rather than setting up hidden ghost tracks and auxiliary audio routing for sidechain compression (which can fail if plugin indices change), the pumping effect is hardcoded directly into the chord's MIDI item using CC 11 (Expression) curves. This guarantees a perfect, artifact-free rhythmic pump.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arrangement Contrast | Split MIDI loop logic | Perfectly mirrors the "Intro -> Drop" block moving shown in the tutorial. |
| 4-on-the-floor Beat | MIDI Note Insertion | Standard trigger for EDM kicks. |
| Sidechain Pumping | MIDI CC 11 Automation | 100% reliable inside REAPER natively. Achieves the exact volume ducking effect taught via sidechain compression, but bypasses the fragility of configuring auxiliary track sends and compressor detector inputs via API. |

> **Feasibility Assessment**: 100% reproduction of the core musical and structural concepts (arrangement blocking and rhythmic pumping). Generic synth sounds are used as placeholders for the specific VSTs shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "EDM_Pumping",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates an EDM arrangement featuring an intro and a 'Drop' with a 4-on-the-floor kick 
    and a simulated sidechain pumping effect on the chords.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, etc.).
        scale: Scale type (major, minor).
        bars: Total number of bars (first half is Intro, second half is Drop).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # Music theory dictionaries
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # === 1. Setup Timing & Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    
    # Split arrangement
    intro_bars = max(1, bars // 2)
    drop_bars = bars - intro_bars

    # === 2. Create Tracks ===
    chords_trk_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(chords_trk_idx, True)
    chords_track = RPR.RPR_GetTrack(0, chords_trk_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)

    kick_trk_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(kick_trk_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_trk_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name}_Kick", True)

    # === 3. Generate Chords MIDI ===
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", bar_len * bars)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    root_val = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)

    def get_chord_notes(degree):
        # Generates a triad based on the scale degree
        notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th of the chord
            idx = degree + i
            octave_shift = idx // scale_len
            note_val = root_val + scale_intervals[idx % scale_len] + (12 * octave_shift)
            notes.append(note_val)
        return notes

    # Classic EDM Progression: i - VI - III - VII (indices 0, 5, 2, 6 in minor)
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 3, 4, 5]

    for b in range(bars):
        chord_start = b * bar_len
        chord_end = chord_start + bar_len
        
        deg = progression[b % len(progression)]
        notes = get_chord_notes(deg)
        
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, chord_start)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, chord_end)
        
        for pitch in notes:
            # Shift extremely high notes down an octave for a thicker pad
            if pitch > 65:
                pitch -= 12
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, ppq_start, ppq_end, 0, int(pitch), velocity_base, False)

    # === 4. Insert Sidechain Pumping Effect (CC 11 Expression) ===
    # We apply the pump only during the drop phase
    for b in range(intro_bars, bars):
        for beat in range(beats_per_bar):
            beat_start_time = b * bar_len + beat * beat_len
            
            # Pumping timing points
            t_hit = beat_start_time                # Kick hits (volume drops)
            t_ramp = beat_start_time + (beat_len * 0.25) # 16th note (ramping up)
            t_up = beat_start_time + (beat_len * 0.5)    # 8th note offbeat (fully recovered)
            t_hold = beat_start_time + (beat_len * 0.95) # Hold before next kick
            
            ppq_hit = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_hit)
            ppq_ramp = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_ramp)
            ppq_up = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_up)
            ppq_hold = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_hold)

            # Insert CC 11 (Expression) - msg2=11
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_hit, 0xB0, 0, 11, 20)  # Ducked heavily
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_ramp, 0xB0, 0, 11, 80) # Swoop curve
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_up, 0xB0, 0, 11, 127)  # Fully back
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_hold, 0xB0, 0, 11, 127)

    RPR.RPR_MIDI_Sort(chords_take)

    # === 5. Generate Drop Kick MIDI ===
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", intro_bars * bar_len)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", drop_bars * bar_len)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    for b in range(intro_bars, bars):
        for beat in range(beats_per_bar):
            kick_start = b * bar_len + beat * beat_len
            kick_end = kick_start + 0.15 # Short, punchy kick note
            
            ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, kick_start)
            ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, kick_end)
            
            # C2 (36) is standard kick drum trigger mapping
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, ppq_start, ppq_end, 0, 36, 120, False)

    RPR.RPR_MIDI_Sort(kick_take)

    # === 6. Add Instruments (ReaSynth Placeholders) ===
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)

    return f"Created EDM Arrangement '{track_name}': {intro_bars} bars Intro, {drop_bars} bars Drop with pumping rhythm at {bpm} BPM."
```
### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Pumping Chords Build-Up

* **Core Musical Mechanism**: This pattern establishes forward momentum by combining two core EDM arrangement techniques: a rhythmic "sidechain ducking" effect and an opening low-pass filter sweep. A ghost kick (muted trigger) forces the volume of the chord progression to dip on every quarter-note beat. Simultaneously, the filter slowly opens, letting higher frequencies bleed in over the duration of the phrase.
* **Why Use This Skill (Rationale)**: 
  * *Psychoacoustics of the Filter Sweep*: Gradually introducing high frequencies creates rising excitement and tension because human ears perceive brightness as proximity and energy. 
  * *Groove Implication*: The sidechain pump provides a strong, syncopated rhythmic framework (the "off-beat") even when the main drums are absent, giving the listener a physical sense of the groove before the drop hits.
* **Overall Applicability**: Used extensively in electronic dance music (House, Trance, Future Bass) for intro builds, breakdowns, and bridges where you need to build energy leading into a massive drop.
* **Value Addition**: Provides a fully routed dual-track architecture containing a diatonic chord generator, an automated EQ filter sweep, and the complete send/receive structure required for true sidechain compression.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time signature: 4/4
  * BPM: 120-128 (default 125)
  * The Chords hold sustained whole-notes (one chord per bar).
  * The Sidechain Trigger plays a rigid 1/16th note on every downbeat (quarter note) to act as a 4-on-the-floor trigger.

* **Step B: Pitch & Harmony**
  * Generates a foundational 4-bar chord progression using diatonic triads.
  * For Major: I - V - vi - IV
  * For Minor: i - VI - III - VII
  * MIDI notes are strictly computed from scale intervals, guaranteeing in-key harmonization.

* **Step C: Sound Design & FX**
  * **Chords Track**: Uses `ReaSynth` blended with a saw wave for harmonic richness. Routed into `ReaEQ` and `ReaComp`.
  * **ReaEQ**: Band 4 (High Shelf) is repurposed as a Low-Pass filter by dropping its gain to -24dB and automating the frequency.
  * **Trigger Track**: Muted from the master output (`B_MAINSEND` = 0). Uses `ReaSynth` with a fast release to generate a short, percussive click.

* **Step D: Mix & Automation**
  * **Sidechain Routing**: The Trigger track is routed directly into channels 3/4 of the Chords track.
  * **Automation**: An envelope is generated on ReaEQ's Band 4 Frequency, sweeping from a muffled 20% (approx. 400Hz) to a wide-open 90% (approx. 10kHz) over the course of the 4 bars.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sidechain trigger & routing | Track routing (`I_DSTCHAN=2`) & `ReaComp` | Authentically recreates the exact ghost-kick sidechain method demonstrated in the tutorial. |
| Filter Sweep | `GetFXEnvelope` & `InsertEnvelopePoint` | Replicates the automated EQ filter movement that drives the arrangement's tension. |
| Harmony generation | MIDI note insertion | Dynamically generates a diatonic chord progression rather than relying on static, hardcoded notes. |

> **Feasibility Assessment**: 95% — The structural routing, MIDI generation, and EQ automation are perfectly reproduced natively in ReaScript. The only manual step required is selecting "Auxiliary Input L+R" in the ReaComp dropdown, as the detector UI dropdown is not exposed as a standard float parameter in the Reaper API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create EDM Pumping Chords Build-Up in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the main chords track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
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

    def get_chord_notes(root_note, scale_intervals, degree):
        notes = []
        for offset in [0, 2, 4]:  # Build triad
            idx = degree + offset
            octave_shift = idx // len(scale_intervals)
            rem_idx = idx % len(scale_intervals)
            note = root_note + scale_intervals[rem_idx] + (octave_shift * 12)
            notes.append(note)
        return notes

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Chords Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    # Enable 4 channels for sidechain routing
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # === Step 3: Create Ghost Trigger Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    trigger_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trigger_track, "P_NAME", "SC Trigger (Ghost)", True)
    # Mute the trigger track from the master mix
    RPR.RPR_SetMediaTrackInfo_Value(trigger_track, "B_MAINSEND", 0)

    # === Step 4: Route Trigger to Chords (Channels 3/4) ===
    send_idx = RPR.RPR_CreateTrackSend(trigger_track, chords_track)
    # Category 0 = Send, I_DSTCHAN 2 = Destination channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_DSTCHAN", 2)

    # === Step 5: Add FX to Chords Track ===
    synth_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, synth_idx, 1, 0.8) # Blend in Saw wave

    eq_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1)
    # Parameter 10 is Band 4 (High Shelf) Gain. Setting to 0.0 acts as a -24dB Low Pass
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, eq_idx, 10, 0.0) 

    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    # Aggressive pumping settings
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_idx, 0, 0.4) # Threshold
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_idx, 1, 0.1) # Ratio (approx 4:1)
    
    # === Step 6: Generate Chords MIDI ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_base = NOTE_MAP.get(key, 0) + 48 # Base Octave 4
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 4, 5, 3] # Standard pop/EDM progression

    for i in range(bars):
        deg = progression[i % len(progression)]
        notes = get_chord_notes(root_base, SCALES.get(scale, SCALES["major"]), deg)
        
        start_time_sec = i * bar_length_sec
        end_time_sec = start_time_sec + bar_length_sec
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time_sec)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        for note in notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Generate Ghost Trigger MIDI & FX ===
    trig_synth_idx = RPR.RPR_TrackFX_AddByName(trigger_track, "ReaSynth", False, -1)
    # Param 3 is Release. Set to 0.0 for a short percussive blip
    RPR.RPR_TrackFX_SetParamNormalized(trigger_track, trig_synth_idx, 3, 0.0)

    trig_item = RPR.RPR_AddMediaItemToTrack(trigger_track)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_LENGTH", total_length)
    trig_take = RPR.RPR_AddTakeToMediaItem(trig_item)

    # 4-on-the-floor pattern
    for i in range(bars * 4): 
        start_time_sec = i * (60.0 / bpm)
        end_time_sec = start_time_sec + (60.0 / bpm / 4) # 1/16th note length
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time_sec)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(trig_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(trig_take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(trig_take, False, False, start_ppq, end_ppq, 0, 36, 127, False)
        
    RPR.RPR_MIDI_Sort(trig_take)

    # === Step 8: Automate EQ Filter Cutoff ===
    # Get envelope for ReaEQ Band 4 Freq (Parameter Index 9)
    env = RPR.RPR_GetFXEnvelope(chords_track, eq_idx, 9, True)
    if env:
        # Start muffled
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True)
        # Sweep wide open at the end of the phrase
        RPR.RPR_InsertEnvelopePoint(env, total_length, 0.9, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' and SC Trigger over {bars} bars at {bpm} BPM. NOTE: Open ReaComp on '{track_name}' and set 'Detector Input' to 'Auxiliary Input L+R' to activate the sidechain."
```
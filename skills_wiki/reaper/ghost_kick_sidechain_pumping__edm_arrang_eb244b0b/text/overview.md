### 1. High-level Design Pattern Extraction

> **Skill Name**: Ghost Kick Sidechain Pumping (EDM Arrangement)

* **Core Musical Mechanism**: Creating rhythmic motion in sustained, static musical elements (like pads or chords) by using an inaudible, muted "ghost" drum track to trigger a sidechain compressor on the target track. This creates a signature "pumping" or "ducking" effect on every downbeat.
* **Why Use This Skill (Rationale)**: In electronic music, the 4-on-the-floor kick pulse is the track's heartbeat. During intros, breakdowns, or verses, producers often mute the main kick drum to drop the energy level. By applying sidechain compression triggered by an unheard ghost kick, the mix retains its danceable, momentum-driving groove even without percussion playing. It prevents the mix from feeling stagnant and builds anticipation for the drop when the main drums finally return.
* **Overall Applicability**: Essential for EDM, House, Future Bass, and modern Pop. It is used primarily on pads, sustained piano chords, thick sub-basses, and noise risers during drum-less sections to glue the arrangement to the tempo grid.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes advanced DAW routing (multichannel tracks, hardware sends) and dynamic processing (sidechain compression) directly into the session. It instantly provides a polished, genre-appropriate groove to plain MIDI chords.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, standard House tempo (120-128 BPM).
  - **Rhythm**: A strict 4-on-the-floor grid (quarter notes). The compressor ducks the volume exactly on the beat (1, 2, 3, 4) and swells back up on the upbeats (the "and").
  - **Note Duration**: The trigger notes are extremely short staccato 16th notes. The target chords are long, sustained whole notes covering the entire bar.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Diatonic triads built dynamically from the provided key and scale.
  - **Progression**: A standard foundational electronic loop moving from the tonic to the subdominant/dominant (e.g., i - iv - v - i) to ensure movement beneath the pumping effect.

* **Step C: Sound Design & FX**
  - **Ghost Kick Track**: Uses `ReaSynth` tuned low with a short release to create a brief, clicky thud. Crucially, the track's Master Send is disabled so it makes no sound in the final mix.
  - **Target Track (Pumping Synth)**: Uses `ReaSynth` with a long attack and release to emulate a soft pad. 
  - **FX Chain (ReaComp)**: Added to the Target Track. `Threshold` set very low (-30dB), `Ratio` high (10:1), `Attack` very fast (5ms) to catch the immediate transient of the ghost kick, and `Release` medium (150ms) so the volume swells back up musically in time with the tempo. The `Detector Input` is set to Aux L/R.

* **Step D: Mix & Automation**
  - **Routing**: The Target Track is converted to a 4-channel track. A hardware send is created from the Ghost Kick track (channels 1/2) routing directly to the Target Track's sidechain inputs (channels 3/4). 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Muted Ghost Trigger | MIDI notes + Routing (Master Send Off) | Creates an accurate, sample-independent control signal without polluting the mix. |
| Sustained Chords | MIDI note insertion | Computes diatonic scale degrees to provide the musical material being compressed. |
| Pumping Effect | FX Chain (ReaComp) + Track Send | Mathematically reproduces the sidechain compression routing architecture demonstrated in the tutorial. |

> **Feasibility Assessment**: 100%. All sidechain routing, multi-channel track configuration, parameter mapping, and MIDI generation can be reliably constructed using stock REAPER plugins (`ReaSynth`, `ReaComp`) and the native ReaScript API. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "PumpingChords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Ghost Kick Sidechain Pumping in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created target track.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # 2a. Create Ghost Kick Track
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    ghost_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", f"{track_name} Ghost Trigger", True)
    
    # Disable Master/Parent send so the kick is purely a control signal
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0)
    
    # 2b. Create Target Track
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    target_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(target_track, "P_NAME", f"{track_name} Pad", True)
    
    # Set target track to 4 channels to accept sidechain input on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(target_track, "I_NCHAN", 4)

    # === Step 3: Setup Routing ===
    # Send from Ghost Kick (ch 1/2) to Target (ch 3/4)
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, target_track)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2) # 2 corresponds to channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "D_VOL", 1.0)   # Unity gain

    # === Step 4: Add FX Chains ===
    # Add a simple synth to act as the ghost click
    RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    
    # Add target synth and compressor
    synth_idx = RPR.RPR_TrackFX_AddByName(target_track, "ReaSynth", False, -1)
    
    comp_idx = RPR.RPR_TrackFX_AddByName(target_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 0, -30.0) # Threshold (deep cut)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 1, 10.0)  # Ratio (hard compression)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 2, 5.0)   # Attack (catch transient fast)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 3, 150.0) # Release (rhythmic swell)
    RPR.RPR_TrackFX_SetParam(target_track, comp_idx, 8, 1.0)   # Detector Input: 1.0 maps to Aux L/R (Sidechain)

    # === Step 5: Add MIDI Items ===
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars

    # --- 5a. Ghost Kick MIDI ---
    ghost_item = RPR.RPR_AddMediaItemToTrack(ghost_track)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(ghost_item, "D_LENGTH", item_length)
    ghost_take = RPR.RPR_AddTakeToMediaItem(ghost_item)
    
    # Insert 4-on-the-floor trigger notes
    for i in range(bars * beats_per_bar):
        start_t = cursor_pos + i * beat_len_sec
        end_t = start_t + (beat_len_sec * 0.1) # extremely short trigger
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, start_t)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, end_t)
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, s_ppq, e_ppq, 0, 36, 127, False)
    
    RPR.RPR_MIDI_Sort(ghost_take)

    # --- 5b. Target Track MIDI (Chords) ---
    target_item = RPR.RPR_AddMediaItemToTrack(target_track)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_LENGTH", item_length)
    target_take = RPR.RPR_AddTakeToMediaItem(target_item)

    # Determine robust root MIDI note
    root_midi = 60
    for k, v in NOTE_MAP.items():
        if k.lower() == key.lower():
            root_midi = v + 48 # Start around C3
            break

    # Generate scale degrees across 3 octaves
    scale_steps = SCALES.get(scale.lower(), SCALES["minor"])
    full_scale = []
    for oct in range(3):
        for step in scale_steps:
            full_scale.append(root_midi + step + (12 * oct))

    # Simple chord progression based on scale degrees (e.g., i - iv - v - i)
    prog = [0, 3, 4, 0]

    # Insert sustained chords
    for bar in range(bars):
        deg = prog[bar % len(prog)]
        # Build diatonic triad (root, 3rd, 5th)
        chord_pitches = [full_scale[deg], full_scale[deg+2], full_scale[deg+4]]
        
        start_t = cursor_pos + bar * bar_length_sec
        end_t = start_t + bar_length_sec
        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, start_t)
        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, end_t)
        
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(target_take, False, False, s_ppq, e_ppq, 0, pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(target_take)
    RPR.RPR_UpdateArrange()

    return f"Created Sidechain Pumping configuration on '{track_name}' over {bars} bars at {bpm} BPM."
```
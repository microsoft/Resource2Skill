### 1. High-level Design Pattern Extraction

> **Skill Name**: Ghost Kick Sidechain Pumping

* **Core Musical Mechanism**: The tutorial demonstrates using a dedicated, muted "ghost" drum track to trigger a sidechain compressor on sustained instruments (like piano chords, synths, or pads). Because the ghost kick track does not route its audio to the master output, its sole purpose is to act as an invisible rhythmic trigger, creating a rhythmic "ducking" or "pumping" effect.
* **Why Use This Skill (Rationale)**: This is a quintessential EDM, house, and future bass production technique. Musically, it creates syncopated rhythmic movement inside otherwise static, sustained harmonies. Techncially, it carves out psychoacoustic "space" in the mix, ensuring that whenever the kick drum hits, competing frequencies from synths are instantly ducked, preventing muddiness and masking. Using a "ghost" trigger allows the pumping groove to remain consistent even if the audible drum pattern changes or drops out.
* **Overall Applicability**: Essential for EDM drops, moving pad sections, huge supersaw chords, or continuous rolling basslines. 
* **Value Addition**: This skill moves beyond placing MIDI notes by encoding actual DAW signal flow and multi-track routing. It automates the complex setup of expanding channel counts, configuring inter-track audio sends, disabling master parent sends, and parameterizing a stock compressor.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: ~120-130 BPM (125 BPM visible in the tutorial).
  - **Rhythm**: The ghost kick plays a strict 4-on-the-floor pattern (1/4 notes).
  - **Note Duration**: The target chords are played as long, sustained legato whole-notes spanning entire bars to heavily contrast with the pumping effect.

* **Step B: Pitch & Harmony**
  - The sidechain technique is agnostic to pitch, but applied here to a sustained triad chord progression. 
  - The script will dynamically generate a root-position triad based on the provided `key` and `scale`.

* **Step C: Sound Design & FX**
  - **Ghost Track**: Uses a short, transient sound (ReaSynth) to trigger the compressor fast.
  - **Target Track**: Uses a sustained sound (ReaSynth).
  - **FX Chain**: ReaComp placed on the Target Track. 
  - **Routing**: The Ghost track is muted from the Master (`B_MAINSEND = 0`) and sends its audio (channels 1/2) to the Auxiliary Inputs (channels 3/4) of the Target track.

* **Step D: Mix & Automation**
  - **Compressor Settings**: High ratio (e.g., 4:1 to 8:1), fast attack (0-5ms), medium-fast release (100ms) to snap the volume back up rhythmically, and a low threshold to ensure aggressive gain reduction on every kick hit.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Four-on-the-floor pattern | MIDI note insertion | Precise generation of quarter-note trigger rhythms. |
| Sustained Chords | MIDI note insertion | Provides the continuous signal required to hear the ducking effect. |
| Ghost Kick Trigger | Track Routing API | Demonstrates the exact technique taught: using a duplicated, master-muted track sending audio directly to another track's auxiliary channels. |
| Pumping Effect | ReaComp (FX Chain) | Standard REAPER dynamic processor capable of auxiliary sidechaining. |

> **Feasibility Assessment**: 85% — The structural routing, MIDI generation, channel configuration, and FX insertion are fully reproduced natively. Because REAPER does not expose the "Detector Input" dropdown in ReaComp via standardized, cross-version named variables, the script routes the audio perfectly to channels 3/4, but the user may need to manually click "Auxiliary Input L+R" inside the ReaComp GUI window for the compression to fully listen to the sidechain. The exact third-party piano VST from the video is replaced with native ReaSynth.

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
    Create a Ghost Kick Sidechain Pumping setup in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the target sustained track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created routing and patterns.
    """
    import reaper_python as RPR

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

    # === Step 1: Set Tempo & Calculate Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    ppq_per_qn = 960

    # === Step 2: Create Ghost Kick Track ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    ghost_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_track, "P_NAME", "Ghost Kick (Sidechain Trigger)", True)
    
    # Disable master send so it acts purely as a silent trigger
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0)
    
    # Add a basic synth to generate the audio pulse
    RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    
    # Create MIDI item for 4-on-the-floor ghost kick
    ghost_item = RPR.RPR_CreateNewMIDIItemInProj(ghost_track, 0.0, item_length, False)
    ghost_take = RPR.RPR_GetActiveTake(ghost_item)
    
    kick_pitch = 36 # C2
    for b in range(bars):
        for q in range(4): # Quarter notes
            start_ppq = (b * 4 + q) * ppq_per_qn
            end_ppq = start_ppq + int(ppq_per_qn * 0.25) # Short transient pulse
            RPR.RPR_MIDI_InsertNote(ghost_take, False, False, start_ppq, end_ppq, 0, kick_pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(ghost_take)

    # === Step 3: Create Target Track (Sustained Chords) ===
    target_idx = track_count + 1
    RPR.RPR_InsertTrackAtIndex(target_idx, True)
    target_track = RPR.RPR_GetTrack(0, target_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(target_track, "P_NAME", track_name, True)
    
    # Enable 4 track channels to receive sidechain audio on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(target_track, "I_NCHAN", 4)
    
    # Add synth for sustained sound
    RPR.RPR_TrackFX_AddByName(target_track, "ReaSynth", False, -1)
    
    # Add Compressor
    reacomp_idx = RPR.RPR_TrackFX_AddByName(target_track, "ReaComp", False, -1)
    
    # Set standard pumping settings 
    RPR.RPR_TrackFX_SetParam(target_track, reacomp_idx, 0, 0.05) # Low Threshold
    RPR.RPR_TrackFX_SetParam(target_track, reacomp_idx, 1, 0.8)  # High Ratio (approx 8:1)
    RPR.RPR_TrackFX_SetParam(target_track, reacomp_idx, 2, 0.0)  # Fast Attack
    RPR.RPR_TrackFX_SetParam(target_track, reacomp_idx, 3, 0.1)  # Medium Release
    
    # === Step 4: Route Ghost Kick to Target Track ===
    # Send from Ghost Kick (Category 0 = Send)
    send_idx = RPR.RPR_CreateTrackSend(ghost_track, target_track)
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_SRCCHAN", 0) # Source: Channels 1/2
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "I_DSTCHAN", 2) # Dest: Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(ghost_track, 0, send_idx, "D_VOL", 1.0)   # Send Volume at 0dB

    # === Step 5: Create Sustained MIDI for Target Track ===
    target_item = RPR.RPR_CreateNewMIDIItemInProj(target_track, 0.0, item_length, False)
    target_take = RPR.RPR_GetActiveTake(target_item)
    
    root_val = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    chord_pitches = [
        root_val + 48 + scale_intervals[0], 
        root_val + 48 + scale_intervals[2], 
        root_val + 48 + scale_intervals[4]
    ]
    
    for b in range(bars):
        start_ppq = b * 4 * ppq_per_qn
        end_ppq = (b + 1) * 4 * ppq_per_qn - 120 # Sustained for the whole bar with a slight gap
        for p in chord_pitches:
            RPR.RPR_MIDI_InsertNote(target_take, False, False, start_ppq, end_ppq, 0, p, int(velocity_base * 0.8), False)
            
    RPR.RPR_MIDI_Sort(target_take)
    RPR.RPR_UpdateArrange()

    return f"Created Sidechain Pumping setup: '{track_name}' ducked by 'Ghost Kick' over {bars} bars at {bpm} BPM."
```
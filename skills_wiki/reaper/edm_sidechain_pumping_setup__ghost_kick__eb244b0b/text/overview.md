### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Sidechain Pumping Setup (Ghost Kick Trigger)

* **Core Musical Mechanism**: Utilizing a muted "ghost" drum track to trigger a sidechain compressor on sustained melodic elements (like chords or pads). This creates a rhythmic, breathing, or "pumping" volume envelope perfectly locked to the grid, imparting dynamic rhythm onto otherwise static sounds.
* **Why Use This Skill (Rationale)**: This is a foundational technique in modern electronic dance music (House, Trance, Future Bass). Technically, it prevents frequency masking between the heavy kick drum and the bass/synths. Psychoacoustically, it forces the groove of the drums into the harmony track. In arrangements with stripped-back drums (like the intros or verses discussed in the video), the invisible ghost kick maintains the danceable pulse even when the main drums are muted.
* **Overall Applicability**: Essential for drops, driving basslines, thick chord stacks, and creating anticipation in intro/build-up sections. 
* **Value Addition**: Encodes advanced REAPER routing (creating 4-channel tracks, setting up hardware-level track sends to channels 3/4, configuring ReaComp for Auxiliary detection) along with a tightly voice-led diatonic pad progression that beautifully highlights the pumping effect.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: 125 (Standard four-on-the-floor tempo).
  - **Ghost Kick**: 1/4 note pulse on beats 1, 2, 3, and 4.
  - **Chords**: Sustained whole notes, changing once per bar.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Minor (configurable).
  - **Progression**: `i - VI - III - VII` (The quintessential modern pop/EDM loop).
  - **Voice Leading**: Chord notes are algorithmically clamped to a tight octave range (G3 to G4) to create a dense, smooth pad sound without jarring jumps.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a bright Sawtooth pad with a slight release tail to fill the gaps between chord changes.
  - **Effect**: `ReaComp` placed after the synth.
  - **Sidechain config**: Detector input set to Auxiliary (channels 3/4). Threshold pulled down to -25dB, Ratio at 4:1, Attack fast (5ms) to catch the transient, Release tuned to the tempo (100ms) to allow the synth to swell back up before the next beat.
* **Step D: Mix & Automation**
  - The Ghost Kick track's Master/Parent send is disabled so it is never heard directly.
  - A track send routes the Ghost Kick's audio exclusively to destination channels 3/4 of the Chords track.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Melodic/Drum Rhythms | `RPR_MIDI_InsertNote` | Provides exact grid placement and duration control for the chords and triggers. |
| Pad Sound Design | `RPR_TrackFX_AddByName` (ReaSynth) | Native lightweight synth that perfectly demonstrates the harmonic pumping effect via a Sawtooth wave. |
| Pumping Effect | `RPR_TrackFX_AddByName` (ReaComp) + Track Sends | Replicates the exact sidechain routing architecture shown in the tutorial (Channels 1/2 -> 3/4 Aux). |

> **Feasibility Assessment**: 100% reproducible. Using REAPER's native ReaScript API, we can programmatically build the multi-channel tracks, the hidden audio send, the VST parameters, and the voice-led MIDI chords entirely from scratch without external dependencies.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Pumping_Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Sidechain Pumping Setup in the current REAPER project.
    Generates a muted ghost kick track that triggers ReaComp on a synthesized chord pad.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chords track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_pitches = [root_val + interval for interval in scale_intervals]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_count = RPR.RPR_CountTracks(0)
    
    # Track 1: Pumping Chords
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    chords_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4) # Enable 4 channels for sidechain

    # Track 2: Ghost Kick (Sidechain Trigger)
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick (Sidechain Trigger)", True)
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0) # Mute from master output

    # === Step 3: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    # Chord generator with tight voice-leading (clamps notes between G3 and G4)
    def get_chord(degree, root_octave):
        deg_idx = (degree - 1) % 7
        oct_shift = (degree - 1) // 7
        
        n1 = root_octave * 12 + scale_pitches[deg_idx] + oct_shift * 12
        n3 = root_octave * 12 + scale_pitches[(deg_idx + 2) % 7] + ((deg_idx + 2) // 7) * 12 + oct_shift * 12
        n5 = root_octave * 12 + scale_pitches[(deg_idx + 4) % 7] + ((deg_idx + 4) // 7) * 12 + oct_shift * 12
        
        chord = []
        for n in [n1, n3, n5]:
            while n > 67: # Max height G4
                n -= 12
            while n < 55: # Min height G3
                n += 12
            chord.append(n)
        return sorted(chord)

    # Insert Chords (Progression: i - VI - III - VII)
    for bar in range(bars):
        degree = [1, 6, 3, 7][bar % 4]
        chord_notes = get_chord(degree, 4)
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(chords_take, end_qn)
        
        for pitch in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)

    # Insert Ghost Kick (Quarter notes)
    for i in range(bars * 4):
        start_time = i * (60.0 / bpm)
        end_time = start_time + 0.1 # Short blip
        
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(kick_take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 1, 36, 127, False)

    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 4: Sound Design & Sidechain Routing ===
    
    # 4a. Add Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 6, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 7, 1.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 8, 0.0)   # Triangle mix
    RPR.RPR_TrackFX_SetParam(chords_track, synth_idx, 5, 200.0) # Release tail

    # 4b. Add Compressor
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 0, -25.0) # Threshold
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 1, 4.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 2, 5.0)   # Attack ms
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 3, 100.0) # Release ms
    RPR.RPR_TrackFX_SetParam(chords_track, comp_idx, 8, 1.0)   # Detector Input: Aux L+R

    # 4c. Route Trigger to Chords (Channels 3/4)
    send_idx = RPR.RPR_CreateTrackSend(kick_track, chords_track)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2) # 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)   # Unity Gain

    return f"Created pumping synth pad and sidechain trigger over {bars} bars at {bpm} BPM in {key} {scale}."
```
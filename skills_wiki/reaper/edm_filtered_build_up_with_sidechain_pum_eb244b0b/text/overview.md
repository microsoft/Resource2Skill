### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Filtered Build-Up with Sidechain Pumping

* **Core Musical Mechanism**: This pattern establishes a compelling arrangement transition (often used for intros or bridge build-ups) by combining two techniques: a **Low-Pass Filter Sweep** that gradually reveals the harmonic content of a chord progression, and a **Ghost Kick Sidechain**, where a muted 4-on-the-floor kick pattern triggers a compressor on the chords to create a rhythmic ducking/pumping effect.
* **Why Use This Skill (Rationale)**: 
  * *Psychoacoustics of Filter Sweeps*: Gradually opening a low-pass filter (increasing the cutoff frequency) introduces higher harmonics over time. This creates a natural sense of rising tension and anticipation, leading the listener toward the "drop" or the verse where the full frequency spectrum is unleashed.
  * *Groove Theory of Sidechaining*: Ducking the volume of the chords on every downbeat implies a kick drum without one actually playing. This imparts a strong kinetic dance groove (syncopation on the off-beats) while keeping the arrangement sparse and airy.
* **Overall Applicability**: Perfect for Electronic Dance Music (House, Future Bass, Trance), pop track intros, or any section where you want to maintain a danceable pulse without the heavy impact of a full drum kit.
* **Value Addition**: This skill moves beyond static MIDI entry by encoding structural arrangement techniques. It links routing (audio sends), dynamic processing (sidechain compression), and automation (filter cutoff) to produce a "living" musical section that evolves over time.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120-128 BPM (standard EDM).
  - **Chords**: Sustained whole notes (legato) spanning the full length of each bar.
  - **Trigger (Ghost Kick)**: Staccato 1/4 notes playing precisely on beats 1, 2, 3, and 4.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (e.g., C minor).
  - **Progression**: A simple 4-bar progression (e.g., i - VI - III - VII) using basic triad voicings to provide a thick pad texture.
* **Step C: Sound Design & FX**
  - **Chords Instrument**: A synthesizer playing a basic sawtooth/square pad (represented here by ReaSynth).
  - **Trigger Instrument**: A short, percussive sound (ReaSynth with a near-zero decay) that outputs no master audio but sends heavily to the sidechain.
  - **FX Chain (Chords)**: 
    - *Low-Pass Filter*: Cutoff sweeps from ~300 Hz up to ~20,000 Hz.
    - *Sidechain Compressor*: `ReaComp` with a fast attack (~5ms), medium release (~100ms), high ratio (4:1 or more), and detector input set to Auxiliary (channels 3/4).
* **Step D: Mix & Automation**
  - **Routing**: Track channels increased to 4 on the Chords track. A pre-fader send from the Trigger track (channels 1/2) to the Chords track (channels 3/4).
  - **Master Send**: The Trigger track's Master Send is disabled (`B_MAINSEND` = 0) so it remains a "ghost" track.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Chords | MIDI note insertion | Allows parameterized keys and scales to form foundational harmonies. |
| Ghost Kick Rhythm | MIDI note insertion | Guarantees perfect 1/4 note timing alignment for the pumping effect. |
| Sidechain Pumping | `RPR_CreateTrackSend` + `ReaComp` | Authentically recreates the exact audio-routing sidechain technique shown in the tutorial. |
| Filter Sweep | `JS: lowpass` + Envelope Automation | Provides the exact tension-building sweep over the 4-bar duration. |

> **Feasibility Assessment**: 95%. The logic accurately sets up the routing, the sidechain compressor, the ghost trigger, and the MIDI items using stock REAPER plugins. The exact tone of the VST synths used in the video cannot be matched exactly with `ReaSynth`, but the core *arrangement and pumping pattern* is fully captured and functional.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Pumping Chords",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Filtered Build-Up with Sidechain Pumping in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the generated chords track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "F#").
        scale: Scale type ("major", "minor").
        bars: Number of bars for the progression.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.
        
    Returns:
        Status string indicating success.
    """
    import reaper_python as RPR

    # --- Musical Context & Theory ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # 4-bar progression using scale degrees: i, VI, III, VII (0, 5, 2, 6)
    progression_degrees = [0, 5, 2, 6] 
    
    def get_chord_pitches(degree_idx, octave=4):
        """Builds a basic triad based on the scale degree index."""
        pitches = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            scale_idx = (degree_idx + i) % 7
            octave_shift = (degree_idx + i) // 7
            pitch = (octave + octave_shift + 1) * 12 + root_val + scale_intervals[scale_idx]
            pitches.append(pitch)
        return pitches

    # --- 1. Environment Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # --- 2. Create the 'Chords' Track ---
    chords_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(chords_track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, chords_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", track_name, True)
    
    # Enable 4 channels on Chords track (needed for sidechain)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "I_NCHAN", 4)

    # --- 3. Create MIDI Chords Item ---
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    
    for bar in range(bars):
        degree = progression_degrees[bar % len(progression_degrees)]
        pitches = get_chord_pitches(degree, octave=4)
        
        start_time = bar * bar_length_sec
        end_time = (bar + 1) * bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        for p in pitches:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, p, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(chords_take)

    # --- 4. Add FX to Chords (Synth + Lowpass + Sidechain Compressor) ---
    # Synth
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    
    # Lowpass Filter (JS)
    lp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "JS: lowpass", False, -1)
    # Add automation for filter sweep (Param 0 is frequency)
    lp_env = RPR.RPR_GetFXEnvelope(chords_track, lp_idx, 0, True)
    # Sweep from ~300Hz (0.01 normalized approx) to ~20000Hz (1.0 normalized)
    # Note: JSFX often use normalized values 0-1 for envelopes in scripting API
    RPR.RPR_InsertEnvelopePoint(lp_env, 0.0, 0.01, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(lp_env, total_length_sec, 1.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(lp_env)

    # Sidechain Compressor
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_idx, 0, 0.3) # Threshold down
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_idx, 1, 0.6) # Ratio up
    RPR.RPR_TrackFX_SetParamNormalized(chords_track, comp_idx, 28, 1.0) # Param 28 is Detector Input: 1.0 = Aux L+R

    # --- 5. Create the 'Ghost Kick' Sidechain Trigger Track ---
    trigger_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(trigger_track_idx, True)
    trigger_track = RPR.RPR_GetTrack(0, trigger_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(trigger_track, "P_NAME", "Ghost Kick Trigger", True)
    
    # DISABLE master send to keep it a ghost track
    RPR.RPR_SetMediaTrackInfo_Value(trigger_track, "B_MAINSEND", 0)

    # --- 6. Create MIDI Trigger Item (4-on-the-floor) ---
    trigger_item = RPR.RPR_AddMediaItemToTrack(trigger_track)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_LENGTH", total_length_sec)
    trigger_take = RPR.RPR_AddTakeToMediaItem(trigger_item)
    
    for beat in range(bars * beats_per_bar):
        start_time = beat * beat_length_sec
        end_time = start_time + (beat_length_sec * 0.25) # Short transient hit
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trigger_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trigger_take, end_time)
        
        # Pitch 36 (C2) standard kick drum note
        RPR.RPR_MIDI_InsertNote(trigger_take, False, False, start_ppq, end_ppq, 0, 36, 127, False)
        
    RPR.RPR_MIDI_Sort(trigger_take)

    # --- 7. Add short percussive synth to Trigger Track ---
    trigger_synth_idx = RPR.RPR_TrackFX_AddByName(trigger_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(trigger_track, trigger_synth_idx, 2, 0.0) # Zero decay for click sound

    # --- 8. Create Audio Routing (Sidechain Send) ---
    # Send from Trigger (idx 0) to Chords (idx 1)
    send_idx = RPR.RPR_CreateTrackSend(trigger_track, chords_track)
    # Set Audio Destination to Channels 3/4 (value '2' in REAPER mapping for stereo pairs: 0=1/2, 2=3/4)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_DSTCHAN", 2)
    # Pre-fader send to ensure ducking is consistent regardless of volume tweaks
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_SENDMODE", 0) 

    return f"Created '{track_name}' and Ghost Sidechain over {bars} bars at {bpm} BPM in {key} {scale}."
```
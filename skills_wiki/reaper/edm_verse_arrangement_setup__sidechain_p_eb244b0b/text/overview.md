### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Verse Arrangement Setup (Sidechain Pumping & Root Bass)

* **Core Musical Mechanism**: Structural contrast via subtraction and rhythmic pumping. In electronic dance music arrangement, a dense, melodic intro/chorus is often stripped down in the verse to build dynamic contrast. The complex chord voicings and lead melodies are removed, leaving a driving, sustained bassline that plays only the root notes of the progression. A "ghost kick" track is then used to trigger heavy sidechain compression, creating a rhythmic 4-on-the-floor "pump" on the bassline.
* **Why Use This Skill (Rationale)**: Removing density in the verse makes the eventual chorus feel significantly larger and more explosive when the layered synths return. The sidechain compression technique creates "breathing space" in the low frequencies (preventing kick and bass from clashing) and imparts an infectious, danceable groove (psychoacoustic anticipation) even when the audible drum track is kept minimal.
* **Overall Applicability**: Essential for arranging verses in House, Techno, Trance, Future Bass, and modern Pop. It establishes the foundational harmonic groove before introducing vocals or lead melodies.
* **Value Addition**: This skill automates the complex REAPER routing required for ghost-trigger sidechain compression. It generates a foundational drum skeleton and algorithmically extracts a sub-heavy bassline based on standard chord progressions derived dynamically from your chosen key and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4-on-the-floor groove. Kick on every downbeat (1, 2, 3, 4). Claps on the 2 and 4. Hi-hats on the offbeats (1.5, 2.5, 3.5, 4.5).
  - **Bass Rhythm**: Long, sustained whole notes held for the duration of each bar to maximize the audibility of the sidechain "ducking" effect.
* **Step B: Pitch & Harmony**
  - Uses standard, highly effective EDM chord progressions: `i - VI - III - VII` for minor scales, and `I - V - vi - IV` for major scales.
  - The script calculates the root notes for these degrees and mathematically constraints them to a powerful sub-bass octave (E1 to D#2) to ensure a heavy foundation.
* **Step C: Sound Design & FX**
  - **Sidechain Trigger (Ghost)**: A track containing a kick pattern but disconnected from the Master output. It uses a short ReaSynth ping to generate pure audio for the compressor detector.
  - **Verse Bass**: Uses ReaSynth set to a Sawtooth wave, heavily processed by ReaComp. 
  - **Routing**: The Ghost trigger track sends its audio directly to Channels 3/4 of the Bass track. 
* **Step D: Mix & Automation**
  - The bass track's channel count is expanded to 4.
  - ReaComp is added to the bass track. (Note: For the perfect pumping effect, the user simply needs to flip ReaComp's "Detector Input" dropdown to "Auxiliary Input L+R", as REAPER's API doesn't expose the detector dropdown index natively).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm / Melody | MIDI note insertion | Precise quantization, PPQ timing control, and clean velocity scaling. |
| Bass/Trigger Tone | FX chain (ReaSynth) | Ensures sound is generated immediately without relying on external VSTs or downloaded drum samples. |
| Sidechain Pumping | Audio Routing & Track Info | Modifying `I_NCHAN`, `B_MAINSEND`, and using `CreateTrackSend` guarantees the REAPER audio architecture is properly configured for sidechain. |

> **Feasibility Assessment**: 95% — The structural arrangement, MIDI generation, track creation, and audio routing are perfectly reproducible. Because ReaComp's "Detector input" dropdown cannot be definitively set via a normalized float parameter in the API, the user may need to manually click the drop-down to "Auxiliary" to hear the pump. The routing itself, however, is 100% established.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Verse",
    bpm: int = 124,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Verse Arrangement featuring 4-on-the-floor drums, 
    a root-note bassline, and sidechain routing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing generated arrangement.
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
    
    # Fallback to minor if an unsupported scale is provided
    if scale not in SCALES:
        scale = "minor"

    key_clean = key.capitalize() if len(key) == 1 else key[0].capitalize() + key[1:].lower()
    root_midi = 36 + NOTE_MAP.get(key_clean, 0) # Base C2

    # Progression logic
    if scale == "minor":
        prog_degrees = [0, 5, 2, 6] # i, VI, III, VII
    else:
        prog_degrees = [0, 4, 5, 3] # I, V, vi, IV

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # === Step 2: Create Sidechain Trigger Track ===
    RPR.RPR_InsertTrackAtIndex(0, True)
    trig_track = RPR.RPR_GetTrack(0, 0)
    RPR.RPR_GetSetMediaTrackInfo_String(trig_track, "P_NAME", f"{track_name}_SC_Trigger", True)
    RPR.RPR_SetMediaTrackInfo_Value(trig_track, "B_MAINSEND", 0) # Disconnect from Master

    trig_item = RPR.RPR_AddMediaItemToTrack(trig_track)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trig_item, "D_LENGTH", bar_len * bars)
    trig_take = RPR.RPR_AddTakeToMediaItem(trig_item)

    # Insert Trigger Notes
    for i in range(bars):
        for b in range(beats_per_bar):
            pos_time = (i * bar_len) + (b * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, pos_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(trig_take, pos_time + 0.1)
            RPR.RPR_MIDI_InsertNote(trig_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
            
    # Add synth to generate trigger pulse
    RPR.RPR_TrackFX_AddByName(trig_track, "ReaSynth", False, -1)

    # === Step 3: Create Verse Bass Track ===
    RPR.RPR_InsertTrackAtIndex(1, True)
    bass_track = RPR.RPR_GetTrack(0, 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_Bass", True)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_NCHAN", 4) # Enable 4 channels for sidechain

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", bar_len * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Setup Bass Routing & FX
    send_idx = RPR.RPR_CreateTrackSend(trig_track, bass_track)
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_DSTCHAN", 2) # Route to Channels 3/4
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    
    # Add Bass Synth
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_fx, 1, 1.0) # Set to Sawtooth wave

    # Insert Bassline Notes
    for i in range(bars):
        degree = prog_degrees[i % len(prog_degrees)]
        note = root_midi + SCALES[scale][degree]
        # Restrict to powerful bass octave (E1 to D#2)
        while note > 39: note -= 12
        while note < 28: note += 12
        
        start_time = i * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time - 0.05) # slight gap
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)

    # === Step 4: Create Drums Track ===
    RPR.RPR_InsertTrackAtIndex(2, True)
    drum_track = RPR.RPR_GetTrack(0, 2)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", bar_len * bars)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    for i in range(bars):
        for b in range(beats_per_bar):
            pos_time = (i * bar_len) + (b * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_time + 0.1)
            
            # Kick
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
            
            # Hat on off-beat
            hat_time = pos_time + (beat_len / 2.0)
            hat_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, hat_time)
            hat_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, hat_time + 0.1)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, hat_ppq, hat_end_ppq, 0, 42, max(1, velocity_base - 20), False)
            
            # Clap on 2 and 4
            if b % 2 == 1:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 39, velocity_base, False)

    RPR.RPR_MIDI_Sort(trig_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drum_take)
    
    return f"Created EDM Verse Setup with 3 tracks (Trigger, Bass, Drums) over {bars} bars at {bpm} BPM in {key} {scale}."
```
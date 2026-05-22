### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Subtractive Arrangement & Sidechain Tension Build

* **Core Musical Mechanism**: Transforming a dense "drop" loop into a full song structure using *subtractive arrangement* (stripping away elements to create verses/intros) and *dynamic tension* (using low-pass filter sweeps and sidechain compression). A muted "ghost kick" track runs continuously, triggering sidechain compression on the chords to maintain a rhythmic pumping feel even when the actual drums are muted.
* **Why Use This Skill (Rationale)**: 
  * **Energy Management**: Stripping back elements in the verse/intro creates contrast, making the subsequent drop feel larger and more impactful.
  * **Psychoacoustic Tension**: A low-pass filter sweeping upwards over time gradually introduces high frequencies, building anticipation and pushing the listener toward a climax.
  * **Rhythmic Groove**: Using sidechain compression on sustained elements (like piano chords or pads) imparts a distinct rhythmic bounce (swing) that locks them into the groove of the track, a staple characteristic of House and EDM.
* **Overall Applicability**: This technique is universally applied in electronic music structure (EDM, House, Future Bass, Pop). It takes an 8-bar or 4-bar core loop and extrapolates it across the timeline by manipulating presence (mutes) and timbre (filters).
* **Value Addition**: Encodes the structural knowledge of "Build -> Drop" and provides the exact routing architecture required to create persistent sidechain pumping without needing the actual kick drum to be audible.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 125 BPM (Classic House/EDM tempo).
  * **Grid**: 4/4 time signature.
  * **Arrangement Grid**: 8 Bars total. Bars 1-4 act as the Intro/Build (stripped back). Bars 5-8 act as the Chorus/Drop (full elements).
  * **Sidechain Rhythm**: A "ghost" kick plays on every downbeat (1/4 notes) continuously for all 8 bars to trigger the pumping effect.

* **Step B: Pitch & Harmony**
  * **Progression**: A ubiquitous EDM 4-chord progression: i - VI - III - VII (e.g., Am - F - C - G). 
  * **Voicings**: The chords are sustained (1 bar each), providing a continuous bed of sound for the sidechain compressor to rhythmically "carve" into.

* **Step C: Sound Design & FX**
  * **Instruments**: Synthesizers acting as Chords, Melody, Bass, and Kick.
  * **Ghost Routing**: The sidechain trigger track must have its "Master Send" disabled so it generates an audio control signal without being heard.
  * **Sidechain Compressor (ReaComp)**: Placed on the Chords. Detector input set to "Auxiliary L/R". Fast attack (0 ms), moderate release (~100 ms), low threshold, and high ratio to create an aggressive volume ducking effect on every quarter note.

* **Step D: Mix & Automation**
  * **Filter Sweep**: A Low-Pass filter (or High Shelf with gain pulled to `-inf`) is placed on the Chords track. The cutoff frequency is automated: starting low at Bar 1 and linearly ramping up to full frequency by Bar 5, opening up the sound exactly as the drop hits.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Arrangement Structure** | MIDI Item Positioning | Subtractive arrangement relies on placing items only in specific time zones (Bars 5-8 for the drop). |
| **Persistent Pumping** | ReaComp + Track Routing | Creating a ghost track with disabled Master Send routed to channels 3/4 of the target track is the native REAPER way to trigger sidechain. |
| **Tension Build** | FX Envelope Automation | Using `RPR_InsertEnvelopePoint` on ReaEQ's frequency parameter accurately replicates the filter sweep shown in the tutorial. |

> **Feasibility Assessment**: 95%. The logic accurately reproduces the subtractive arrangement, the track routing for the ghost sidechain, the ReaComp setup, and the filter sweep automation. Stock ReaSynth is used in place of the specific third-party VSTs shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM Arrangement",
    bpm: int = 125,
    key: str = "A",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Build-to-Drop arrangement demonstrating subtractive layout,
    ghost kick sidechaining, and low-pass filter tension sweeps.
    """
    import reaper_python as RPR

    # Note Map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root_midi = 48 + NOTE_MAP.get(key.upper(), 9) # Default A3

    # EDM Progression relative intervals (minor): i - VI - III - VII
    prog_intervals = [
        [0, 3, 7],     # i
        [8, 12, 15],   # VI
        [3, 7, 10],    # III
        [10, 14, 17]   # VII
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * 4
    half_bars = bars // 2  # e.g., 4 bars intro, 4 bars drop
    
    # Helper to create track
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        return tr, idx

    # ==========================================
    # 1. GHOST KICK (Sidechain Trigger)
    # ==========================================
    ghost_tr, ghost_idx = add_track("Ghost Kick (Trigger)")
    # Disable Master send (silent track)
    RPR.RPR_SetMediaTrackInfo_Value(ghost_tr, "B_MAINSEND", 0)
    RPR.RPR_TrackFX_AddByName(ghost_tr, "ReaSynth", False, -1)
    
    # Create MIDI for all 8 bars (Quarter notes)
    item_g = RPR.RPR_AddMediaItemToTrack(ghost_tr)
    RPR.RPR_SetMediaItemInfo_Value(item_g, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_g, "D_LENGTH", bar_sec * bars)
    take_g = RPR.RPR_AddTakeToMediaItem(item_g)
    
    for b in range(bars * 4): # Every beat
        pos = b * beat_sec
        RPR.RPR_MIDI_InsertNote(take_g, False, False, pos, pos + (beat_sec * 0.5), 1, 36, 120, False)

    # ==========================================
    # 2. CHORDS (Plays all 8 bars with automation)
    # ==========================================
    chords_tr, chords_idx = add_track("Chords (Pumping)")
    # Set to 4 channels to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(chords_tr, "I_NCHAN", 4)
    RPR.RPR_TrackFX_AddByName(chords_tr, "ReaSynth", False, -1)
    
    item_c = RPR.RPR_AddMediaItemToTrack(chords_tr)
    RPR.RPR_SetMediaItemInfo_Value(item_c, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_c, "D_LENGTH", bar_sec * bars)
    take_c = RPR.RPR_AddTakeToMediaItem(item_c)
    
    for bar in range(bars):
        pos = bar * bar_sec
        chord = prog_intervals[bar % 4]
        for note_offset in chord:
            p = root_midi + note_offset
            RPR.RPR_MIDI_InsertNote(take_c, False, False, pos, pos + bar_sec, 1, p, 90, False)

    # ROUTING: Ghost Kick (1/2) -> Chords (3/4)
    send_idx = RPR.RPR_CreateTrackSend(ghost_tr, chords_tr)
    RPR.RPR_SetTrackSendInfo_Value(ghost_tr, 0, send_idx, "I_DSTCHAN", 2) # 2 = Channels 3/4

    # SIDECHAIN COMPRESSOR
    comp_idx = RPR.RPR_TrackFX_AddByName(chords_tr, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_tr, comp_idx, 0, 0.2)  # Low Threshold
    RPR.RPR_TrackFX_SetParam(chords_tr, comp_idx, 1, 0.7)  # High Ratio
    RPR.RPR_TrackFX_SetParam(chords_tr, comp_idx, 14, 0.5) # Detector Input: Aux L/R
    
    # FILTER SWEEP AUTOMATION (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(chords_tr, "ReaEQ", False, -1)
    # Automate Band 4 Freq (Param 9)
    env = RPR.RPR_GetFXEnvelope(chords_tr, eq_idx, 9, True)
    drop_start_sec = half_bars * bar_sec
    # Points: start low (0.2), build up to fully open (1.0) right before drop
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, drop_start_sec, 1.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    # ==========================================
    # 3. DROP DRUMS (Plays only Bars 5-8)
    # ==========================================
    drums_tr, drums_idx = add_track("Drop Kick")
    RPR.RPR_TrackFX_AddByName(drums_tr, "ReaSynth", False, -1)
    
    item_d = RPR.RPR_AddMediaItemToTrack(drums_tr)
    RPR.RPR_SetMediaItemInfo_Value(item_d, "D_POSITION", drop_start_sec)
    RPR.RPR_SetMediaItemInfo_Value(item_d, "D_LENGTH", bar_sec * half_bars)
    take_d = RPR.RPR_AddTakeToMediaItem(item_d)
    
    for b in range(half_bars * 4): # Drop beat loop
        pos = drop_start_sec + (b * beat_sec)
        RPR.RPR_MIDI_InsertNote(take_d, False, False, pos, pos + (beat_sec * 0.25), 1, 36, 127, False)

    # ==========================================
    # 4. DROP BASS (Plays only Bars 5-8)
    # ==========================================
    bass_tr, bass_idx = add_track("Drop Bass")
    RPR.RPR_TrackFX_AddByName(bass_tr, "ReaSynth", False, -1)
    
    item_b = RPR.RPR_AddMediaItemToTrack(bass_tr)
    RPR.RPR_SetMediaItemInfo_Value(item_b, "D_POSITION", drop_start_sec)
    RPR.RPR_SetMediaItemInfo_Value(item_b, "D_LENGTH", bar_sec * half_bars)
    take_b = RPR.RPR_AddTakeToMediaItem(item_b)
    
    for bar in range(half_bars):
        pos = drop_start_sec + (bar * bar_sec)
        root = root_midi - 24 + prog_intervals[bar % 4][0] # Root note, 2 octaves down
        for beat in range(8): # 8th note rhythm
            b_pos = pos + (beat * (beat_sec / 2))
            RPR.RPR_MIDI_InsertNote(take_b, False, False, b_pos, b_pos + (beat_sec * 0.4), 1, root, 110, False)

    return f"Created {bars}-bar EDM structure at {bpm} BPM: Subtractive Drop, Sidechain Trigger, and Filter Build on Chords."
```
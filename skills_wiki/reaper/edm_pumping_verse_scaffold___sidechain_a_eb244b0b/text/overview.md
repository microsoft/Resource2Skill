### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Pumping Verse Scaffold & Sidechain Architecture

* **Core Musical Mechanism**: This pattern relies on **arrangement contrast through reduction**. It transitions from a dense, melodic section (like a chorus) into a stripped-down verse by removing the main melody and sustained pads. Instead, it leans entirely on a driving 8th-note bassline and heavily syncopated (3-3-2) chord stabs. Crucially, it sets up a **"Ghost Kick" sidechain architecture**, where a muted duplicate of the kick drum triggers a compressor on the bass and chords to create the signature EDM "pumping" volume envelope.
* **Why Use This Skill (Rationale)**: In electronic music, if every section is full of high-energy melodies, the listener experiences ear fatigue and drops lose their impact. By stripping the verse down to staccato, rhythmic elements, you create space in the frequency spectrum and build rhythmic tension. The sidechain pumping glues the bass and chords to the drum groove, adding forward momentum even when the arrangement is sparse.
* **Overall Applicability**: Perfect for the verse or build-up sections of 4-on-the-floor genres like House, Trance, Future Bass, or modern Pop.
* **Value Addition**: This skill not only generates a highly musical, rhythmically engaging MIDI progression but also automatically constructs the complex track routing required for native sidechain compression in REAPER.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120-128 BPM
  - **Time Signature**: 4/4
  - **Kick**: Straight quarter notes (4-on-the-floor).
  - **Bass**: Continuous driving 8th notes, with slight velocity accents on the off-beats.
  - **Chords**: Staccato stabs using a syncopated 3-3-2 sixteenth note rhythm (dotted-8th, dotted-8th, 8th) to leave breathing room for the kick.

* **Step B: Pitch & Harmony**
  - **Scale**: Minor (defaulting to A minor).
  - **Progression**: i - VI - III - VII (a classic EDM four-chord loop).
  - **Voicings**: Bass plays the root note in Octave 2. Chords play root position diatonic triads in Octave 4.

* **Step C: Sound Design & FX**
  - **Instruments**: `ReaSynth` is used as a native placeholder. The kick is shaped into a percussive blip (zero sustain, short decay), while the chords use a mix of sawtooth waves with a sharp decay to mimic an EDM stab.
  - **Sidechain FX**: `ReaComp` is added to the Bass and Chords tracks to process the pumping effect.

* **Step D: Mix & Automation**
  - A dedicated **"Ghost Kick" track** is created and its Master/Parent send is disabled (muted).
  - The Bass and Chord tracks are expanded to 4 audio channels.
  - Sends are created routing audio from channels 1/2 of the Ghost Kick into channels 3/4 of the Bass and Chords, preparing the exact architecture needed for the sidechain detector.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Verse Groove Construction | MIDI note insertion | Allows precise generation of the 3-3-2 syncopated chord stabs and driving 8th note bassline. |
| Ghost Kick Sidechaining | Track Creation & Routing API | `RPR_CreateTrackSend` and channel manipulation programmatically builds the complex sidechain routing architecture taught in the tutorial. |
| Instrument Setup | FX Chains (`ReaSynth`, `ReaComp`) | Provides immediate, self-contained audio playback without relying on external VSTs or sample files. |

> **Feasibility Assessment**: 90% reproducible. The arrangement logic, rhythmic MIDI generation, and sidechain routing architecture are perfectly reproduced using native ReaScript. The only missing 10% is the exact timbral character of the third-party synths used in the video, which we approximate using parameterized `ReaSynth` instances.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Verse",
    bpm: int = 125,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Pumping Verse Scaffold with Ghost Kick Sidechain routing.

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
        Status string describing the created arrangement and routing.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key.upper(), 9) # Default to A
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Standard EDM Progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6]

    # === Step 1: Set Tempo & Calculate Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    qn_duration = 60.0 / bpm
    bar_duration = qn_duration * 4

    # Helper: Create a track by name
    def create_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    # Helper: Create a MIDI item and return its take
    def create_midi_item(track, start_time, length):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        return RPR.RPR_AddTakeToMediaItem(item)

    # Helper: Insert a quantized MIDI note
    def insert_note(take, pos_sec, duration_sec, pitch, velocity):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec + duration_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # === Step 2: Main Kick Track ===
    kick_track = create_track(f"{track_name}_MainKick")
    kick_take = create_midi_item(kick_track, 0.0, bar_duration * bars)
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, 0, 1, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(kick_track, 0, 2, 0.05)  # Decay (Percussive)
    RPR.RPR_TrackFX_SetParam(kick_track, 0, 3, 0.0)   # Sustain

    # === Step 3: Ghost Kick Track (Muted, for Sidechain Triggering) ===
    ghost_track = create_track(f"{track_name}_GhostKick")
    RPR.RPR_SetMediaTrackInfo_Value(ghost_track, "B_MAINSEND", 0) # Mute Master Send
    ghost_take = create_midi_item(ghost_track, 0.0, bar_duration * bars)
    RPR.RPR_TrackFX_AddByName(ghost_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(ghost_track, 0, 1, 0.0)
    RPR.RPR_TrackFX_SetParam(ghost_track, 0, 2, 0.05)
    RPR.RPR_TrackFX_SetParam(ghost_track, 0, 3, 0.0)

    # Populate both kicks with 4-on-the-floor pattern
    for b in range(bars):
        for q in range(4):
            pos = b * bar_duration + q * qn_duration
            insert_note(kick_take, pos, qn_duration * 0.25, 36, velocity_base + 20)
            insert_note(ghost_take, pos, qn_duration * 0.25, 36, 127) # Max velocity for solid trigger

    # === Step 4: Driving 8th-Note Bass ===
    bass_track = create_track(f"{track_name}_Bass")
    bass_take = create_midi_item(bass_track, 0.0, bar_duration * bars)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.5)  # Sustain
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.5)  # Add Sawtooth harmonics

    for b in range(bars):
        degree_idx = progression_degrees[b % len(progression_degrees)]
        base_pitch = root_val + scale_intervals[degree_idx] + 36 # Octave 2
        
        for e in range(8):
            pos = b * bar_duration + e * (qn_duration / 2)
            # Accent off-beats slightly for extra groove
            vel = velocity_base if e % 2 == 0 else velocity_base + 10
            insert_note(bass_take, pos, qn_duration * 0.4, base_pitch, vel)

    # === Step 5: Syncopated Chord Stabs ===
    chord_track = create_track(f"{track_name}_Chords")
    chord_take = create_midi_item(chord_track, 0.0, bar_duration * bars)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 5, 1.0)  # Pure Sawtooth
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 1, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 2, 0.15) # Quick Decay
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 3, 0.0)  # No Sustain (Staccato)

    sn = qn_duration / 4
    # 3-3-2 sixteenth note syncopation per half-bar
    rhythm_offsets = [0, 3*sn, 6*sn, 8*sn, 11*sn, 14*sn]
    
    for b in range(bars):
        degree_idx = progression_degrees[b % len(progression_degrees)]
        
        root_pitch = root_val + scale_intervals[degree_idx] + 60 # Octave 4
        
        # Calculate diatonic third and fifth
        third_idx = (degree_idx + 2) % len(scale_intervals)
        fifth_idx = (degree_idx + 4) % len(scale_intervals)
        
        third_pitch = root_val + scale_intervals[third_idx] + 60
        if third_idx < degree_idx: third_pitch += 12 # Push up an octave if it wraps
        
        fifth_pitch = root_val + scale_intervals[fifth_idx] + 60
        if fifth_idx < degree_idx: fifth_pitch += 12
        
        for offset in rhythm_offsets:
            pos = b * bar_duration + offset
            for p in [root_pitch, third_pitch, fifth_pitch]:
                insert_note(chord_take, pos, sn * 1.5, p, velocity_base - 10)

    # === Step 6: Construct Sidechain Routing Architecture ===
    def setup_sidechain(src_track, dest_track):
        # Expand destination track to 4 audio channels
        RPR.RPR_SetMediaTrackInfo_Value(dest_track, "I_NCHAN", 4)
        # Add ReaComp
        RPR.RPR_TrackFX_AddByName(dest_track, "ReaComp", False, -1)
        # Create Send from Ghost Kick
        send_idx = RPR.RPR_CreateTrackSend(src_track, dest_track)
        # Route audio from channels 1/2 of source to channels 3/4 of destination (Value 2 = 3/4)
        RPR.RPR_SetTrackSendInfo_Value(src_track, 0, send_idx, "I_DSTCHAN", 2)
        # Set Send Volume to 0dB
        RPR.RPR_SetTrackSendInfo_Value(src_track, 0, send_idx, "D_VOL", 1.0)

    setup_sidechain(ghost_track, bass_track)
    setup_sidechain(ghost_track, chord_track)

    RPR.RPR_UpdateArrange()

    return f"Created EDM Verse Scaffold: 4 Tracks (Kick, Ghost Kick, Bass, Chords) over {bars} bars at {bpm} BPM with Sidechain Routing established."
```
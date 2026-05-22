# Quick-Start Songwriting Template & Starter Loop

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Quick-Start Songwriting Template & Starter Loop

* **Core Musical Mechanism**: Project templating and rapid harmonic/rhythmic prototyping. While the provided tutorial heavily focuses on DAW customization (preferences, actions, themes), its ultimate philosophical takeaway is to **avoid getting stuck in the "learning phase" and just jump in to create** (01:13). At 03:10, the video visually demonstrates a specific "Songwriting Layout." This skill extracts that concept by generating an instant multi-track songwriting template (Drums, Bass, Piano, Guitars, Vocals) and populating it with a generative diatonic chord progression and beat. 

* **Why Use This Skill (Rationale)**: "Blank canvas syndrome" is a major cause of procrastination. By instantly instantiating the track layout shown in the tutorial alongside a diatonic musical foundation (a standard I-V-vi-IV progression), the producer bypasses the configuration phase. This encodes the tutorial's core advice: prioritize creating over endlessly tweaking shortcuts.

* **Overall Applicability**: Use this when starting any new track to instantly bypass the setup phase and establish a playable, harmonically correct structural foundation.

* **Value Addition**: Transforms an empty REAPER project into a 5-track structured songwriting environment with a ready-to-play rhythmic and harmonic foundation that automatically adapts to your chosen key and scale.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Tempo**: 120 BPM (Parametric)
  - **Grid**: Basic 4-on-the-floor kick, backbeat snare, 8th-note hi-hats. The bass plays an aggressive 8th-note driving rhythm to keep momentum.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Fully parametric (defaults to C Major).
  - **Progression**: The classic pop/songwriting progression: `I - V - vi - IV` (or `i - v - VI - iv` in minor).
  - **Voicings**: Root position triads for the Piano/Synth pad, foundational root notes for the bassline. Note computation dynamically wraps octaves based on the scale degrees.

* **Step C: Sound Design & FX**
  - **Instruments**: Uses stock `ReaSynth` on the Bass and Piano tracks to ensure immediate audible playback without requiring third-party VSTs.
  - **Sound Shaping**: The chord track modifies ReaSynth parameters to roll off the Square wave, emphasize the Sawtooth wave, and increase the Attack/Release times to form a smooth background pad.
  - **Track Layout**: Matches the video's visual reference: DRUMS, BASS, PIANO, GTR RHYTHM, LEAD VOCAL.

* **Step D: Mix & Automation**
  - **Balancing**: Bass volume is dropped to 0.5 (-6dB) and the Chords to 0.3 (-10dB) to prevent digital clipping and leave headroom for live recording.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Structure Setup | `RPR_InsertTrackAtIndex` | Recreates the 5-track songwriting template shown visually in the video. |
| Rhythmic/Harmonic Base | MIDI note insertion | Provides an immediate musical context (drums, bassline, pad) to start writing over, avoiding a blank screen. |
| Basic Audibility | FX chain (`ReaSynth`) | Ensures the MIDI data generates immediate sound using REAPER's built-in synth. |

> **Feasibility Assessment**: 90%. While the tutorial is primarily about REAPER software preferences, this script successfully captures the specific "Songwriting Layout" shown at 03:10 and executes the creator's advice to "just jump in" by automatically generating a diatonic starting point. External VSTs from the video (like Kontakt or EZDrummer) are substituted with stock ReaSynth for maximum compatibility.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Songwriting_Template",
    track_name: str = "Song_Foundation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a multi-track Songwriting Template with a starter drum beat, bassline, 
    and diatonic chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused here, tracks are explicitly named.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and template.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

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

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Helper function to generate diatonic notes dynamically
    def get_note_by_degree(degree, root=root_val, intervals=scale_intervals, base_octave=4):
        octave_shift = degree // len(intervals)
        idx = degree % len(intervals)
        return (base_octave + octave_shift) * 12 + root + intervals[idx]

    # Target layout extracted from tutorial
    tracks_to_create = [
        {"name": "DRUMS", "type": "drums"},
        {"name": "BASS", "type": "bass"},
        {"name": "PIANO PAD", "type": "chords"},
        {"name": "GTR RHYTHM", "type": "audio"},
        {"name": "LEAD VOCAL", "type": "audio"}
    ]

    beats_per_bar = 4
    qn_length = 60.0 / bpm
    total_length_sec = (bars * beats_per_bar) * qn_length
    
    # Calculate offset so we are purely additive
    start_track_idx = RPR.RPR_CountTracks(0)

    for i, t_info in enumerate(tracks_to_create):
        idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        
        # Only populate tracks meant for MIDI
        if t_info["type"] in ["drums", "bass", "chords"]:
            item = RPR.RPR_AddMediaItemToTrack(track)
            RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
            RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
            take = RPR.RPR_AddTakeToMediaItem(item)
            
            # --- DRUMS ---
            if t_info["type"] == "drums":
                for bar in range(bars):
                    for beat in range(4):
                        start_sec = (bar * 4 + beat) * qn_length
                        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + (0.25 * qn_length))
                        
                        # 4-on-the-floor Kick
                        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
                        
                        # Backbeat Snare (beats 2 and 4)
                        if beat % 2 == 1:
                            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 38, velocity_base, False)
                        
                        # 8th note Hi-Hats
                        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 42, velocity_base - 10, False)
                        
                        hh2_start_sec = start_sec + (0.5 * qn_length)
                        hh2_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh2_start_sec)
                        hh2_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh2_start_sec + (0.25 * qn_length))
                        RPR.RPR_MIDI_InsertNote(take, False, False, hh2_start_ppq, hh2_end_ppq, 0, 42, velocity_base - 30, False)

            # --- BASS ---
            elif t_info["type"] == "bass":
                RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
                RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Prevent clipping
                
                progression_degrees = [0, 4, 5, 3] # I, V, vi, IV
                for bar in range(bars):
                    deg = progression_degrees[bar % len(progression_degrees)]
                    note = get_note_by_degree(deg, base_octave=2)
                    
                    # Driving 8th notes
                    for eighth in range(8):
                        start_sec = (bar * 4 + eighth * 0.5) * qn_length
                        s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                        e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + (0.4 * qn_length))
                        RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, note, velocity_base, False)
                        
            # --- CHORDS (PAD) ---
            elif t_info["type"] == "chords":
                RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
                # Tweak ReaSynth into a smoother Pad
                RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Square mix -> 0
                RPR.RPR_TrackFX_SetParam(track, 0, 1, 1.0) # Saw mix -> 1.0
                RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.5) # Attack -> 0.5s
                RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.5) # Release -> 0.5s
                RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.3)
                
                progression_degrees = [0, 4, 5, 3] # I, V, vi, IV
                for bar in range(bars):
                    deg = progression_degrees[bar % len(progression_degrees)]
                    
                    # Construct root position triad
                    notes = [get_note_by_degree(deg, base_octave=4),
                             get_note_by_degree(deg + 2, base_octave=4),
                             get_note_by_degree(deg + 4, base_octave=4)]
                             
                    start_sec = (bar * 4) * qn_length
                    s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                    e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + (4.0 * qn_length))
                    
                    for n in notes:
                        RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, n, velocity_base - 20, False)
            
            RPR.RPR_MIDI_Sort(take)

    return f"Created Songwriting Template with 5 tracks. Generated {bars} bars of starter loop in {key} {scale} at {bpm} BPM."
```
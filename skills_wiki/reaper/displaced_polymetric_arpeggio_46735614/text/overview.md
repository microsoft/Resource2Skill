# Displaced Polymetric Arpeggio

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Displaced Polymetric Arpeggio

* **Core Musical Mechanism**: The tutorial demonstrates a technique called a "displaced arpeggio" (or polymetric arpeggiation). Instead of playing block chords and applying a standard up/down arpeggiator that follows the chord changes perfectly, this technique relies on a **fixed, odd-length melodic sequence** (e.g., 7 notes long) that repeats endlessly over a standard **even-length chord progression** (e.g., a 4-bar loop).
* **Why Use This Skill (Rationale)**: This creates two profound musical effects:
    1. **Polymetric Rhythm**: A 7-step pattern played in 8th or 16th notes over a 4/4 time signature will shift its downbeat accent on every single repetition, creating rhythmic tension and forward momentum without changing tempo.
    2. **Harmonic Recontextualization**: Because the arpeggio notes remain static while the bass/chords underneath them change, the *function* of the arpeggio notes changes. A static "G" note might act as the Root when the bass plays G, but it becomes a floating 9th when the bass moves to F, and a suspended 4th when the bass moves to D. This creates complex, extended harmonies automatically.
* **Overall Applicability**: This technique is a staple in cinematic scoring, ambient electronic music, progressive house, and synthwave. It is perfect for turning a boring, static chord progression into a driving, evolving soundscape.
* **Value Addition**: Compared to a standard MIDI chord block, this skill encodes horizontal (linear) composition rather than vertical (block) composition. It separates the rhythm of the melody from the rhythm of the harmony, preventing the "cookie-cutter" sound of standard synth arpeggiators.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
    *   **Time Signature:** 4/4
    *   **Arpeggio Rhythm:** 1/16th notes or 1/8th notes. The sequence length is purposefully odd (7 steps).
    *   **Pad/Bass Rhythm:** Whole notes (1 chord per bar), providing a slow, grounded anchor to contrast the fast, shifting arpeggio.
* **Step B: Pitch & Harmony**
    *   **Arp Sequence:** Root, 5th, Octave, 5th, minor 3rd, 5th, 2nd (Scale degrees: 0, 4, 7, 4, 2, 4, 1). This utilizes strong intervals (roots and 5ths) with a few color notes (2nd, 3rd) so it doesn't clash when the chords change.
    *   **Pad Progression:** A standard minor progression: i - VI - III - VII (Scale degrees: 0, 5, 2, 6).
* **Step C: Sound Design & FX**
    *   **Arp Synth:** Plucky sound. Instant attack, short decay, zero sustain.
    *   **Pad Synth:** Lush sound. Slow attack, long release.
    *   **FX:** Delay on the arpeggio to enhance the rhythmic complexity; Reverb on the pad to push it to the background.
* **Step D: Mix & Automation**
    *   The Arp is kept relatively loud and dry, while the pad is tucked underneath.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Odd-length Arpeggio | MIDI Note Insertion (Math loop) | Allows us to create a true 7-step sequence that crosses bar lines, avoiding the limitations of stock arpeggiator plugins. |
| Slow Chord Progression | MIDI Note Insertion | Creates the vertical harmonic anchor on a separate track. |
| Pluck vs. Pad Tones | FX Chain (ReaSynth) + Parameters | ReaSynth's envelope parameters allow us to program a plucky arp (short ADSR) and a lush pad (long ADSR) using strictly native plugins. |
| Spatial Rhythms | FX Chain (ReaDelay) | Adding a dotted-eighth or standard 8th delay to a 16th-note polymetric arp creates beautiful cascading rhythms. |

> **Feasibility Assessment**: 90%. While we cannot reproduce the exact high-end Waldorf Iridium synthesizer used in the video, the REAPER native script perfectly reproduces the *compositional technique* (the displaced 7-step sequence over changing chords) and sets up the fundamental ADSR and Delay staging required to make it sound good.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "DisplacedArpProject",
    track_name: str = "Displaced_Arp",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a "Displaced Polymetric Arpeggio" pattern.
    Generates two tracks: A 7-step looping plucky arpeggio, and a 4-bar slow pad progression underneath.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, G, D#).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (should be a multiple of 4).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    if scale not in SCALES:
        scale = "minor"
    
    root_val = NOTE_MAP.get(key.capitalize(), 7) # Default G
    scale_intervals = SCALES[scale]

    # Helper function to convert scale degrees to absolute MIDI notes
    def get_midi_note(degree, octave=4):
        oct_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_val + ((octave + oct_shift) * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # ==========================================
    # === Step 2: Create Arpeggio Track (T1) ===
    # ==========================================
    track_idx_arp = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_arp, True)
    track_arp = RPR.RPR_GetTrack(0, track_idx_arp)
    RPR.RPR_GetSetMediaTrackInfo_String(track_arp, "P_NAME", f"{track_name}_Pluck", True)

    item_arp = RPR.RPR_AddMediaItemToTrack(track_arp)
    RPR.RPR_SetMediaItemInfo_Value(item_arp, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_arp, "D_LENGTH", item_length)
    take_arp = RPR.RPR_AddTakeToMediaItem(item_arp)

    # 7-step sequence (Root, 5th, Octave, 5th, 3rd, 5th, 2nd) represented in scale degrees
    arp_pattern_degrees = [0, 4, 7, 4, 2, 4, 1] 
    note_length_beats = 0.25 # 16th notes
    total_16th_notes = int(bars * beats_per_bar * 4)

    for i in range(total_16th_notes):
        degree = arp_pattern_degrees[i % len(arp_pattern_degrees)]
        pitch = get_midi_note(degree, octave=5)
        
        start_time = i * note_length_beats * (60.0 / bpm)
        end_time = start_time + (note_length_beats * (60.0 / bpm) * 0.8) # 80% gate length for pluck
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_arp, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_arp, end_time)
        
        # Add dynamic velocity based on position in the 7-step sequence to emphasize the polymeter
        vel = velocity_base if (i % 7 == 0) else velocity_base - 20
        
        RPR.RPR_MIDI_InsertNote(take_arp, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take_arp)

    # Add Plucky Synth & Delay to Arp
    synth_arp = RPR.RPR_TrackFX_AddByName(track_arp, "ReaSynth", False, -1)
    # Param 1: Attack (fast), Param 2: Decay (short), Param 3: Sustain (none), Param 4: Release (short)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 1, 0.0)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 2, 0.1)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 3, 0.0)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 4, 0.1)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 5, 0.7) # Square wave mix for bite

    delay = RPR.RPR_TrackFX_AddByName(track_arp, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track_arp, delay, 0, -6.0) # Wet mix

    # =======================================
    # === Step 3: Create Pad Track (T2)   ===
    # =======================================
    track_idx_pad = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_pad, True)
    track_pad = RPR.RPR_GetTrack(0, track_idx_pad)
    RPR.RPR_GetSetMediaTrackInfo_String(track_pad, "P_NAME", f"{track_name}_Pad", True)
    
    # Lower pad volume
    RPR.RPR_SetMediaTrackInfo_Value(track_pad, "D_VOL", 0.5) 

    item_pad = RPR.RPR_AddMediaItemToTrack(track_pad)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_LENGTH", item_length)
    take_pad = RPR.RPR_AddTakeToMediaItem(item_pad)

    # Progression: i - VI - III - VII (represented as root scale degrees)
    progression = [0, 5, 2, 6] 

    for bar in range(bars):
        root_degree = progression[bar % len(progression)]
        
        # Create a triad: Root, 3rd, 5th based on the current scale degree
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, end_time)
        
        for deg in chord_degrees:
            pitch = get_midi_note(deg, octave=3) # Play pad in lower octave
            RPR.RPR_MIDI_InsertNote(take_pad, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 15, False)

    RPR.RPR_MIDI_Sort(take_pad)

    # Add Lush Synth to Pad
    synth_pad = RPR.RPR_TrackFX_AddByName(track_pad, "ReaSynth", False, -1)
    # Slow attack, high sustain, slow release
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 1, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 2, 0.5) # Decay
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 3, 0.8) # Sustain
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 4, 0.6) # Release
    
    RPR.RPR_TrackFX_AddByName(track_pad, "ReaVerbate", False, -1)

    return f"Created Displaced Polymetric Arp setup ('{track_name}_Pluck' and '{track_name}_Pad') over {bars} bars in {key} {scale} at {bpm} BPM."
```
### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Build-up Filter Sweep (3-3-2 Syncopation)

* **Core Musical Mechanism**: This pattern automates a low-pass filter (or high-cut shelf) to gradually open up the frequency spectrum of a rhythmic chord progression. The chords themselves utilize a classic 3-3-2 (dotted-eighth, dotted-eighth, eighth) syncopation rhythm, driving energetic momentum forward. 
* **Why Use This Skill (Rationale)**: Filter sweeps play directly on psychoacoustics. Muffled, high-cut sounds feel distant or physically constrained. Gradually opening the filter creates a psychological sense of approaching proximity and expanding space, naturally building tension. Paired with a 3-3-2 rhythm that breaks the predictable 4/4 grid, the pattern creates a driving groove that leaves the listener craving the resolution of the drop.
* **Overall Applicability**: Perfect for Intros, Pre-choruses, and Build-ups in EDM, House, Future Bass, Pop, and Synthwave. 
* **Value Addition**: This skill replaces static block chords with a dance-ready syncopated rhythm. It encodes algorithmic diatonic chord generation and sets up native FX automation routing, creating a dynamic, mix-ready build-up out of thin air.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: Typically 120–130 BPM (Defaulting to 125 BPM).
  - **Grid/Syncopation**: The 3-3-2 rhythm divides the 4-beat bar into durations of 1.5 beats, 1.5 beats, and 1.0 beat.
  - **Articulation**: Notes are played slightly staccato (85% gate length) to leave rhythmic breathing room and emphasize the bouncy, pumping feel without needing complex sidechain routing.

* **Step B: Pitch & Harmony**
  - **Scale/Progression**: Uses a standard diatonic minor (i - VI - III - VII) or major (I - V - vi - IV) progression depending on the input.
  - **Voicing**: Triads played in root position, augmented with a sub-octave root note to provide weight and low-end support as the filter eventually opens up.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` for a foundational synthesizer tone.
  - **Filter Setup**: `ReaEQ` is used creatively. Band 4 (which is a High Shelf by default) has its gain reduced to the absolute minimum (-inf dB), effectively turning it into a sharp Low Pass / High Cut filter.

* **Step D: Mix & Automation**
  - **Filter Automation**: An automation envelope is attached to the ReaEQ Band 4 Frequency parameter. It sweeps linearly from roughly 200Hz (normalized `0.15`) up to 10kHz+ (normalized `0.85`) over the designated duration, smoothly revealing the track's high-frequency content.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Chords | `RPR_MIDI_InsertNote` | Provides exact algorithmic control over the 3-3-2 syncopation lengths and diatonic pitch structures. |
| Synth Sound | `ReaSynth` FX | Guarantees a sound source is available on any default REAPER installation without relying on third-party VSTs. |
| Filter Sweep Build-up | `ReaEQ` + `RPR_InsertEnvelopePoint` | Using native ReaEQ ensures cross-compatibility, while Envelope API allows us to program the signature build-up sweep natively. |

> **Feasibility Assessment**: 90%. While the video explicitly routes a sidechain compressor to a muted "ghost kick" for pumping, doing cross-track audio routing via the script API can be highly brittle depending on the exact ReaComp version. Instead, this script emulates the dynamic movement using rhythmic gating (85% note length) combined with the filter sweep, effectively capturing the structural and psychological impact of the build-up.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Build Sweep Chords",
    bpm: int = 125,
    key: str = "F",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Build-up Filter Sweep with 3-3-2 syncopated chords.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Number of bars to generate (sweep covers the entire duration).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set volume slightly lower to allow headroom for the build-up peak
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.7) 

    # === Step 3: Create MIDI Item & Syncopated Notes ===
    start_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory lookup arrays
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_val = NOTE_MAP.get(key.upper(), 5) + 48 # Default to F4 if missing
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    def get_pitch(degree, octave_offset=0):
        octaves = degree // 7
        step = degree % 7
        return root_val + (octaves + octave_offset) * 12 + scale_intervals[step]

    # Select diatonic chord progression based on scale
    if scale.lower() == "major":
        progression = [0, 4, 5, 3] # I - V - vi - IV
    else:
        progression = [0, 5, 2, 6] # i - VI - III - VII

    # 3-3-2 EDM rhythm syncopation (tuple of start_beat, duration_beats)
    rhythm = [(0.0, 1.5), (1.5, 1.5), (3.0, 1.0)]
    
    note_count = 0
    for bar in range(bars):
        chord_root_degree = progression[bar % len(progression)]
        bar_start_time = start_pos + bar * bar_length_sec
        
        # Chord Voicing: Sub-octave Root, Root, Third, Fifth
        pitches = [
            get_pitch(chord_root_degree, -1),
            get_pitch(chord_root_degree, 0),
            get_pitch(chord_root_degree + 2, 0),
            get_pitch(chord_root_degree + 4, 0)
        ]
        
        for beat_start, duration in rhythm:
            note_start_sec = bar_start_time + beat_start * beat_sec
            note_end_sec = note_start_sec + (duration * beat_sec * 0.85) # 85% gate leaves rhythmic gaps
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
            
            for p in pitches:
                valid_pitch = max(0, min(127, p))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, valid_pitch, velocity_base, True)
                note_count += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX & Filter Sweep Automation ===
    
    # 4a. Add Synthesizer
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 4b. Add EQ for Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Set ReaEQ Band 4 (High Shelf) Gain to minimum to act as a harsh low-pass cut
    # Param 10 is Band 4 Gain; 0.0 effectively mutes the high frequencies
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0) 
    
    # 4c. Automate ReaEQ Band 4 Frequency to open up over time
    # Param 9 is Band 4 Frequency
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    if env:
        start_val = 0.15 # Approx 200-300 Hz (Muffled / Underwater)
        end_val = 0.85   # Approx 10+ kHz (Bright / Open)
        
        # Shape 2 provides a slightly smoothed linear curve
        RPR.RPR_InsertEnvelopePoint(env, start_pos, start_val, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, start_pos + item_length, end_val, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM, including an automated EQ filter sweep."
```
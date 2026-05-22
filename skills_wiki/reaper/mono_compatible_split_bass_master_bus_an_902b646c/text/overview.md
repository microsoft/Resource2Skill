# Mono-Compatible Split Bass & Master Bus Analyzer Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Mono-Compatible Split Bass & Master Bus Analyzer Setup

* **Core Musical Mechanism**: This pattern actively applies the diagnostic mixing techniques taught in the tutorial. It splits a bass instrument into two discrete frequency bands: a strictly mono sub-bass foundation (below 120Hz) and a wide, stereo mid-bass (above 120Hz). A spectrum analyzer is then placed on the parent bus to visualize the tonal balance and phase alignment.
* **Why Use This Skill (Rationale)**: The tutorial focuses on using a frequency analyzer (like Voxengo SPAN) in Mid/Side mode to identify problematic low-end frequencies bleeding into the stereo field (the "Side" channel). Low frequencies carry massive energy, and placing them in the stereo field causes phase cancellation and loss of punch on mono playback systems. By forcefully crossing over the bass into a pure mono sub and a stereo mid-band, you achieve a massive, wide bass sound that remains perfectly phase-aligned and punchy in the sub-frequencies.
* **Overall Applicability**: Essential for EDM, Trap, Future Bass, and Pop mixing. Whenever a track requires a "huge" wide bass presence without sacrificing the solid, driving foundation of the kick and sub-bass relationship.
* **Value Addition**: This skill translates a *diagnostic* mixing concept (looking for side-channel low-end bleed) into an *actionable* production template. It automatically configures the routing, synthesis, EQ crossovers, and visual analyzer, saving significant setup time and encoding professional mix-down practices into the compositional phase.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/8th and 1/16th note syncopation.
  - **Pattern**: A driving, pumping rhythmic sequence that emphasizes the strong beats while stepping up to higher scale degrees on the off-beats.
  - **BPM**: Inherits project tempo (typically 110-130 BPM for this style).

* **Step B: Pitch & Harmony**
  - **Range**: Bass frequencies. The sub operates around C1-C2 (30Hz - 65Hz), delivering the "thud" the tutorial mentions, while the mid-bass highlights the harmonics up to 1kHz.
  - **Movement**: Root -> Octave -> Minor/Major 3rd -> Fifth. 

* **Step C: Sound Design & FX**
  - **Sub Bass Track**: `ReaSynth` (pure sine wave) → `JS: 3-Band EQ` (Mid & High bands muted, crossing over at 120Hz).
  - **Mid Bass Track**: `ReaSynth` (sawtooth wave for rich harmonics) → `JS: 3-Band EQ` (Low band muted, crossing over at 120Hz) → `JS: Chorus` (to generate the extreme stereo width that SPAN is designed to monitor).
  - **Bus Track**: `JS: Frequency Spectrum Analyzer Meter` applied to the folder parent to monitor the combined result.

* **Step D: Mix & Automation**
  - **Volume/Panning**: Sub bass is kept perfectly centered. The mid-bass is allowed to push to the extremes of the stereo field via the chorus effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Split Band Routing | Parent/Child Folder Tracks | Allows independent processing of the Sub and Mid frequencies while summing them together into a single analyzer bus. |
| Frequency Crossover | `JS: 3-Band EQ` | An extremely reliable stock REAPER plugin for hard-cutting frequency bands to enforce the mono-sub rule taught in the video. |
| Spectrum Analysis | `JS: Frequency Spectrum Analyzer Meter` | The stock alternative to Voxengo SPAN that requires zero third-party installations, fulfilling the core visual lesson of the tutorial. |
| Bass Sequencing | MIDI note insertion (`RPR_MIDI_InsertNote`) | Generates the actual musical tones needed to test the 50Hz vs 110Hz thud described in the tutorial. |

> **Feasibility Assessment**: 100% reproducible for the audio design pattern. While we cannot instantiate the third-party Voxengo SPAN plugin natively via ReaScript without assuming user installation, we perfectly recreate the *mixing technique* the tutorial uses SPAN to justify (mono low-end) and attach REAPER's stock spectrum analyzer to replicate the visual monitoring workflow.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Split_Bass_Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Mono-Compatible Split Bass and Spectrum Analyzer setup in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # Set tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Note map and scales for MIDI generation
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Base octave for sub bass (C2 = 36)
    base_pitch = 36 + root_val

    # Helper function to add MIDI notes
    def add_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === TRACK CREATION & ROUTING ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # 1. Create Parent Folder (Bus & Analyzer)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    bus_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1) # Start folder
    RPR.RPR_TrackFX_AddByName(bus_track, "Frequency Spectrum Analyzer Meter", False, -1)

    # 2. Create Child Track 1 (Sub Bass - Mono)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    sub_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", "Sub_Bass_Mono", True)
    
    # Setup Sub FX: Sine Wave + Lowpass
    fx_synth_sub = RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, fx_synth_sub, 2, 0.0) # Sawtooth mix 0%
    fx_eq_sub = RPR.RPR_TrackFX_AddByName(sub_track, "3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 1, -120.0) # Mid Gain cut
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 2, -120.0) # High Gain cut
    RPR.RPR_TrackFX_SetParam(sub_track, fx_eq_sub, 3, 120.0)  # Low-Mid Crossover Hz

    # 3. Create Child Track 2 (Mid Bass - Stereo)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 2, True)
    wide_track = RPR.RPR_GetTrack(0, num_tracks + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(wide_track, "P_NAME", "Mid_Bass_Wide", True)
    RPR.RPR_SetMediaTrackInfo_Value(wide_track, "I_FOLDERDEPTH", -1) # End folder
    
    # Setup Wide FX: Saw Wave + Highpass + Stereo Width
    fx_synth_wide = RPR.RPR_TrackFX_AddByName(wide_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(wide_track, fx_synth_wide, 2, 1.0) # Sawtooth mix 100%
    fx_eq_wide = RPR.RPR_TrackFX_AddByName(wide_track, "3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(wide_track, fx_eq_wide, 0, -120.0) # Low Gain cut
    RPR.RPR_TrackFX_SetParam(wide_track, fx_eq_wide, 3, 120.0)  # Low-Mid Crossover Hz
    RPR.RPR_TrackFX_AddByName(wide_track, "Chorus", False, -1)

    # === MIDI GENERATION ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    
    # Create items on both child tracks
    item_sub = RPR.RPR_AddMediaItemToTrack(sub_track)
    item_wide = RPR.RPR_AddMediaItemToTrack(wide_track)
    
    for item in [item_sub, item_wide]:
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_sec * bars)
        
    take_sub = RPR.RPR_AddTakeToMediaItem(item_sub)
    take_wide = RPR.RPR_AddTakeToMediaItem(item_wide)

    # Driving 1/8th and 1/16th syncopated bassline pattern
    note_count = 0
    for bar in range(bars):
        bar_offset = bar * bar_sec
        
        # Define rhythm in beats (1/4 = 1.0, 1/8 = 0.5, 1/16 = 0.25)
        # Sequence: Root(0) -> Root(0.5) -> Octave(1.5) -> Third(2.5) -> Fifth(3.0)
        pattern = [
            (0.0, 0.45, 0),                       # Beat 1
            (0.5, 0.95, 0),                       # Beat 1 &
            (1.5, 1.95, 12),                      # Beat 2 & (Octave jump)
            (2.5, 2.95, scale_intervals[2]),      # Beat 3 & (Third)
            (3.0, 3.45, scale_intervals[4]),      # Beat 4
            (3.5, 3.95, scale_intervals[4] - 12)  # Beat 4 & (Fifth, lower octave)
        ]
        
        for start_beat, end_beat, pitch_offset in pattern:
            pitch = base_pitch + pitch_offset
            start_t = bar_offset + (start_beat * beat_sec)
            end_t = bar_offset + (end_beat * beat_sec)
            
            add_note(take_sub, start_t, end_t, pitch, velocity_base)
            add_note(take_wide, start_t, end_t, pitch, velocity_base - 10)
            note_count += 1

    # Force MIDI UI update
    RPR.RPR_MIDI_Sort(take_sub)
    RPR.RPR_MIDI_Sort(take_wide)

    return f"Created Split Bass Bus with {note_count} notes over {bars} bars at {bpm} BPM. A stock Spectrum Analyzer has been placed on the parent folder to monitor mono compatibility."
```
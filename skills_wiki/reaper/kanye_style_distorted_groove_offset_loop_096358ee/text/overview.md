# Kanye-Style Distorted Groove & Offset Looping

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: Kanye-Style Distorted Groove & Offset Looping

* **Core Musical Mechanism**: This pattern relies on three distinct techniques:
  1. **Monotone Distorted Bass**: Using extreme distortion/saturation on a single repeated pitch (often a non-traditional bass sound) rather than relying on a classic 808.
  2. **Abrasive, Zero-Tail Percussion**: Designing upfront percussive layers with immediate cutoffs (gated or ultra-short ADSR release) run through heavy clipping.
  3. **"Hiding the Seams" (Offset Turnarounds)**: Taking a repetitive 1-bar or 2-bar sample chop sequence and slightly shifting the timing of the final chops on the 4th bar. This breaks the predictable grid and hides the restart point of the loop.

* **Why Use This Skill (Rationale)**: 
  * *Distortion* introduces complex, dense upper harmonics to simple sine/saw waves or samples. This allows a monotone, single-note bassline to remain interesting because the timbral texture is so rich.
  * *Zero-tail ADSR* creates abrupt silence between hits. This contrast (loud, clipped noise immediately followed by dead silence) creates an aggressive, "in-your-face" psychoacoustic effect.
  * *Offsetting turnarounds* combats listener fatigue. The human brain quickly maps repetitive loops; by shifting a chop by an 8th note right before the loop restarts, the brain is caught off guard, making the beat feel organic and constantly forward-moving.

* **Overall Applicability**: Gritty, sample-based hip-hop (Boom Bap, Industrial Hip-Hop), experimental electronic music, and minimalist beats where texture must compensate for a lack of melodic density.

* **Value Addition**: This skill moves beyond placing standard drum samples on a grid by encoding advanced sound design (synthetic clipping and gating) and structural arrangement (turnaround obfuscation) directly into the generated MIDI and FX chains.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: Mid-tempo hip-hop groove (80 - 95 BPM).
  * **Grid**: 1/8th and 1/16th note syncopations.
  * **Durations**: Extreme staccato for percussion (e.g., 50ms). Legato or standard lengths for the bass, depending on the groove.
  * **Turnaround**: On the final bar of the loop (e.g., Bar 4), the final hit is delayed by exactly one 1/8th note to "hide the seam."

* **Step B: Pitch & Harmony**
  * **Bass**: Strictly monotone (playing the Root note of the chosen key).
  * **Loop/Melody**: Minimalist 2 or 3 note chops (e.g., Root, Minor 3rd, Perfect 5th) to simulate a chopped soul or jazz sample.

* **Step C: Sound Design & FX**
  * **Instruments**: Stock `ReaSynth`. 
    * *Percussion*: Noise oscillator turned up, oscillators turned down, Sustain = 0, Release = very fast.
    * *Bass*: Square/Saw mix.
  * **FX Chain**: Heavy reliance on `JS: Saturation` and `JS: Distortion` to emulate the hardware clipping Kanye uses on vocal and drum chops.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Monotone Bass | MIDI insertion + `ReaSynth` + `JS: Saturation` | Allows us to synthetically generate a heavily driven, non-808 tonal bass layer matching the tutorial's aesthetic. |
| Abrasive Percussion | `ReaSynth` (Noise) + `JS: Distortion` + Envelope shaping | By tweaking ReaSynth's ADSR parameters via `RPR_TrackFX_SetParam`, we can enforce the "zero tail" abrasive cutoff described in the video. |
| "Hiding the seams" | Algorithmic MIDI timing (Offsetting Bar 4) | By dynamically shifting the `start_time` of notes in the final iteration of the loop, we perfectly replicate the offset chop technique. |

> **Feasibility Assessment**: 90%. While we cannot extract the exact vinyl samples Kanye uses, we can accurately reproduce the structural timing ("hiding the seams") and the core sound design philosophy (extreme distortion on zero-tail monotone/percussive layers) using stock REAPER synthesizers and JS effects.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "KanyeStyleGroove",
    track_name: str = "Distorted_Groove",
    bpm: int = 88,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Kanye-style distorted monotone groove with offset looping.
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

    # Helper function to insert MIDI notes
    def insert_note(take, start_time, duration, pitch, vel=100):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    quarter_note = 60.0 / bpm
    eighth_note = quarter_note / 2.0
    sixteenth_note = quarter_note / 4.0
    bar_length = quarter_note * 4
    total_length = bar_length * bars

    root_pitch = NOTE_MAP.get(key.capitalize(), 4)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Octave offsets
    bass_octave = 36 # C2 range
    melody_octave = 60 # C4 range
    
    notes_created = 0

    # ==========================================
    # TRACK 1: Monotone Distorted Bass
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_MonoBass", True)
    
    # FX: ReaSynth + JS Saturation
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 0, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 1, 0.5) # Saw mix
    
    bass_dist = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_dist, 0, 100.0) # 100% Amount for extreme drive

    # MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    bass_pitch = bass_octave + root_pitch

    for bar in range(bars):
        bar_start = bar * bar_length
        # Syncopated monotone pattern
        insert_note(bass_take, bar_start, quarter_note, bass_pitch, velocity_base)
        insert_note(bass_take, bar_start + quarter_note + eighth_note, eighth_note, bass_pitch, velocity_base - 10)
        insert_note(bass_take, bar_start + (quarter_note * 2) + sixteenth_note, eighth_note, bass_pitch, velocity_base)
        insert_note(bass_take, bar_start + (quarter_note * 3), eighth_note, bass_pitch, velocity_base - 15)
        notes_created += 4

    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # TRACK 2: Zero-Tail Abrasive Percussion
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    perc_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(perc_track, "P_NAME", f"{track_name}_AbrasivePerc", True)
    
    # FX: ReaSynth (Noise) + JS Distortion
    perc_synth = RPR.RPR_TrackFX_AddByName(perc_track, "ReaSynth", False, -1)
    # Zero out standard oscillators
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 0, 0.0) # Square
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 1, 0.0) # Saw
    # Max noise
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 4, 1.0) # Noise mix
    # ADSR for "Zero Tail"
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 6, 0.0) # Attack = 0
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 7, 0.1) # Decay = short
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 8, 0.0) # Sustain = 0
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 9, 0.0) # Release = 0
    
    perc_dist = RPR.RPR_TrackFX_AddByName(perc_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(perc_track, perc_dist, 0, 15.0) # Heavy Gain
    
    perc_item = RPR.RPR_AddMediaItemToTrack(perc_track)
    RPR.RPR_SetMediaItemInfo_Value(perc_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(perc_item, "D_LENGTH", total_length)
    perc_take = RPR.RPR_AddTakeToMediaItem(perc_item)

    for bar in range(bars):
        bar_start = bar * bar_length
        # Upfront percussive hits on 2 and 4, plus syncopations
        insert_note(perc_take, bar_start + quarter_note, sixteenth_note, 60, velocity_base)
        insert_note(perc_take, bar_start + quarter_note + eighth_note + sixteenth_note, sixteenth_note, 60, velocity_base - 20)
        insert_note(perc_take, bar_start + (quarter_note * 3), sixteenth_note, 60, velocity_base)
        notes_created += 3

    RPR.RPR_MIDI_Sort(perc_take)

    # ==========================================
    # TRACK 3: "Hiding the Seam" Offset Loop
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    loop_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(loop_track, "P_NAME", f"{track_name}_OffsetChops", True)
    
    loop_synth = RPR.RPR_TrackFX_AddByName(loop_track, "ReaSynth", False, -1)
    
    loop_item = RPR.RPR_AddMediaItemToTrack(loop_track)
    RPR.RPR_SetMediaItemInfo_Value(loop_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(loop_item, "D_LENGTH", total_length)
    loop_take = RPR.RPR_AddTakeToMediaItem(loop_item)

    # Simple 3-chop sequence representing a sample
    chop_1_pitch = melody_octave + root_pitch
    chop_2_pitch = melody_octave + root_pitch + scale_intervals[2] # 3rd degree
    chop_3_pitch = melody_octave + root_pitch + scale_intervals[4] # 5th degree

    for bar in range(bars):
        bar_start = bar * bar_length
        
        # Chop 1 & 2 are consistent
        insert_note(loop_take, bar_start, quarter_note, chop_1_pitch, velocity_base - 10)
        insert_note(loop_take, bar_start + quarter_note, quarter_note, chop_2_pitch, velocity_base - 15)
        
        # "Hiding the Seam" Logic:
        if bar == bars - 1:
            # On the final bar, shift the 3rd chop later by an 8th note to break the predictability
            offset = eighth_note
            insert_note(loop_take, bar_start + (quarter_note * 2) + offset, quarter_note, chop_3_pitch, velocity_base)
        else:
            # Normal placement for standard bars
            insert_note(loop_take, bar_start + (quarter_note * 2), quarter_note, chop_3_pitch, velocity_base)
            
        notes_created += 3

    RPR.RPR_MIDI_Sort(loop_take)

    return f"Created {track_name} groove with {notes_created} notes across 3 tracks (Mono Bass, Zero-Tail Perc, Offset Chops) over {bars} bars at {bpm} BPM."
```
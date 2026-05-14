### 1. High-level Design Pattern Extraction

> **Skill Name**: Filtered Pumping Intro / Build

* **Core Musical Mechanism**: This pattern strips back the arrangement to just the core harmonic progression (chords) while applying two crucial effects: a slowly opening Low-Pass Filter (frequency sweep) and a 4-on-the-floor amplitude ducking effect (sidechain pumping). 
* **Why Use This Skill (Rationale)**: Psychoacoustically, a heavy low-pass filter removes high-frequency energy, making the music feel smaller, darker, and further away. As the filter opens, the energy "approaches" the listener, naturally building tension. The pumping effect keeps the listener's internal physical clock locked to the dance tempo without needing a literal, heavy kick drum, preserving the groove and leaving spectral room for the drop to hit with maximum impact.
* **Overall Applicability**: This is the quintessential arrangement technique for EDM, House, and Future Bass tracks. It is used to transition from an intro into a verse, or from a breakdown/bridge into a high-energy drop.
* **Value Addition**: Compared to a static MIDI chord loop, this skill encodes structural arrangement techniques. It demonstrates how to create motion, anticipation, and groove out of a static element using automation and simulated sidechaining.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120-130 BPM (Standard House/EDM).
  - **Grid**: Sustained chords (whole notes or tied over multiple bars) serving as a pad/bed.
  - **Ducking Rhythm**: The volume dips sharply on every downbeat (1/4 note grid) and recovers in an 8th-note or 16th-note curve, mimicking a sidechain compressor triggered by a four-on-the-floor kick.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Often minor or Dorian for electronic tracks.
  - **Progression**: A classic 4-bar EDM progression (e.g., i - VI - III - VII).
  - **Voicing**: Wide block chords, often with the root note doubled an octave lower to fill out the spectrum.

* **Step C: Sound Design & FX**
  - **Instrument**: A supersaw or rich poly-synth (approximated here via native `ReaSynth` with a mix of saw/square).
  - **Filter**: `JS: Lowpass` or ReaEQ. 
  - **Dynamic FX**: Pumping volume envelope to simulate the sidechain compression shown in the tutorial.

* **Step D: Mix & Automation**
  - **Filter Automation**: Low-pass cutoff starts around 200-400Hz and linearly ramps up to fully open (20kHz) over the course of the 4 or 8 bar section.
  - **Volume Automation**: Rhythmic dipping on beats 1, 1.25, 1.5, 1.75 etc.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Progression | MIDI note insertion | Allows algorithmic generation of the i-VI-III-VII chord sequence based on user parameters. |
| Synth Sound | `ReaSynth` FX chain | Native REAPER synth that can generate the necessary harmonically rich waveforms (sawtooth) to feed the filter. |
| Sidechain Pump | Track Volume Envelope | Instead of brittle routing to a dummy kick track, writing a perfectly timed pumping volume envelope is 100% reliable in ReaScript and perfectly mimics the tutorial's sidechain result. |
| Tension Build | `JS: Lowpass` Envelope | Automating the filter frequency parameter directly creates the classic "approaching" tension sweep shown by the creator. |

> **Feasibility Assessment**: 95%. The structural and mixing techniques (chords, pumping, filter sweep) are perfectly reproduced using REAPER's native automation and JSFX. The only difference is the specific VST synthesizer tone, which is approximated using ReaSynth.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Pumping Filtered Build",
    bpm: int = 126,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Intro/Build sequence featuring sustained chords,
    a 4-on-the-floor simulated sidechain pump, and an opening low-pass filter sweep.
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Default to F minor if missing
    root_val = NOTE_MAP.get(key.capitalize(), 5)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Classic EDM Progression: i - VI - III - VII
    # Represented as scale degrees (0-indexed)
    progression = [0, 5, 2, 6] 

    # --- Step 1: Initialize Project & Track ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set track color to an "EDM Orange/Red"
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", RPR.RPR_ColorToNative(255, 100, 50) | 0x1000000)

    # --- Step 2: Create Media Item & MIDI Take ---
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # --- Step 3: Insert Chords ---
    octave_base = 4
    notes_added = 0
    
    for bar in range(bars):
        # Loop the progression if bars > len(progression)
        degree = progression[bar % len(progression)]
        
        # Build a triad + octave bass
        chord_intervals = [
            degree, 
            (degree + 2) % 7, 
            (degree + 4) % 7
        ]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate literal MIDI notes
        for i, interval in enumerate(chord_intervals):
            octave_shift = (degree + (2*i if i>0 else 0)) // 7
            note_val = root_val + scale_intervals[interval] + ((octave_base + octave_shift) * 12)
            
            # Insert triad notes
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val, velocity_base, False)
            notes_added += 1
            
            # Add a bass note an octave lower for depth
            if i == 0:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val - 12, velocity_base + 10, False)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # --- Step 4: Sound Design (ReaSynth) ---
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to Sawtooth for a rich harmonic spectrum
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0) # Saw shape
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Square shape
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.8) # Release

    # --- Step 5: The "Filter Sweep" Automation ---
    # Add a Lowpass filter
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Lowpass", False, -1)
    # Get the envelope for Param 0 (Frequency) and create it if it doesn't exist
    filter_env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True)
    
    if filter_env:
        # Sweep from 10% (muffled) to 100% (fully open) over the entire duration
        RPR.RPR_InsertEnvelopePoint(filter_env, 0.0, 0.1, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(filter_env, total_length_sec, 1.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(filter_env)

    # --- Step 6: The "Sidechain Pump" Volume Automation ---
    # Show volume envelope
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if vol_env:
        # Loop through every beat (1/4 note) to create a pumping effect
        total_beats = bars * beats_per_bar
        for b in range(total_beats):
            beat_start = b * beat_length_sec
            pump_bottom = beat_start + 0.01
            pump_recover = beat_start + (beat_length_sec * 0.4) # Recovers slightly before next beat
            
            # Amplitude values (Reaper linear volume: 1.0 = 0dB, 0.25 = -12dB, 0.05 = -26dB)
            vol_ducked = 0.05 
            vol_full = 1.0
            
            # Beat Start (dip instantly)
            RPR.RPR_InsertEnvelopePoint(vol_env, beat_start, vol_full, 0, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(vol_env, pump_bottom, vol_ducked, 2, 0.0, False, True) # 2 = Slow Start/End shape
            
            # Recover
            RPR.RPR_InsertEnvelopePoint(vol_env, pump_recover, vol_full, 0, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(vol_env)

    return f"Created '{track_name}' with {notes_added} chord notes, fake sidechain pump, and filter sweep over {bars} bars at {bpm} BPM."
```
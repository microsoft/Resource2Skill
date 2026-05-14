# Power Layered EDM Bass

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Power Layered EDM Bass

* **Core Musical Mechanism**: The technique relies on **Frequency & Transient Splitting** through layered synthesis. Instead of trying to force a single synthesizer to cover the entire sonic spectrum, the bass is split into specific, purpose-driven tracks:
  1. **Sub**: Handles the fundamental weight (deep, sustained, low-pass filtered).
  2. **Mid / Punch**: Handles the attack transient and aggressive grit (fast decay envelope, distortion, high-pass filtered to avoid low-end mud).
  3. **High / Wide**: Handles the stereo width and upper harmonics (sustained, chorus/unison, heavily high-pass filtered).
  These layers are grouped into a single folder/bus and compressed ("glued") together so they sound like one massive instrument playing a syncopated, bouncy 16th-note rhythm.

* **Why Use This Skill (Rationale)**: By separating frequencies, you prevent low-end phase cancellation and "mud" (the mid/high layers have their bass frequencies cut). By separating transients, you can have a massive, sustained sub-bass while still retaining the sharp, rhythmic punch of a pluck bass in the mid-range.

* **Overall Applicability**: Essential for Future House, Future Bounce, EDM drops, and modern Pop/Hip-Hop where the bass needs to sound enormous, wide, and rhythmic without cluttering the mix.

* **Value Addition**: This script encodes a complete "Bus + Multilayer" mixing topology. Instead of just writing MIDI, it automates the creation of a track folder, instantiates three customized synthesizers with specialized envelope shapes, applies the necessary crossover EQs, and glues them together with bus compression.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 126–130 BPM.
  - **Rhythm**: A highly syncopated Future Bounce 16th-note pattern.
  - **Timing Matrix**: Notes trigger on beat 1, the "a" of 1, the "&" of 2, beat 3, the "a" of 3, and the "&" of 4. Notes are slightly shortened (staccato gaps) to ensure the transient envelopes re-trigger cleanly.

* **Step B: Pitch & Harmony**
  - **Key**: G minor (standard heavy bass key).
  - **Progression**: i - VI - iv - v (Root, bVI, iv, v).
  - **Octave Spacing**: Sub plays on octave 1 (G1), Mid plays on octave 2 (G2), High plays on octave 3 (G3).

* **Step C: Sound Design & FX**
  - **Sub Layer**: Sine/Triangle wave. `ReaEQ` cutting highs above 150Hz.
  - **Punch Layer**: Square/Saw mix with a fast decay (150ms) and low sustain. `ReaEQ` cutting lows below 150Hz.
  - **High Layer**: Saw wave with `JS: Chorus` for stereo width. `ReaEQ` cutting lows below 600Hz.
  - **Bus**: `ReaComp` on the parent folder to glue the layers together.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bouncy syncopated rhythm | MIDI Note Insertion (`InsertNote`) | Allows precise programming of 16th-note syncopation and staccato gaps. |
| Frequency & Transient Layering | Multiple Tracks + `ReaSynth` Envelopes | Matches the tutorial's core lesson of separating attack/punch from sub-body using distinct synth parameters. |
| EQ Crossovers | `ReaEQ` (High/Low Shelf attenuation) | The most robust, native way to filter frequencies without relying on external plugins. |
| Bus Routing | Track `I_FOLDERDEPTH` | Groups the layers visually and sonically, allowing the bus compressor to glue them. |

> **Feasibility Assessment**: 90% reproduction. While we cannot load the exact third-party synths (Serum/Sylenth) shown in the video, we perfectly recreate the *mixing and synthesis architecture* (frequency splitting, transient separation, and bus gluing) using native REAPER plugins. The resulting sound accurately demonstrates the "power layering" technique.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Power Layered Bass",
    bpm: int = 126,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a multi-layered EDM bass bus (Sub, Mid-Punch, High-Wide) 
    playing a bouncy, syncopated 16th-note rhythm in REAPER.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }
    
    if scale not in SCALES:
        scale = "minor"

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Future Bounce Syncopated Rhythm Grid
    # Format: (start_16th_index, length_in_16ths)
    pattern = [
        (0, 1.5),  # Beat 1
        (3, 1.0),  # Beat 1 'a'
        (6, 1.5),  # Beat 2 '&'
        (8, 1.5),  # Beat 3
        (11, 1.0), # Beat 3 'a'
        (14, 1.5)  # Beat 4 '&'
    ]
    
    # Simple i - VI - iv - v progression mapped to scale indices
    progression_degrees = [0, 5, 3, 4] 
    
    # Define the sonic characteristics of the 3 layers
    layers = [
        {
            "name": "Sub", 
            "octave_shift": -1, 
            "lp_freq": 150.0, 
            "hp_freq": None, 
            "chorus": False,
            "synth": {4: 1.0, 3: 0.0, 8: 1.0, 9: 50.0} # Triangle, full sustain
        },
        {
            "name": "Mid Punch", 
            "octave_shift": 0, 
            "lp_freq": None, 
            "hp_freq": 150.0, 
            "chorus": False,
            "synth": {2: 1.0, 3: 1.0, 6: 0.0, 7: 150.0, 8: 0.1, 9: 50.0} # Square/Saw, fast decay, low sustain
        },
        {
            "name": "High Wide", 
            "octave_shift": 1, 
            "lp_freq": None, 
            "hp_freq": 600.0, 
            "chorus": True,
            "synth": {3: 1.0, 2: 0.0, 8: 0.8, 9: 100.0} # Saw, high sustain
        }
    ]

    beats_per_bar = 4
    item_length_sec = bars * beats_per_bar * (60.0 / bpm)

    # === 1. Create Parent Bus Track ===
    bus_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(bus_idx, True)
    bus_track = RPR.RPR_GetTrack(0, bus_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)
    
    # Make it a folder parent
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)
    
    # Add glue compressor to bus
    comp_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(bus_track, comp_idx, 0, -15.0) # Threshold
    RPR.RPR_TrackFX_SetParam(bus_track, comp_idx, 1, 4.0)   # Ratio

    # === 2. Create Child Layers ===
    for i, layer in enumerate(layers):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        full_name = f"{track_name} - {layer['name']}"
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_name, True)
        
        # Close folder on the last layer
        if i == len(layers) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", -1)
        else:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", 0)

        # Add & Configure ReaSynth
        synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        for param_idx, val in layer["synth"].items():
            RPR.RPR_TrackFX_SetParam(track, synth_idx, param_idx, val)

        # Add & Configure ReaEQ for frequency splitting
        eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
        if layer["hp_freq"]:
            # Band 1 (Low Shelf) turned down to -60dB acts as a smooth High-Pass
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, layer["hp_freq"])
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, -60.0)
        if layer["lp_freq"]:
            # Band 4 (High Shelf) turned down to -60dB acts as a smooth Low-Pass
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, layer["lp_freq"])
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, -60.0)

        # Add Chorus for width on high layers
        if layer["chorus"]:
            RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Generate MIDI Notes
        for bar in range(bars):
            # Determine chord root for the bar
            prog_idx = bar % len(progression_degrees)
            scale_degree = progression_degrees[prog_idx]
            
            # Base octave (e.g., C2 = 36)
            root_midi = NOTE_MAP[key] + 36 
            pitch = root_midi + SCALES[scale][scale_degree % len(SCALES[scale])]
            
            # Apply layer-specific octave shifting
            pitch += (layer["octave_shift"] * 12)

            for start_16th, len_16th in pattern:
                start_qn = bar * beats_per_bar + (start_16th * 0.25)
                # Subtract 0.05 QN to create a small staccato gap to retrigger envelopes
                end_qn = start_qn + (len_16th * 0.25) - 0.05

                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

                RPR.RPR_MIDI_InsertNote(
                    take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False
                )

        RPR.RPR_MIDI_Sort(take)

    return f"Created multi-layer bass bus '{track_name}' with 3 layers (Sub, Mid, High) over {bars} bars."
```
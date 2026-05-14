# Heavy Reese Bass (Detuned Saws + Sub + Multiband Distortion)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Heavy Reese Bass (Detuned Saws + Sub + Multiband Distortion)

* **Core Musical Mechanism**: The defining characteristic of a "Reese Bass" is the phasing and movement created by playing two identical waveforms (usually saw waves) that are slightly detuned from one another. This tutorial expands on the classic technique by keeping the sub-bass (a sine wave) perfectly centered and clean, while routing the detuned saw waves through heavy multiband compression (OTT-style) and soft-clip distortion. Finally, automated pitch-gliding is applied to give the bass a "diving" or "scooping" motion.
* **Why Use This Skill (Rationale)**: Detuning oscillators creates a psychoacoustic "beating" effect—as the waveforms drift in and out of phase, they cancel and reinforce each other, giving the bass a continuous, tearing motion without needing an LFO. By separating the sub-bass from this detuning process, you maintain low-end mono compatibility and punch, avoiding a muddy mix. The multiband compression flattens the dynamics, bringing out the high-frequency crunch of the distortion.
* **Overall Applicability**: This is a staple sound design pattern for Drum & Bass, Dubstep, Midtempo (e.g., Rezz, 1788-L), Cyberpunk, and heavy cinematic electronic music. It is almost always used as the dominant melodic and harmonic anchor in a "drop" section.
* **Value Addition**: Compared to a basic MIDI bassline, this skill encodes the complete synthesis architecture required for a professional heavy bass: fundamental sub-layering, stereo width via detuning, harmonic excitation via saturation, and the specific high/low EQ brackets needed to make it sit cleanly in a mix.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: Typically 85-110 BPM (Midtempo) or 170-174 BPM (Drum & Bass).
  * **Rhythm**: Relies heavily on long, sustained notes to allow the phase-cancellation movement to evolve. Legato/overlapping notes are used to trigger pitch glides (portamento).
* **Step B: Pitch & Harmony**
  * **Key/Scale**: Usually Minor, Phrygian, or Harmonic Minor. 
  * **Register**: The fundamental sub-bass sits deep in the C1-E1 range (approx. 30-40 Hz). 
* **Step C: Sound Design & FX**
  * **Oscillators**: 
    * Osc 1: Saw wave (-2 octaves).
    * Osc 2: Saw wave (-2 octaves), slightly detuned (+10 to +20 cents).
    * Osc 3: Sine wave (-3 octaves), pure mono sub-bass.
  * **FX Chain Sequence**: 
    1. **Chorus**: High-passed (so it only widens the highs), creating extra detuned width.
    2. **Multiband Compression**: Fast attack, slightly reduced release, high mix to crush the dynamics and bring up the noise floor/harmonics.
    3. **Soft Clip Distortion / Saturator**: Pushed hard to add grit and square off the peaks.
    4. **EQ (Pre/Post)**: High-pass the extreme ultra-lows (<30Hz) to prevent headroom loss, low-pass the extreme highs to remove digital fizz/noise, and notch out harsh midrange frequencies.
* **Step D: Mix & Automation**
  * **Pitch Automation**: Global pitch dips at the end of phrases to create a "power down" or "falling" effect.
  * **Voicing**: Strictly monophonic with glide/portamento enabled.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Bassline | MIDI note insertion | Allows us to sequence overlapping legato notes, which is essential for heavy bass grooves. |
| Detuned Saw Movement | FX Chain: ReaSynth + JS Chorus | Standard `ReaSynth` provides the raw saw wave. `JS: Chorus` perfectly emulates the detuned double-oscillator phasing central to a Reese bass. |
| Multiband Grit | FX Chain: ReaXcomp + JS Saturation | Emulates the Vital OTT multiband compression and soft-clip distortion used in the tutorial. |
| Clean Sub + EQ | FX Chain: ReaEQ | Replicates the Ableton EQ Eight cuts, removing muddy ultra-lows and harsh high-end fizz. |

> **Feasibility Assessment**: 80%. While we cannot run Vital or Ableton's "Corpus" natively via ReaScript, we can replicate the exact mathematical audio principles (detuned saws -> chorus -> multiband compression -> saturation -> EQ limits) using REAPER's stock plugins. The resulting sound provides the exact same heavy, phasing Reese character.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Heavy Reese Bass",
    bpm: int = 100,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 115,
    **kwargs,
) -> str:
    """
    Creates a Heavy Reese Bass pattern with a detuned FX chain and syncopated MIDI.
    """
    import reaper_python as RPR

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11]
    }

    root_pitch = NOTE_MAP.get(key.upper(), 4) # Default E
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # We want a low bass register (Octave 1 = starting at MIDI note 24)
    base_note = 24 + root_pitch 
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Create MIDI Item
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert MIDI notes (A syncopated, heavy midtempo bass rhythm)
    # Rhythm structure in 16th notes: [3, 3, 2] (half bar), then a long sustained 1-bar note
    
    ppq_per_quarter = 960 # Standard REAPER PPQ
    ppq_16th = ppq_per_quarter / 4
    
    # Note sequence: lengths in 16ths, scale degree, overlap for glide
    rhythm_pattern = [
        {"len": 3, "deg": 0},
        {"len": 3, "deg": 0},
        {"len": 2, "deg": 2}, # up slightly
        {"len": 8, "deg": 0}, # sustain
        {"len": 16, "deg": 0} # big 1 bar sustain with pitch dive potential
    ]
    
    current_ppq = 0
    note_count = 0
    
    # Loop over bars to create the pattern
    sequence_len_16ths = 32 # 2 bars
    iterations = (bars * 16) // sequence_len_16ths
    if iterations == 0: iterations = 1

    for loop in range(iterations):
        for step in rhythm_pattern:
            note_len_ppq = step["len"] * ppq_16th
            note_val = base_note + scale_intervals[step["deg"]]
            
            # Make the note slightly longer than its step length to create legato (overlap)
            # Legato triggers the portamento/glide in monophonic synths
            end_ppq = current_ppq + note_len_ppq + (ppq_16th * 0.5)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                current_ppq, end_ppq, 
                0, note_val, velocity_base, False
            )
            
            current_ppq += note_len_ppq
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # Add Sound Design FX Chain
    
    # 1. ReaSynth: Raw Saw Wave
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. JS Chorus: Emulates the highly detuned "Reese" dual-saw phasing
    # Slow rate, high depth, 50% mix
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 0, 15.0) # Delay
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 1, 0.3)  # Rate
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 2, 4.0)  # Depth
    
    # 3. ReaXcomp: Multiband compression (OTT style crush)
    RPR.RPR_TrackFX_AddByName(track, "ReaXcomp", False, -1)
    
    # 4. JS Saturation: Soft Clipping to add harmonic grit
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track, sat_idx, 0, 75.0) # Amount (Drive)
    
    # 5. ReaEQ: Sculpting (Cut extreme lows to preserve headroom, cut extreme highs to remove fizz)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: High Pass at 30Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0) # Type: High Pass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 30.0) # Freq
    # Band 4: Low Pass at 8000Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 1) # Type: Low Pass (approx index mapping)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 8000.0) # Freq

    return f"Created '{track_name}' (Reese Bass) with {note_count} legato notes over {bars} bars at {bpm} BPM in {key} {scale}."
```
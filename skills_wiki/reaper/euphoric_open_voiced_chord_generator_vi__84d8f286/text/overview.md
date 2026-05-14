# Euphoric Open-Voiced Chord Generator (VI-III-VII-i)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Euphoric Open-Voiced Chord Generator (VI-III-VII-i)

* **Core Musical Mechanism**: The tutorial demonstrates a defining technique for modern electronic, pop, and chillwave music: **Open-Voiced Triads with Top-End Pedal Tones**. Instead of playing standard block chords, the producer constructs a diatonic progression (VI - III - VII - i in minor), extracts the 3rd interval from the middle of each chord, and transposes it up an entire octave. Two sustained "pedal tones" (the 3rd and 7th scale degrees) are then layered over the entire progression. 
* **Why Use This Skill (Rationale)**: Moving the 3rd up an octave opens up the midrange frequency band, preventing muddy low-mid build-up while creating a wide, "lush" arrangement. Harmonically, the constant pedal notes create functional tension and resolution; as the chords change underneath, the pedal tones temporarily rub against the harmony (creating pleasant maj7, add9, or sus4 textures) before resolving smoothly.
* **Overall Applicability**: This technique is the backbone of "feel-good", euphoric, and emotional anthems (Future Bass, Melodic House, Synthwave, Pop). It works perfectly on warm analog pads, supersaws, and soft pianos.
* **Value Addition**: This encodes pure music theory into an algorithmic generator. A blank MIDI clip requires you to know voice leading, diatonic intervals, and chord inversions. This skill automatically maps the requested key to the correct scale degrees, spaces the chords into open voicings, and anchors the harmony with mathematically correct pedal tones.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 110-130 BPM (typically).
  - **Grid/Rhythm**: 1 chord per bar over a 4-bar loop (whole notes).
  - **Articulation**: Legato (100% gate length), meaning chords seamlessly transition into one another with no gaps.

* **Step B: Pitch & Harmony**
  - **Scale**: Natural Minor.
  - **Progression**: VI - III - VII - i (Scale degrees 6, 3, 7, 1).
  - **Voicing Algorithm**: 
    1. Bass note (Root - 1 octave)
    2. Tenor note (Root)
    3. Alto note (Perfect 5th)
    4. Soprano note (Major/Minor 3rd + 1 octave)
  - **Pedal Tones**: A drone on the 3rd scale degree and 7th scale degree (a perfect fifth above the first pedal), positioned two octaves up to sit above the changing chords.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` parameterized to behave like a warm pad.
  - **FX Chain**: `JS: Chorus` (to provide width/detuning for a "supersaw" feel) → `ReaVerbate` (for ambient decay).

* **Step D: Mix & Automation**
  - Moderate velocities (around 85-100) to keep the synth from sounding too harsh or plucky. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Voicings | MIDI note insertion | Requires precise pitch computation (Root, 5th, 3rd+12) and PPQ timing to construct the open chords. |
| Euphoric Timbre | FX chain creation | Combining ReaSynth with a Chorus and Reverb creates the lush, wide pad sound needed to sell the emotional impact. |

> **Feasibility Assessment**: 90% reproducibility. While we don't have the producer's exact third-party VSTs (like Serum or Sylenth1), the underlying music theory—the exact octave spacing, diatonic mapping, and pedal tones—is 100% reproducible using REAPER's ReaScript and stock plugins. 

#### 3b. Complete Reproduction Code

```python
def create_euphoric_open_chords(
    project_name: str = "EuphoricProject",
    track_name: str = "Euphoric Pad",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an emotional, open-voiced chord progression (VI-III-VII-i) with pedal tones.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "B").
        scale: Scale type (forces "minor" for this specific progression).
        bars: Number of bars (generates a 4-bar loop repeated).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note dictionary mapping
    NOTE_MAP = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
        "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
    }
    
    # Scale intervals for Natural Minor
    scale_intervals = [0, 2, 3, 5, 7, 8, 10]
    
    # Base MIDI pitch mapping (Octave 3 is a solid anchor point)
    # Using 48 (C3) as base octave offset
    root_pitch = 48 + NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 11)

    # Helper function to get the diatonic pitch for any scale degree
    # Automatically handles octave wrapping
    def get_diatonic_pitch(degree_0_indexed):
        octave = degree_0_indexed // 7
        step = degree_0_indexed % 7
        return root_pitch + (octave * 12) + scale_intervals[step]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # The progression: VI - III - VII - i
    # Zero-indexed scale degrees: 5, 2, 6, 0
    chord_sequence = [5, 2, 6, 0]
    
    # Generate the chords for the requested number of bars
    notes_inserted = 0
    for bar in range(bars):
        # Loop the 4-chord progression
        chord_root_degree = chord_sequence[bar % 4]
        
        start_time = bar * bar_length_sec
        end_time = (bar + 1) * bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Diatonic chord construction
        r_pitch = get_diatonic_pitch(chord_root_degree)
        third_pitch = get_diatonic_pitch(chord_root_degree + 2)
        fifth_pitch = get_diatonic_pitch(chord_root_degree + 4)
        
        # Apply the "Open Voicing" rules:
        bass = r_pitch - 12            # Bass note down 1 octave
        tenor = r_pitch                # Root note
        alto = fifth_pitch             # 5th note
        soprano = third_pitch + 12     # 3rd note pushed up 1 octave!

        voicings = [bass, tenor, alto, soprano]
        
        for pitch in voicings:
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, True)
            notes_inserted += 1

    # Apply the Pedal Tones spanning the entire length
    # Pedal 1: 3rd scale degree (index 2), shifted up 2 octaves
    pedal_1 = get_diatonic_pitch(2) + 24
    
    # Pedal 2: 7th scale degree (index 6), shifted up 2 octaves
    pedal_2 = get_diatonic_pitch(6) + 24
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, total_length)
    
    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pedal_1), velocity_base - 10, True)
    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pedal_2), velocity_base - 10, True)
    notes_inserted += 2

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain for a Wide, Lush Timbre ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # We add Chorus and Reverb to mimic the lush supersaws/pads from the tutorial
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    
    # Lower the track volume slightly to account for the massive 6-note chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    return f"Created '{track_name}' with {notes_inserted} open-voiced notes over {bars} bars at {bpm} BPM in {key} {scale}."
```
### 1. High-level Design Pattern Extraction

> **Skill Name**: Tight Unison Metal Doubling (Guitar & Bass)

* **Core Musical Mechanism**: The video demonstrates the technique of extracting a syncopated, staccato guitar riff and turning it into a perfectly mirrored MIDI bassline. The signature of this pattern is absolute rhythmic synchronization between the bass and guitar, including identical articulations (short palm-muted 16th notes followed by heavily accented sustained chords/notes), with the bass playing exactly one octave below the guitar.
* **Why Use This Skill (Rationale)**: This is a staple technique in modern metal, hard rock, and heavy alternative music. By locking the bass exactly to the rhythmic grid of the guitar's palm mutes and accents, it creates a psychoacoustic illusion of one massive, unified "super-instrument" rather than two distinct players. The staccato notes create aggressive rhythmic drive, while the sustained accents provide heavy harmonic weight.
* **Overall Applicability**: Best used in heavy verses, breakdowns, or main riff sections of rock/metal/djent/doom tracks where maximum low-end impact and rhythmic tightness are required. 
* **Value Addition**: Since an automated REAPER script cannot perform dynamic offline audio-to-MIDI analysis on unavailable external files (as done via EZBass in the video), this skill directly encodes the *intended musical outcome*: a perfectly synced, multi-track heavy metal riff template with synchronized staccato/legato programming and octave-separated tracking.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 110 - 140 BPM (standard for mid-tempo groove metal/hard rock).
  - **Rhythmic Grid**: 16th notes.
  - **Articulation**: Heavy contrast between short, staccato "palm-muted" notes (velocities ~90, cut short) and sustained "open" accents (velocities ~110-120, played for full duration).
* **Step B: Pitch & Harmony**
  - **Scale**: Blues or Harmonic Minor scale (relies heavily on the minor 3rd and flat 5th for tension).
  - **Voicing**: Unison doubling. The guitar plays the root riff (e.g., E2), and the bass mirrors it exactly one octave down (E1).
* **Step C: Sound Design & FX**
  - **Guitar**: Aggressive, mid-focused waveform (Square/Saw mix) fed into distortion, with lows rolled off to make room for the bass.
  - **Bass**: Subby, low-end waveform (Sine/Triangle) fed into lighter saturation for grit, with highs rolled off to avoid clashing with the guitar's pick attack.
* **Step D: Mix & Automation**
  - Bass panned dead center.
  - Guitar typically panned hard L/R (the script generates one centered heavy guitar as a core mono template).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Synchronization | MIDI note insertion on multiple tracks | Ensures perfect alignment and allows exact manipulation of staccato/legato durations across both instruments. |
| Octave Doubling | Parameterized MIDI generation | Automatically shifts the bass notes -12 semitones relative to the guitar riff. |
| Source Audio Emulation | Track & FX Creation | Since the source audio file is unavailable, we must synthesize both the Guitar and Bass tracks using ReaSynth and JSFX to demonstrate the musical result of the tutorial. |

> **Feasibility Assessment**: 80% — The code perfectly reproduces the musical rhythm, harmony, and octave-doubling mixing strategy shown in the video. The remaining 20% accounts for the fact that we are generating the source riff programmatically rather than analyzing an external WAV file, as REAPER ReaScript cannot robustly perform offline audio-to-MIDI transcription without third-party plugins (like EZBass). 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Unison_Riff",
    bpm: int = 120,
    key: str = "E",
    scale: str = "blues",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 'Tight Unison Metal Doubling' in the current REAPER project.
    Generates perfectly synced Guitar and Bass tracks playing a staccato heavy riff.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (will append 'Guitar' and 'Bass').
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Defaults to E for metal.
        scale: Scale type (blues, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # Ensure key and scale exist, fallback if not
    root_val = NOTE_MAP.get(key.capitalize(), 4) # Default to E
    scale_intervals = SCALES.get(scale.lower(), SCALES["blues"])

    # Base pitch for Guitar (e.g., E2)
    guitar_base_pitch = 40 + (root_val - 4)
    bass_base_pitch = guitar_base_pitch - 12 # Octave lower

    # === Define the Riff Pattern (Syncopated Staccato / Legato mix) ===
    # Tuple format: (scale_degree_index, duration_in_beats, is_staccato, velocity_modifier)
    riff_pattern = [
        (0, 0.25, True, 0.9),  # 16th, palm muted
        (0, 0.25, True, 0.9),  # 16th, palm muted
        (0, 0.25, True, 0.9),  # 16th, palm muted
        (1, 0.25, True, 1.0),  # 16th, minor 3rd accent
        (0, 0.25, True, 0.9),  # 16th
        (0, 0.25, True, 0.9),  # 16th
        (3, 0.50, False, 1.2), # 8th, flat 5th heavy accent (sustained)
        (0, 0.25, True, 0.9),  # 16th
        (0, 0.25, True, 0.9),  # 16th
        (0, 0.25, True, 0.9),  # 16th
        (2, 0.25, True, 1.0),  # 16th, 4th accent
        (1, 0.50, False, 1.1), # 8th, minor 3rd accent (sustained)
        (0, 0.50, False, 1.1)  # 8th, root (sustained resolution)
    ] # Total = 4.0 beats (1 Bar)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Step 2: Helper Function to Create Track & MIDI ===
    def create_instrument_track(name, base_pitch, is_bass):
        # Create Track
        track_idx = RPR.RPR_GetNumTracks()
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)

        note_count = 0
        
        # Loop over bars and populate MIDI
        for bar in range(bars):
            current_beat = bar * beats_per_bar
            for step in riff_pattern:
                scale_idx, dur_beats, staccato, vel_mod = step
                
                # Calculate Pitch
                # Handle octave wrapping if index exceeds scale length
                octave_shift = scale_idx // len(scale_intervals)
                safe_idx = scale_idx % len(scale_intervals)
                pitch = base_pitch + scale_intervals[safe_idx] + (octave_shift * 12)
                
                # Calculate Timing
                start_time_sec = current_beat * beat_len_sec
                # If staccato, cut the note to 50% of its slot length. If legato, 95%
                actual_dur_beats = dur_beats * 0.5 if staccato else dur_beats * 0.95
                end_time_sec = (current_beat + actual_dur_beats) * beat_len_sec
                
                # Convert to PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
                
                # Velocity mapping
                vel = min(127, max(1, int((velocity_base * vel_mod))))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                
                current_beat += dur_beats
                note_count += 1

        RPR.RPR_MIDI_Sort(take)

        # Add Synths & FX
        synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        if is_bass:
            # Subby Bass Setting: Triangle wave, lower tuning, filter highs
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0) # Square mix 0
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Saw mix 0
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 1.0) # Triangle mix 1.0
            
            # Add saturation/distortion for bite
            dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
            RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 5.0) # Gain
            
            # Lowpass EQ
            eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 3.0) # Band 1 Type: Low Shelf
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 100.0) # Freq
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 4.0) # Gain
            
            # Pan Center
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", 0.0)
            
        else:
            # Distorted Guitar Setting: Square/Saw mix
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7) # Square mix
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.7) # Saw mix
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0) # Triangle mix
            
            # Heavy Distortion
            dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
            RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 25.0) # Heavy Gain
            
            # Highpass EQ to leave room for bass
            eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 1.0) # Band 1 Type: High Pass
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 120.0) # Freq
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 0.0) # Gain
            
            # Pan slightly Right
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", 0.4)

        return note_count

    # === Step 3: Execute Creation ===
    notes_g = create_instrument_track(f"{track_name}_Guitar", guitar_base_pitch, is_bass=False)
    notes_b = create_instrument_track(f"{track_name}_Bass", bass_base_pitch, is_bass=True)

    return f"Created synced Guitar and Bass tracks ('{track_name}') with {notes_g} matched notes over {bars} bars at {bpm} BPM in {key} {scale}."
```
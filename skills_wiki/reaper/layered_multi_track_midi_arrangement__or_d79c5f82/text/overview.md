### 1. High-level Design Pattern Extraction

> **Skill Name**: Layered Multi-Track MIDI Arrangement (Orchestral / Band Context)

* **Core Musical Mechanism**: This pattern establishes a harmonically synchronized, multi-part arrangement (Drums, Bass, Rhythm Chords, and Lead Arpeggio/Melody) designed to be composed and edited simultaneously. By assigning specific frequency bands and rhythmic roles to distinct tracks and viewing them stacked in a single piano roll, the producer ensures tight harmonic voice leading and prevents rhythmic frequency masking.

* **Why Use This Skill (Rationale)**: Producing multiple instruments in isolation often leads to harmonic clashes or muddy mixes where elements fight for the same rhythmic space. By layering them (e.g., driving 8th-note bass, sustained mid-range chords, 16th-note high-register arpeggios, and anchored drums), you create a complete, balanced frequency spectrum. Seeing these notes ghosted against each other (using REAPER's multi-track MIDI visibility) allows for instant visual verification of chord voicings and rhythmic interplay.

* **Overall Applicability**: This template is the foundation for rock/metal band mockups, electronic music drops, and dense orchestral compositions where multiple sections (strings, brass, woodwinds) must weave together harmonically without colliding.

* **Value Addition**: Compared to an empty project, this skill provides an instantly playable 4-part polyphonic arrangement. It encodes the foundational music theory of diatonic chord progressions, track-based color-coding for visual organization, and complementary rhythmic subdivisions (quarter, eighth, and sixteenth note layers) across the frequency spectrum.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Drums**: Standard pop/rock backbeat (Kick on beats 1 and 3, Snare on 2 and 4, Hi-hats driving on constant 8th notes).
  - **Bass**: Driving 8th notes locking in with the drum groove.
  - **Rhythm Chords**: Sustained whole notes establishing the harmonic foundation for each bar.
  - **Lead**: 16th-note descending/ascending arpeggios providing top-end kinetic energy.
  - **Grid/Tempo**: 120 BPM, strictly quantized to the 16th-note grid to demonstrate tight interlocking parts.

* **Step B: Pitch & Harmony**
  - **Progression**: The code uses a standard `i - VI - III - VII` diatonic progression in minor keys (or `I - V - vi - IV` in major keys) across 4 bars.
  - **Voicing Structure**: 
    - Bass: Root notes played 1 octave below middle C (C2-C3 range).
    - Rhythm: Root position triads played around middle C (C3-C4 range).
    - Lead: Broken chord tones (root, 3rd, 5th) played 1 octave above middle C (C5 range).

* **Step C: Sound Design & FX**
  - Track color coding (Purple, Orange, Teal, Green) is actively used as a sound design organizational tool so the user can visually separate the instruments in the MIDI editor using "Color notes by: Track".
  - Native `ReaSynth` instances are inserted on the tonal tracks to provide immediate audio feedback (sine/sawtooth waves).

* **Step D: Mix & Automation**
  - To replicate the video's workflow optimally, the user should configure REAPER's settings as shown in the tutorial:
    1. *Options > MIDI Editor > One MIDI editor per project*
    2. *Behavior for "open items in built-in MIDI editor": Open all selected MIDI items*
    3. *Options (in MIDI Editor) > Color notes by > Track*

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-Track Creation | `RPR_InsertTrackAtIndex` & `RPR_SetMediaTrackInfo_Value` | Generates the distinct colored tracks required for the multi-track visual workflow demonstrated in the video. |
| Harmonic Progression | MIDI note insertion | Calculates diatonic triads and root notes dynamically using music theory math so it works in any key/scale. |
| Playback/Sound | FX chain (`ReaSynth`) | Uses REAPER's native synth to ensure the generated MIDI produces immediate audible chords and melodies without requiring 3rd-party VSTs. |

> **Feasibility Assessment**: 100% reproducible for the musical arrangement pattern. The workflow settings (docking, custom toolbars) shown in the video are global user preferences and shouldn't be overridden by a standard script, but the code perfectly scaffolds the 4-track musical context necessary to utilize those multi-track editing techniques.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "MultiTrack_Layer",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track layered arrangement (Drums, Bass, Rhythm, Lead) in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Ensure valid inputs
    root_note = NOTE_MAP.get(key, 11) # Default B
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard pop/rock progression diatonic degrees (0-indexed)
    if scale == "major":
        progression = [0, 4, 5, 3] # I - V - vi - IV
    else:
        progression = [0, 5, 2, 4] # i - VI - III - VII

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def get_chord_pitches(degree, root_midi):
        """Returns the MIDI pitches for a diatonic triad based on the scale degree."""
        p1 = root_midi + scale_intervals[degree % 7] + (12 * (degree // 7))
        p3 = root_midi + scale_intervals[(degree + 2) % 7] + (12 * ((degree + 2) // 7))
        p5 = root_midi + scale_intervals[(degree + 4) % 7] + (12 * ((degree + 4) // 7))
        return [p1, p3, p5]

    def add_midi_note(take, start_beat, end_beat, pitch, vel, chan=0):
        """Helper to insert MIDI notes using beat (quarter note) timing."""
        start_time = (60.0 / bpm) * start_beat
        end_time = (60.0 / bpm) * end_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    def create_instrument_track(name, color_hex, is_drum=False):
        """Creates a track, sets color, adds ReaSynth, and returns a new MIDI take of length 'bars'."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Set track color (Hex to Native RGB format | 0x1000000 for custom flag)
        color_val = color_hex | 0x1000000
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", color_val)
        
        # Add basic synth for immediate sound
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Create MIDI Item
        beats_per_bar = 4
        item_length = (60.0 / bpm) * beats_per_bar * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return take

    # Calculate base octave (C3 = 48)
    base_midi = 48 + root_note

    # --- TRACK 1: DRUMS ---
    # Indigo color: RGB(75, 0, 130) -> 75 | (0 << 8) | (130 << 16)
    take_drums = create_instrument_track(f"{track_name}_Drums", 75 | (0 << 8) | (130 << 16), is_drum=True)
    for bar in range(bars):
        b_offset = bar * 4
        # Kick (MIDI 36)
        add_midi_note(take_drums, b_offset + 0, b_offset + 0.25, 36, velocity_base)
        add_midi_note(take_drums, b_offset + 1.5, b_offset + 1.75, 36, velocity_base)
        add_midi_note(take_drums, b_offset + 2, b_offset + 2.25, 36, velocity_base)
        # Snare (MIDI 38)
        add_midi_note(take_drums, b_offset + 1, b_offset + 1.25, 38, velocity_base)
        add_midi_note(take_drums, b_offset + 3, b_offset + 3.25, 38, velocity_base)
        # Hi-Hats (MIDI 42)
        for i in range(8):
            add_midi_note(take_drums, b_offset + i*0.5, b_offset + i*0.5 + 0.25, 42, velocity_base - 20)
    RPR.RPR_MIDI_Sort(take_drums)

    # --- TRACK 2: BASS ---
    # Purple color: RGB(160, 32, 240)
    take_bass = create_instrument_track(f"{track_name}_Bass", 160 | (32 << 8) | (240 << 16))
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        # Down one octave for bass
        root_pitch = base_midi + scale_intervals[degree] - 12
        for i in range(8): # Driving 8th notes
            add_midi_note(take_bass, bar*4 + i*0.5, bar*4 + i*0.5 + 0.45, root_pitch, velocity_base)
    RPR.RPR_MIDI_Sort(take_bass)

    # --- TRACK 3: RHYTHM CHORDS ---
    # Orange color: RGB(255, 165, 0)
    take_chords = create_instrument_track(f"{track_name}_Chords", 255 | (165 << 8) | (0 << 16))
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        chord = get_chord_pitches(degree, base_midi)
        # Whole note sustained chords
        for pitch in chord:
            add_midi_note(take_chords, bar*4, bar*4 + 3.9, pitch, velocity_base - 10)
    RPR.RPR_MIDI_Sort(take_chords)

    # --- TRACK 4: LEAD ARPEGGIO ---
    # Teal/Green color: RGB(0, 200, 150)
    take_lead = create_instrument_track(f"{track_name}_Lead", 0 | (200 << 8) | (150 << 16))
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        chord = get_chord_pitches(degree, base_midi + 12) # Up one octave for lead
        # 16th note arpeggio repeating root, 3rd, 5th
        for i in range(16):
            pitch = chord[i % 3]
            # Add an accent every beat
            vel = velocity_base if i % 4 == 0 else velocity_base - 25
            add_midi_note(take_lead, bar*4 + i*0.25, bar*4 + i*0.25 + 0.2, pitch, vel)
    RPR.RPR_MIDI_Sort(take_lead)

    # Notify REAPER to update UI
    RPR.RPR_UpdateArrange()

    return f"Created 4 layered multi-tracks (Drums, Bass, Chords, Lead) with {bars} bars at {bpm} BPM in {key} {scale}."
```
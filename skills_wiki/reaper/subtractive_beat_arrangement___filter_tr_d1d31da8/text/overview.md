### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Beat Arrangement & Filter Transition

* **Core Musical Mechanism**: The tutorial demonstrates the principle of "Arrangement by Subtraction" combined with a "Wash-Out Drop Transition". You build the track starting from the densest, most complete section (the Chorus/Drop, containing the full kick pattern, fast hi-hats, chords, and lead melodies). You then copy this block to create the Verse/Build section, but *subtract* elements: omitting the kick drum at the start of the verse, slowing the hi-hat rhythm from 16th to 8th notes, and muting the lead melody entirely. At the final turnaround before the Chorus returns, a low-pass filter on the instrument bus sweeps down to muffle the sound, snapping back to full frequency exactly on the drop.

* **Why Use This Skill (Rationale)**: 
  - *Psychoacoustics & Contrast*: A mix sounds "huge" only relative to what came before it. By purposefully thinning out the rhythm (slower hi-hats, no kicks) and the frequency spectrum (muting the lead), the verse creates a sonic void.
  - *The Filter Wash-Out*: Dropping the cutoff frequency of a low-pass filter a beat before the drop removes high-frequency energy. This tricks the listener's brain into relaxing its high-frequency perception; when the drop hits with full spectrum, the perceived width and impact are exponentially magnified.

* **Overall Applicability**: This is a universal production macro-structure used in almost all modern genres, including trap, hip-hop, EDM, and pop. It is specifically useful when generating the overall timeline of a track to ensure the sections breathe and evolve rather than remaining a static 8-bar loop.

* **Value Addition**: Instead of just looping a chord progression, this skill encodes structural storytelling. It teaches an automated agent how to format dynamics over time (Verse → Build → Chorus) and how to use track grouping (busses) and automation to glue transitions together.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid & Subdivisions**: 4/4 time signature.
  - **Subtractive Rhythm**: 
    - *Chorus*: Kicks on beats 1 and 3.5. Hi-hats on 16th notes.
    - *Verse*: The first kick of the section is deliberately muted. Hi-hats are reduced to 8th notes.
  - **Transition Timing**: The filter sweep occurs on the 4th beat of the final bar of the verse section, lasting exactly one beat.

* **Step B: Pitch & Harmony**
  - **Progression**: Uses a diatonic `i - VI - III - VII` progression, universally applicable in minor scales.
  - **Subtractive Harmony**: The main chord foundation remains playing through both sections to anchor the listener, but the higher-octave melodic lead is completely deleted in the verse to reserve the high frequencies for the chorus.

* **Step C: Sound Design & FX**
  - **Bussing**: Synths and Leads are routed to a parent "Instrument Bus".
  - **FX Used**: A native Lowpass Filter (`JS: Lowpass`) is applied to the Instrument Bus. This allows a single automation line to affect all melodic elements simultaneously without messing up the drums.

* **Step D: Mix & Automation (if applicable)**
  - **Filter Cutoff Automation**: The lowpass filter's cutoff parameter is automated. It rests at 1.0 (fully open), sweeps down to 0.1 (heavily muffled) over the final 1.5 beats of the verse, and snaps instantly back to 1.0 exactly at beat 1 of the chorus.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Subtractive Drums | MIDI note insertion | Allows programmatic generation of a dense loop (chorus) and a sparse loop (verse) by selectively skipping beats in the loop logic. |
| Instrument Bussing | Track Folders (`I_FOLDERDEPTH`) | Replicates the tutorial's technique of treating all melodic instruments as a single unit for transition effects. |
| Filter Transition Sweep | Automation Envelope (`RPR_InsertEnvelopePoint`) | The exact technique shown to create the "wash-out" drop effect, controlling `JS: Lowpass` cutoff precisely. |

> **Feasibility Assessment**: 100% reproducible for the structural, MIDI, and automation techniques. While the specific third-party VST synths used in the video aren't available, we replicate the exact arrangement logic and FX transition using REAPER's native JSFX and MIDI items, completely capturing the core skill.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Subtractive Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Verse-to-Chorus Subtractive Arrangement with a Filter Sweep Transition.
    
    Bars 1 to (bars/2) represent the sparse Verse/Build.
    Bars (bars/2)+1 to the end represent the dense Chorus/Drop.
    """
    import reaper_python as RPR

    # --- Music Theory & Pitch Data ---
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

    scale_notes = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 48 + NOTE_MAP.get(key, 0) # Base octave C3

    # Standard pop/trap minor progression: i - VI - III - VII
    chord_progression_degrees = [
        [0, 2, 4], # i
        [5, 7, 9], # VI
        [2, 4, 6], # III
        [4, 6, 8]  # VII
    ]

    def get_pitch(degree, octave_offset=0):
        octave = degree // len(scale_notes)
        note_idx = degree % len(scale_notes)
        return root_midi + ((octave + octave_offset) * 12) + scale_notes[note_idx]

    # --- Step 1: Setup Tempo & Timing ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    sec_per_beat = 60.0 / bpm
    beats_per_bar = 4
    half_bars = max(2, bars // 2) 
    total_bars = half_bars * 2

    # Helper: Add MIDI note
    def add_midi_note(take, start_beat, duration_beats, pitch, vel):
        start_ppq = int(start_beat * 960)
        end_ppq = int((start_beat + duration_beats) * 960)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Helper: Create Track
    def create_track(name, folder_depth=0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", folder_depth)
        return track

    # Helper: Create MIDI item and take
    def create_midi_item(track, num_bars):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", num_bars * beats_per_bar * sec_per_beat)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # --- Step 2: Track Creation & Routing (Arrangement Hierarchy) ---
    # Drum Bus
    drum_bus = create_track(f"{track_name} - Drum Bus", 1)
    kick_track = create_track("Kick", 0)
    hihat_track = create_track("Hihat", -1) # End Drum Folder

    # Instrument Bus
    inst_bus = create_track(f"{track_name} - Inst Bus", 1)
    chord_track = create_track("Chords", 0)
    lead_track = create_track("Lead", -1) # End Inst Folder

    # Create MIDI Takes
    kick_take = create_midi_item(kick_track, total_bars)
    hihat_take = create_midi_item(hihat_track, total_bars)
    chord_take = create_midi_item(chord_track, total_bars)
    lead_take = create_midi_item(lead_track, total_bars)

    # --- Step 3: Subtractive Arrangement Logic ---
    for bar in range(total_bars):
        is_chorus = bar >= half_bars
        chord_degrees = chord_progression_degrees[bar % 4]
        
        # 1. Chords (Anchoring element - plays in both sections)
        for degree in chord_degrees:
            p = get_pitch(degree)
            add_midi_note(chord_take, bar * beats_per_bar, beats_per_bar, p, velocity_base - 10)

        # 2. Kick Drum
        for b in [0.0, 2.5]:
            # SUBTRACTION: Omit the very first kick of the Verse section for impact
            if not is_chorus and bar == 0 and b == 0.0:
                continue
            add_midi_note(kick_take, bar * beats_per_bar + b, 0.5, 36, velocity_base)

        # 3. Hi-hats
        # SUBTRACTION: Slower 8th notes in verse, fast 16th notes in chorus
        step = 0.25 if is_chorus else 0.5
        b = 0.0
        while b < beats_per_bar:
            add_midi_note(hihat_take, bar * beats_per_bar + b, 0.1, 42, velocity_base - 20)
            b += step

        # 4. Lead Melody
        # SUBTRACTION: Completely muted during the Verse section. Only plays in Chorus.
        if is_chorus:
            lead_pitch = get_pitch(chord_degrees[1], octave_offset=1) # 3rd of the chord, one octave up
            for b in [0.0, 1.5, 2.5, 3.5]:
                add_midi_note(lead_take, bar * beats_per_bar + b, 0.5, lead_pitch, velocity_base)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(hihat_take)
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(lead_take)

    # --- Step 4: The Filter Sweep Transition ---
    # Add JS: Lowpass to the Instrument Bus
    fx_idx = RPR.RPR_TrackFX_AddByName(inst_bus, "JS: Lowpass", False, -1)
    
    # Get envelope for Parameter 0 (Cutoff)
    env = RPR.RPR_GetFXEnvelope(inst_bus, fx_idx, 0, True)
    
    # Calculate transition times in seconds
    transition_bar = half_bars - 1
    t_start_sweep = (transition_bar * beats_per_bar + 2.5) * sec_per_beat  # Starts at beat 3 of the last verse bar
    t_muffled = (transition_bar * beats_per_bar + 3.9) * sec_per_beat      # Heavily filtered just before drop
    t_drop = (half_bars * beats_per_bar) * sec_per_beat                    # The Drop (Chorus start)

    # Insert Envelope Points (1.0 = fully open, 0.0 = fully closed)
    # 0 = linear shape, 1 = square, 2 = slow start/end, 3 = fast start
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, t_start_sweep, 1.0, 2, 0.0, False, True)   # Anchor point before sweep
    RPR.RPR_InsertEnvelopePoint(env, t_muffled, 0.15, 1, 0.0, False, True)      # Muffled wash-out (Square shape to hold until drop)
    RPR.RPR_InsertEnvelopePoint(env, t_drop, 1.0, 0, 0.0, False, True)          # Snap back to full spectrum at the Drop
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created subtractive arrangement '{track_name}' (Verse -> Chorus) over {total_bars} bars at {bpm} BPM, with a low-pass filter drop transition on the instrument bus."
```
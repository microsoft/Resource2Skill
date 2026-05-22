### 1. High-level Design Pattern Extraction

> **Skill Name**: Synthwave Multi-Track Ensemble (Arp, Chords, Bass, Drums)

* **Core Musical Mechanism**: 
Frequency layering and multi-track orchestration. This pattern constructs a complete 4-layer musical ensemble characteristic of the synthwave/rock demonstration shown in the tutorial. It utilizes a driving 4-on-the-floor drum beat with 8th-note hi-hats, a pumping 8th-note root bassline, sustained block chords for a thick midrange harmonic foundation, and a rapid 16th-note up-and-down arpeggio that spans multiple octaves to create melodic contour and rhythmic momentum.

* **Why Use This Skill (Rationale)**: 
The video demonstrates a complex multi-track MIDI editing workflow. To practically utilize and test this workflow (docking the MIDI editor, switching track visibility, Ghost notes, and multi-track drawing), you need a cohesive, multi-layered musical arrangement. Musically, this specific ensemble pattern relies on the psychoacoustic principle of frequency bracketing—each instrument occupies a distinct rhythmic density (16th, 8th, 4th, whole notes) and frequency band (sub, low-mid, mid, high), ensuring a clear, unmuddy mix while building substantial harmonic tension. 

* **Overall Applicability**: 
This ensemble is perfect as a foundational mockup for synthwave, 80s pop, retrowave, cinematic electronic tracks, and driving rock arrangements. It also serves as the ultimate "test bed" project for utilizing REAPER's advanced multi-track MIDI editor features.

* **Value Addition**: 
Instead of generating a static, single-track melody, this skill generates an entire ecosystem of tracks. It encodes standard functional harmony (`i - VI - VII - v` or `I - vi - IV - V`), intelligent voicing generation, and rhythmic counterpoint across four distinct instruments. 


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Drums**: 4/4 grid. Kick drum on beats 1, 2-and, and 3. Snare on beats 2 and 4. Hi-hats playing straight 8th notes with alternating velocities for groove.
  - **Bass**: Continuous, driving 8th notes with a slight staccato gap (legato 90%) and alternating accents.
  - **Chords**: Sustained whole notes holding out the harmonic progression.
  - **Lead Arp**: Continuous 16th notes executing an 8-step up-and-down pattern (Root, 3rd, 5th, 7th, Octave, 7th, 5th, 3rd).

* **Step B: Pitch & Harmony**
  - **Progression**: A cinematic 4-bar progression using scale degrees `[1, 6, 7, 5]` (e.g., Am, F, G, Em in minor). 
  - **Voicing**: 
    - Bass plays root notes in Octave 2/3.
    - Chords play 4-note tertian stacks (7th chords) in Octave 4 to fill the midrange.
    - Arpeggio sweeps across 5 chord tones spanning into Octave 5 and 6.

* **Step C: Sound Design & FX**
  - All tonal tracks (Bass, Chords, Arp) are instantiated with REAPER's stock `ReaSynth` to ensure zero external dependencies while providing immediate playback.
  - Tracks are color-coded (Drums = Red, Bass = Blue, Chords = Green, Arp = Yellow) directly mimicking the visual organization needed for the tutorial's UI workflow.
  - Stereo imaging is applied: Chords are panned 30% Left, and the Lead Arp is panned 30% Right to prevent frequency masking in the center channel.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Setup & Colors | `RPR_InsertTrackAtIndex`, `RPR_SetMediaTrackInfo_Value` | Prepares the multi-track layout exactly as needed for the tutorial's docked MIDI workflow. |
| Harmony & Rhythms | `RPR_MIDI_InsertNote` | Provides exact control over the mathematically generated scale degrees, timings, and alternating groove velocities. |
| Synthesis | `RPR_TrackFX_AddByName` (ReaSynth) | Ensures immediate, self-contained playback without relying on external VSTis (Kontakt, etc.) shown in the video. |
| Mix Separation | `RPR_SetMediaTrackInfo_Value` (Pan & Vol) | Prevents the 4 simultaneous layers from clipping the master bus and creates stereo width. |

> **Feasibility Assessment**: 100% reproducible for the musical composition, layout, and MIDI data. The specific third-party sample libraries (e.g., SSD5 Drums, specific guitar amp sims) are approximated using native ReaSynth to guarantee runtime execution safety.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Synthwave_Ensemble",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-layer Synthwave/Rock ensemble setup for multi-track MIDI editing.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    root_pitch = NOTE_MAP.get(key.capitalize(), 9)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Generate 10 octaves of scale notes for dynamic chord building
    scale_notes = []
    for oct in range(10):
        for interval in intervals:
            scale_notes.append(root_pitch + interval + (oct * 12))
            
    def get_chord(degree: int, octave: int, num_notes: int = 3):
        """Returns a list of absolute MIDI pitches for a chord built on a scale degree."""
        base_idx = octave * len(intervals) + degree
        return [scale_notes[base_idx + i * 2] for i in range(num_notes)]

    # Standard progression: i - VI - VII - v (minor) or I - vi - IV - V (major)
    if scale.lower() == "major":
        progression = [0, 5, 3, 4] 
    else:
        progression = [0, 5, 6, 4] 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks & Items ===
    tracks_info = [
        {"name": "Drums", "color": RPR.RPR_ColorToNative(255, 100, 100) | 0x1000000, "pan": 0.0},
        {"name": "Bass", "color": RPR.RPR_ColorToNative(100, 100, 255) | 0x1000000, "pan": 0.0},
        {"name": "Chords", "color": RPR.RPR_ColorToNative(100, 255, 100) | 0x1000000, "pan": -0.3},
        {"name": "Lead Arp", "color": RPR.RPR_ColorToNative(255, 255, 100) | 0x1000000, "pan": 0.3}
    ]

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    total_len = beat_len * beats_per_bar * bars
    
    takes = []
    for t_info in tracks_info:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # -6dB to prevent clipping
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", t_info["pan"])
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes.append(take)
        
        # Add native synth to tonal tracks
        if t_info["name"] != "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    drums_take, bass_take, chords_take, arp_take = takes

    # === Step 3: Generate MIDI Data ===
    for bar in range(bars):
        bar_start_beats = bar * beats_per_bar
        degree = progression[bar % len(progression)]
        
        # --- 3a. Drums ---
        kicks_qn = [0, 1.5, 2.5] if bar % 2 == 0 else [0, 1.5, 2] # Rock groove
        for k_pos in kicks_qn:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, (bar_start_beats + k_pos) * beat_len)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 240, 0, 36, velocity_base, False)
        
        for s_pos in [1, 3]: # Snare on 2 and 4
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, (bar_start_beats + s_pos) * beat_len)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 240, 0, 38, velocity_base, False)
            
        for h_pos in range(8): # 8th note hi-hats
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, (bar_start_beats + h_pos * 0.5) * beat_len)
            vel = velocity_base if h_pos % 2 == 0 else velocity_base - 25
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 120, 0, 42, vel, False)

        # --- 3b. Bass (8th notes) ---
        bass_note = get_chord(degree, octave=2, num_notes=1)[0]
        for i in range(8):
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, (bar_start_beats + i * 0.5) * beat_len)
            end_ppq = start_ppq + 960 * 0.45 # Leave slight gap for staccato feel
            vel = velocity_base if i % 2 == 0 else velocity_base - 15
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_note, vel, False)

        # --- 3c. Chords (Whole notes) ---
        chord_notes = get_chord(degree, octave=4, num_notes=4) # 7th chords
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, bar_start_beats * beat_len)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, (bar_start_beats + 4) * beat_len)
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, note, velocity_base - 20, False)

        # --- 3d. Lead Arp (16th notes) ---
        arp_notes = get_chord(degree, octave=5, num_notes=5) # Spans up into next octave
        pattern_indices = [0, 1, 2, 3, 4, 3, 2, 1] # Up and down contour
        for i in range(16):
            note = arp_notes[pattern_indices[i % 8]]
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(arp_take, (bar_start_beats + i * 0.25) * beat_len)
            end_ppq = start_ppq + 960 * 0.2 
            RPR.RPR_MIDI_InsertNote(arp_take, False, False, start_ppq, end_ppq, 0, note, velocity_base + 10, False)

    # === Step 4: Finalize ===
    for take in takes:
        RPR.RPR_MIDI_Sort(take)
        
    RPR.RPR_UpdateArrange()

    return f"Created Synthwave Ensemble (4 tracks) over {bars} bars in {key} {scale} at {bpm} BPM."
```
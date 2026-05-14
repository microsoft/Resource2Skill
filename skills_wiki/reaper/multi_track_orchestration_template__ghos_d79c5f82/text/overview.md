### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Orchestration Template (Ghost-Note Layering)

* **Core Musical Mechanism**: The video predominantly teaches a *workflow*—specifically configuring REAPER's MIDI Editor for multi-track "ghost note" visibility (like Logic Pro). The underlying *musical mechanism* demonstrated is **diatonic orchestration across discrete frequency bands**. The arrangement relies on locking multiple instruments (drums, bass, rhythm chords, lead arpeggios) tightly to the same rhythmic grid and harmonic progression, designed to be visualized simultaneously.
* **Why Use This Skill (Rationale)**: Arranging tracks in isolation often leads to frequency clashes and harmonic dissonance. By generating a cohesive baseline (a i - VI - III - VII diatonic progression) colored specifically for REAPER's "Color notes by track" view, this skill provides a structured foundation. The drums anchor the grid, the bass dictates the harmonic root, the rhythm guitar fills the mid-range with block triads, and the lead provides syncopated upper-register movement. 
* **Overall Applicability**: Essential for rock, orchestral mockups, cinematic scoring, and synthwave—any genre where dense, multi-instrument layering requires strict harmonic alignment and visual organization.
* **Value Addition**: Instead of starting with a blank project, this skill automatically scaffolds four distinct, color-coded tracks pre-populated with an interlocking 4-bar progression. It encodes diatonic chord theory (automatically wrapping intervals to stay within the key) and rhythm section roles, setting up the exact environment the video demonstrates.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Time Signature & Tempo**: 4/4 time, typically 110-130 BPM (driving rock/metal feel).
  * **Grid Divisions**:
    * *Drums*: 1/4 note kick/snare backbeat, 1/8 note hi-hats.
    * *Bass*: Pumping 1/8 note roots.
    * *Rhythm*: Sustained whole notes (chords).
    * *Lead*: 1/8 note ascending arpeggios providing melodic momentum.
* **Step B: Pitch & Harmony**
  * **Progression**: i - VI - III - VII (Relative scale degrees: 0, 5, 2, 6). Very common in epic/cinematic music.
  * **Voicings**: The code uses a robust diatonic chord builder. It calculates the root, third, and fifth strictly within the selected scale array, automatically shifting octaves when notes wrap past the 7th scale degree.
* **Step C: Sound Design & FX**
  * Because the video focuses on the MIDI editor, this script focuses heavily on *MIDI population and track aesthetic setup*. It strictly assigns specific RGB colors to tracks to utilize REAPER's `View -> Color notes by track` feature shown in the tutorial.
* **Step D: Mix & Automation**
  * Tracks are grouped and color-coded. No heavy audio FX are added to ensure this serves cleanly as a compositional MIDI starting point.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Color Coding | `RPR_SetTrackColor` | The video emphasizes visualizing multiple tracks. Distinct colors (Indigo, Purple, Orange, Blue) are essential for this workflow. |
| Harmony & Notes | `RPR_MIDI_InsertNote` | Precise programmatic insertion of notes allows us to mathematically build diatonic triads and arpeggios in *any* key or scale the user requests. |
| Arrangement | Project Track Insertion | Creates a non-destructive, additive setup where four distinct tracks represent the ensemble demonstrated in the tutorial. |

> **Feasibility Assessment**: 100% reproduction of the musical arrangement *concept* demonstrated in the video. While the tutorial uses premium VSTs (Kontakt guitars/drums), this code generates the universal MIDI data that drives those instruments, making it perfectly reproducible on any system without external dependencies.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Orchestral_Rock_Template",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track interlocking arrangement (Drums, Bass, Rhythm, Lead)
    specifically color-coded for REAPER's "Color notes by track" workflow.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "B").
        scale: Scale type (major, minor, dorian, etc.).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    key_offset = NOTE_MAP.get(key.capitalize(), 11) # Default to B if not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * 4
    
    # Helper to calculate diatonic pitches (auto-wraps octaves)
    def get_diatonic_pitch(degree_index, base_octave_note):
        octave_shift = degree_index // len(scale_intervals)
        scale_degree = degree_index % len(scale_intervals)
        return base_octave_note + key_offset + (octave_shift * 12) + scale_intervals[scale_degree]

    # Helper to create a track with a properly colored MIDI item
    def create_colored_track(name_suffix, rgb_tuple):
        RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
        track = RPR.RPR_GetTrack(0, RPR.RPR_CountTracks(0) - 1)
        full_name = f"{track_name} - {name_suffix}"
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_name, True)
        
        # Apply color: R + (G<<8) + (B<<16) + 0x1000000 (valid custom color flag)
        r, g, b = rgb_tuple
        color_val = r | (g << 8) | (b << 16) | 0x1000000
        RPR.RPR_SetTrackColor(track, color_val)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # Colors mapping to the tutorial's aesthetic
    take_drums = create_colored_track("Drums", (75, 0, 130))       # Indigo
    take_bass = create_colored_track("Bass", (128, 0, 128))        # Purple
    take_rhythm = create_colored_track("Rhythm Gtr", (255, 165, 0))# Orange
    take_lead = create_colored_track("Lead Gtr", (0, 150, 255))    # Blue

    # Progression: i - VI - III - VII (0, 5, 2, 6 in zero-indexed diatonic math)
    progression = [0, 5, 2, 6]
    
    # --- Generate Notes ---
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # 1. DRUMS (Standard Rock Beat)
        for beat in range(4):
            # Kick (36) on 1 & 3, Snare (38) on 2 & 4
            drum_pitch = 36 if beat % 2 == 0 else 38
            pos_sec = (bar * bar_sec) + (beat * beat_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, pos_sec + (beat_sec * 0.5))
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, drum_pitch, velocity_base, True)
            
            # Hi-hats (42) every 8th note
            for eighth in [0, 0.5]:
                hh_pos = pos_sec + (eighth * beat_sec)
                hh_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hh_pos)
                hh_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hh_pos + (beat_sec * 0.25))
                vel = velocity_base if eighth == 0 else int(velocity_base * 0.7)
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, hh_start, hh_end, 9, 42, vel, True)
        
        # Add Crash (49) on the very first beat
        if bar == 0:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, 0)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, beat_sec)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, 49, velocity_base + 10, True)

        # 2. BASS (Pumping 8th notes, C2 base = 36)
        bass_pitch = get_diatonic_pitch(degree, 36)
        for eighth in range(8):
            pos_sec = (bar * bar_sec) + (eighth * 0.5 * beat_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, pos_sec + (0.45 * beat_sec)) # Slight staccato
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, True)

        # 3. RHYTHM GUITAR (Sustained Triads, C3 base = 48)
        pos_sec = bar * bar_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_rhythm, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_rhythm, pos_sec + bar_sec)
        
        triad_degrees = [degree, degree + 2, degree + 4] # Root, 3rd, 5th
        for d in triad_degrees:
            chord_pitch = get_diatonic_pitch(d, 48)
            RPR.RPR_MIDI_InsertNote(take_rhythm, False, False, start_ppq, end_ppq, 0, chord_pitch, int(velocity_base*0.9), True)

        # 4. LEAD GUITAR (Ascending 8th note Arpeggios, C4 base = 60)
        # Pattern: Root, 3rd, 5th, Octave
        arp_degrees = [degree, degree + 2, degree + 4, degree + 7]
        for beat in range(4):
            for eighth in [0, 0.5]:
                note_idx = beat if eighth == 0 else (beat + 1) % 4
                arp_pitch = get_diatonic_pitch(arp_degrees[note_idx], 60)
                
                pos_sec = (bar * bar_sec) + (beat * beat_sec) + (eighth * beat_sec)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_lead, pos_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_lead, pos_sec + (0.4 * beat_sec))
                RPR.RPR_MIDI_InsertNote(take_lead, False, False, start_ppq, end_ppq, 0, arp_pitch, velocity_base, True)

    # Sort MIDI events for all takes to ensure they play and display correctly
    for take in [take_drums, take_bass, take_rhythm, take_lead]:
        RPR.RPR_MIDI_Sort(take)

    return f"Created multi-track orchestration (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {scale} at {bpm} BPM."
```
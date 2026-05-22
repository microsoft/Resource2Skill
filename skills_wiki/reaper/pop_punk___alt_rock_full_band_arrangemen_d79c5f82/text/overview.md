### 1. High-level Design Pattern Extraction

> **Skill Name**: Pop-Punk / Alt-Rock Full Band Arrangement (vi-IV-I-V)

* **Core Musical Mechanism**: The video tutorial demonstrates Reaper's multi-track MIDI editing capabilities by arranging a multi-part instrumental rock loop. The signature of this pattern is a driving **vi - IV - I - V** chord progression (e.g., Bm - G - D - A), which forms the bedrock of countless pop-punk, alternative rock, and modern pop anthems. It utilizes strict frequency stratification: a pulsing root-note bass, mid-range thick power chords, high-end melodic lead arpeggios, and an aggressive 8th-note rock drum groove.
* **Why Use This Skill (Rationale)**: This arrangement template works musically because of the interplay between constant rhythmic momentum (8th-note bass/guitar chugging and hi-hats) and soaring harmonic resolution. The vi-IV-I-V progression balances emotional tension (starting on the minor vi chord) with anthemic release (resolving through the major IV and I before resetting on the dominant V).
* **Overall Applicability**: This acts as a foundation for rock, pop-punk, emo, or modern pop productions. It serves as an excellent starting point/scaffold for a verse or chorus that needs immediate energy and a full-band feel.
* **Value Addition**: Compared to a blank project, this skill automatically creates a fully routed, mathematically locked 4-piece band arrangement (Drums, Bass, Rhythm Guitar, Lead Guitar). It encodes the specific drum mappings (Kick, Snare, Hi-Hat, Crash) and computes the exact relative intervals for power chords and syncopated lead motifs based on the chosen key and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 150-170 BPM (Pop-punk standard).
  - **Grid**: Straight 8th notes (no swing).
  - **Drums**: Kick on 1 and 2-and (syncopated). Snare on 2 and 4. Hi-hats on straight 8ths.
  - **Bass & Rhythm Guitar**: Relentless straight 8th notes driving the chord progression.
* **Step B: Pitch & Harmony**
  - **Progression**: vi - IV - I - V (or i - VI - III - VII in minor).
  - **Voicings**: Rhythm guitar uses 3-note power chords (Root, Perfect 5th, Octave). This avoids major/minor 3rds in the guitar, leaving room for the lead and avoiding low-mid mud.
  - **Bass**: Plays single root notes, dropping an octave down from the guitar.
  - **Lead**: A syncopated 8th-note arpeggio highlighting the 3rd and 5th scale degrees.
* **Step C: Sound Design & FX**
  - Synthesizers: Placeholders (like ReaSynth) are used to generate instant tone, setting the rhythm elements lower with square/saw waves, and the lead with a higher, brighter tone.
* **Step D: Mix & Automation**
  - Bass is mixed center; Rhythm guitars usually panned wide (represented as a single mid-range track here); Lead sits above them.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track arrangement | `RPR_InsertTrackAtIndex` | Builds the full 4-piece band structure safely without touching existing tracks. |
| Notes & Chords | `RPR_MIDI_InsertNote` | Computes the progression, power chord intervals, and drum hits dynamically based on user-defined Key/Scale/BPM. |
| Tone Generation | `RPR_TrackFX_AddByName` | Adds REAPER's native `ReaSynth` so the MIDI immediately produces an audible pitch reference upon creation. |

> **Feasibility Assessment**: 100% reproducible for the MIDI arrangement and structural template. The specific third-party VST amp simulators and drum samplers used in the video (like GetGood Drums or Neural DSP) are replaced by standard MIDI layouts and native REAPER synths to guarantee execution in any environment.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "PopPunkAnthem",
    track_name: str = "RockBand",
    bpm: int = 160,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full 4-track Pop-Punk / Alt-Rock arrangement (vi-IV-I-V).
    Includes Drums, Bass, Rhythm Guitar (Power Chords), and a Lead Arpeggio.
    """
    import reaper_python as RPR

    # --- Musical Math & Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key, 2)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Standard rock progression: vi - IV - I - V in Major, or i - VI - III - VII in Minor
    if scale == "major":
        progression_degrees = [5, 3, 0, 4] # 0-indexed (vi, IV, I, V)
    else:
        progression_degrees = [0, 5, 2, 6] # 0-indexed (i, VI, III, VII)

    def get_pitch_in_scale(degree, base_octave):
        """Calculates exact MIDI pitch for a scale degree and octave."""
        deg_mod = degree % 7
        octave_shift = degree // 7
        return (base_octave + octave_shift + 1) * 12 + root_val + scale_intervals[deg_mod]

    # --- Project Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars

    def add_midi_track(name, y_color=None):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Add basic tone generator
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Add MIDI item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take, item

    def insert_note(take, start_beat, end_beat, pitch, vel=100):
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # 1. DRUMS TRACK
    take_drums, _ = add_midi_track(f"{track_name}_Drums")
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        # Kick (36) on 1, 2.5, 3.5
        insert_note(take_drums, bar_offset + 0.0, bar_offset + 0.5, 36, velocity_base)
        insert_note(take_drums, bar_offset + 1.5, bar_offset + 2.0, 36, velocity_base - 10)
        insert_note(take_drums, bar_offset + 2.5, bar_offset + 3.0, 36, velocity_base)
        
        # Snare (38) on 2 and 4
        insert_note(take_drums, bar_offset + 1.0, bar_offset + 1.5, 38, velocity_base + 10)
        insert_note(take_drums, bar_offset + 3.0, bar_offset + 3.5, 38, velocity_base + 10)
        
        # Hi-Hats (42) straight 8ths
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 20
            insert_note(take_drums, bar_offset + (i * 0.5), bar_offset + (i * 0.5) + 0.25, 42, vel)
            
        # Crash (49) on downbeat of first bar
        if bar == 0:
            insert_note(take_drums, bar_offset + 0.0, bar_offset + 1.0, 49, velocity_base + 15)
    
    RPR.RPR_MIDI_Sort(take_drums)

    # 2. BASS TRACK
    take_bass, _ = add_midi_track(f"{track_name}_Bass")
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        deg = progression_degrees[bar % len(progression_degrees)]
        pitch = get_pitch_in_scale(deg, 2) # Octave 2
        
        # Driving 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 10
            insert_note(take_bass, bar_offset + (i * 0.5), bar_offset + (i * 0.5) + 0.45, pitch, vel)
    RPR.RPR_MIDI_Sort(take_bass)

    # 3. RHYTHM GUITAR TRACK (POWER CHORDS)
    take_gtr, _ = add_midi_track(f"{track_name}_RhythmGtr")
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        deg = progression_degrees[bar % len(progression_degrees)]
        root_pitch = get_pitch_in_scale(deg, 3) # Octave 3
        fifth_pitch = root_pitch + 7 # Perfect 5th
        octave_pitch = root_pitch + 12 # Octave
        
        # Driving 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 15
            insert_note(take_gtr, bar_offset + (i * 0.5), bar_offset + (i * 0.5) + 0.45, root_pitch, vel)
            insert_note(take_gtr, bar_offset + (i * 0.5), bar_offset + (i * 0.5) + 0.45, fifth_pitch, vel)
            insert_note(take_gtr, bar_offset + (i * 0.5), bar_offset + (i * 0.5) + 0.45, octave_pitch, vel)
    RPR.RPR_MIDI_Sort(take_gtr)

    # 4. LEAD GUITAR TRACK
    take_lead, _ = add_midi_track(f"{track_name}_LeadGtr")
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        # Create a syncopated repeating arpeggio sequence using scale degrees (0, 2, 4 = 1st, 3rd, 5th)
        deg_1 = get_pitch_in_scale(0, 5) # Root, up high
        deg_3 = get_pitch_in_scale(2, 5) # Third
        deg_5 = get_pitch_in_scale(4, 5) # Fifth
        
        # Syncopated 3-3-2 rhythmic motif (8th notes: 123 123 12)
        pattern = [
            (0.0, 0.5, deg_5),
            (0.5, 1.0, deg_3),
            (1.0, 1.5, deg_1),
            
            (1.5, 2.0, deg_5),
            (2.0, 2.5, deg_3),
            (2.5, 3.0, deg_1),
            
            (3.0, 3.5, deg_5),
            (3.5, 4.0, deg_3)
        ]
        
        for start, end, pitch in pattern:
            insert_note(take_lead, bar_offset + start, bar_offset + end, pitch, velocity_base + 5)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created full Rock Band template (4 tracks) over {bars} bars at {bpm} BPM in {key} {scale}."
```
### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Synthwave Foundation (Drums, Bass, Rhythm, Lead)

* **Core Musical Mechanism**: This pattern represents a fully synchronized 4-layer arrangement template (Drums, Bass, Rhythm Chords, Lead Arpeggio). The signature of this pattern is vertical integration: a driving 4/4 drum groove locked with an 8th-note pulsing root-note bassline, supported by sustained mid-range block chords, and topped with a 16th-note high-register arpeggiator. 
* **Why Use This Skill (Rationale)**: In the tutorial, the creator demonstrates REAPER's multi-track MIDI editing capabilities by arranging a full band segment. Musically, this works because it covers the entire frequency spectrum and rhythmic grid efficiently without masking. The kick and bass anchor the low end on the downbeats; the rhythm guitar fills the midrange harmony; the hi-hats and lead synth provide high-frequency rhythmic subdivision and forward momentum.
* **Overall Applicability**: This is the fundamental building block for rock, metal, pop-punk, and synthwave drops/choruses. It instantly provides a "full band" context to test chord progressions or vocal melodies against.
* **Value Addition**: Instead of a single flat MIDI clip, this skill encodes orchestration logic. It mathematically derives basslines, block chords, and arpeggios from a single master chord progression and maps them to appropriate instruments and octaves automatically.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, default 120 BPM.
  - **Drums**: Standard rock groove. Kick on beats 1 and 3; Snare on 2 and 4; Hi-hats driving continuous 8th notes. Crash on the downbeat of bar 1.
  - **Bass**: Continuous 8th-note pulses (staccato) locking exactly with the kick and hi-hat.
  - **Rhythm**: Whole notes holding the chord triads across each bar.
  - **Lead**: 16th-note arpeggiations subdividing the beat and creating rhythmic energy.

* **Step B: Pitch & Harmony**
  - **Progression**: The skill uses a highly reusable i - VI - III - VII progression (e.g., Bm - G - D - A if in B minor).
  - **Bass Layer**: Plays the root note of the current chord, dropped 2 octaves below the melody.
  - **Rhythm Layer**: Plays the 1st, 3rd, and 5th scale degrees relative to the current chord root, placed in the midrange (Octave 4).
  - **Lead Layer**: Arpeggiates the chord stack (Root, 3rd, 5th, Octave) two octaves up (Octave 5/6).

* **Step C: Sound Design & FX**
  - **Drums**: General MIDI mapping on Channel 10 (Kick 36, Snare 38, Hi-hat 42, Crash 49).
  - **Tonal Layers**: Routed to REAPER's stock `ReaSynth`. The bass is placed in the low registers to mimic a synth bass/bass guitar, while the rhythm and lead take the midrange and highs.

* **Step D: Mix & Automation**
  - Volumes are staggered to prevent clipping: Bass and Drums hit hardest (Velocity 100-110), Rhythm chords are softened to sit in the background (Velocity 85), and the Lead cuts through with articulate velocity (Velocity 95).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track Orchestration | `RPR_InsertTrackAtIndex` & `RPR_AddMediaItemToTrack` | Creates the specific 4-layer vertical stack shown in the tutorial. |
| Harmonic Sync | Python algorithmic generation | Derives bass roots, triads, and arpeggios dynamically from a single scale definition. |
| Sound Design | `RPR_TrackFX_AddByName("ReaSynth")` | Uses stock REAPER plugins to ensure the tonal MIDI is immediately audible without external VSTs. |

> **Feasibility Assessment**: 100% reproducible for the MIDI patterns and orchestration logic. The specific VSTs (like Kontakt libraries) used in the tutorial video are replaced with REAPER's stock `ReaSynth` to ensure the code executes safely and audibly on any machine.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Band_Foundation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Rock/Synthwave arrangement (Drums, Bass, Rhythm, Lead).
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
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    # Setup base pitch and scale
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_pitch(degree, octave):
        """Convert a scale degree (0-indexed) to an absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[scale_idx] + (octave + octave_shift) * 12

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    total_length_sec = bar_sec * bars
    
    # i - VI - III - VII progression (relative scale degrees)
    progression = [0, 5, 2, 4] 

    def create_layer(name, add_synth=True, color=0):
        """Helper to create a track and a blank MIDI take."""
        track_idx = RPR.RPR_GetNumTracks()
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        if add_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        return take
        
    def add_note(take, start_beat, duration_beats, pitch, vel, chan=0):
        start_time = start_beat * beat_sec
        end_time = (start_beat + duration_beats) * beat_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    # --- 1. DRUMS LAYER ---
    take_drums = create_layer("Drums", add_synth=False)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Crash on first bar
        if bar == 0:
            add_note(take_drums, bar_start_beat, 1.0, 49, velocity_base + 10, chan=9)
            
        # Kick (1 and 3) & Snare (2 and 4)
        for beat in range(4):
            if beat % 2 == 0: # Beats 1, 3 (0-indexed 0, 2)
                add_note(take_drums, bar_start_beat + beat, 0.5, 36, velocity_base + 10, chan=9)
            else:             # Beats 2, 4 (0-indexed 1, 3)
                add_note(take_drums, bar_start_beat + beat, 0.5, 38, velocity_base + 5, chan=9)
                
        # 8th Note Hi-Hats
        for eighth in range(8):
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 20 # Accent downbeats
            add_note(take_drums, bar_start_beat + (eighth * 0.5), 0.25, 42, vel, chan=9)
            
    RPR.RPR_MIDI_Sort(take_drums)

    # --- 2. BASS LAYER ---
    take_bass = create_layer("Bass", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        bass_pitch = get_pitch(chord_root, 2) # Octave 2
        
        # 8th note driving pulses
        for eighth in range(8):
            add_note(take_bass, bar_start_beat + (eighth * 0.5), 0.45, bass_pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(take_bass)

    # --- 3. RHYTHM LAYER (Chords) ---
    take_rhythm = create_layer("Rhythm", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        
        # Triad degrees (Root, 3rd, 5th)
        chord_degrees = [chord_root, chord_root + 2, chord_root + 4]
        for deg in chord_degrees:
            pitch = get_pitch(deg, 4) # Octave 4
            add_note(take_rhythm, bar_start_beat, 3.9, pitch, velocity_base - 15)
            
    RPR.RPR_MIDI_Sort(take_rhythm)

    # --- 4. LEAD LAYER (Arpeggios) ---
    take_lead = create_layer("Lead", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        
        # Arpeggio pattern (Root, 3rd, 5th, Octave)
        arp_degrees = [chord_root, chord_root + 2, chord_root + 4, chord_root + 7]
        
        # 16th note arpeggiator
        for sixteenth in range(16):
            deg = arp_degrees[sixteenth % 4]
            pitch = get_pitch(deg, 5) # Octave 5
            add_note(take_lead, bar_start_beat + (sixteenth * 0.25), 0.2, pitch, velocity_base - 5)

    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track Foundation ({bars} bars) at {bpm} BPM in {key} {scale}."
```
# Nu-Disco / French Touch Groove (Daft Punk Style)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Nu-Disco / French Touch Groove (Daft Punk Style)

* **Core Musical Mechanism**: This pattern relies on a strict combination of four elements: a heavily quantized "four-on-the-floor" drum loop with syncopated 16th-note hi-hats, a bouncy staccato bassline built on the minor pentatonic or Dorian scale, rapid 16th-note rhythmic guitar/synth stabs (often heavily compressed), and a robotic synthesized vocal layer (Vocoder).
* **Why Use This Skill (Rationale)**: The magic of this style lies in the interlocking 16th-note grid. The kick and snare anchor the groove, while the bass and guitar/keys dance around the off-beats (the "e" and "a" of the 16th note subdivisions). The Dorian mode provides a characteristic minor but upbeat, sophisticated harmony (due to the major 6th interval). The vocoder introduces a psychoacoustic blend of human expression and synthesized tonal perfection.
* **Overall Applicability**: Essential for funk, nu-disco, French house, and modern pop tracks. It provides an instant "danceable" foundation.
* **Value Addition**: This skill moves beyond static chords by implementing an interlocking, multi-track rhythmic arrangement. It establishes a complete groove pocket with rhythmically distinct roles for drums, bass, and harmony, plus the foundational FX chain for a vocoder setup.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: 110 - 120 (Standard for Nu-Disco).
  - **Time Signature**: 4/4.
  - **Grid**: 1/16th notes.
  - **Drum Rhythm**: Kick on 1, 2, 3, 4. Snare on 2 and 4. Open hi-hats on the "and" (8th-note off-beats), closed hats on 16th subdivisions.
  - **Bass/Guitar Rhythm**: Staccato notes, heavily utilizing the 16th-note off-beats just before the downbeats (anticipation).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically Dorian or natural minor. (Defaulting to A Dorian).
  - **Bass**: Root, minor 3rd, perfect 4th, perfect 5th, minor 7th.
  - **Chords**: Minor 7th (Root, m3, P5, m7) and Dominant 9th voicings.

* **Step C: Sound Design & FX**
  - **Drums**: Tight, punchy electronic/acoustic blend.
  - **Bass**: Analog synth, short decay, low filter cutoff.
  - **Chords**: Clean, plucky sounds.
  - **Vocoder**: A carrier synth (sawtooth/pulse) routed into a vocoder plugin alongside a modulator (vocal track).

* **Step D: Mix & Automation**
  - Tight leveling: Kick and bass dominate the low end, guitar/keys heavily high-passed to avoid masking the bass. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Drums** | MIDI note insertion | Requires precise drum mapping (Kick 36, Snare 38, Hats 42/46) and 16th-note timing. |
| **Bass & Keys Groove** | MIDI note insertion | Captures the syncopated, interlocking rhythmic relationship between the low and mid frequencies. |
| **Vocoder Setup** | FX chain insertion | Emulates "Step 4" by setting up a track with ReaVocoder, preparing the session for robotic vocals. |

> **Feasibility Assessment**: 80%. The exact tonal character of the vintage Sennheiser vocoder and the specific analog synths/guitars used by Daft Punk require specialized 3rd-party plugins. However, the MIDI groove (the notes, rhythm, and structural relationships) and the stock REAPER FX setup are 100% reproducible and form the true core of the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "RandomAccessGroove",
    track_name: str = "French_Touch",
    bpm: int = 115,
    key: str = "A",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Nu-Disco / French Touch Groove in the current REAPER project.
    Generates 4 tracks representing the tutorial steps: Drums, Bass, Keys/Guitar, and a Vocoder setup.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (110-120 recommended).
        key: Root note (e.g., "A").
        scale: Scale type (e.g., "dorian", "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor":  [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 9) # Default to A
    scale_intervals = SCALES.get(scale.lower(), SCALES["dorian"])
    
    # Octave offsets
    bass_root = 36 + root_val # MIDI octave 2/3
    keys_root = 60 + root_val # MIDI octave 4/5
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    def add_track_with_midi(name, is_drum=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, take

    def insert_note(take, start_beat, length_beats, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- TRACK 1: DRUMS (Step 3 in Video) ---
    drum_track, drum_take = add_track_with_midi(f"{track_name}_Drums", True)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1) # Placeholder for drum sampler
    
    for b in range(bars):
        bar_offset = b * 4.0
        # Kick (Four on the floor)
        for beat in [0.0, 1.0, 2.0, 3.0]:
            insert_note(drum_take, bar_offset + beat, 0.25, 36, velocity_base + 10)
        # Snare (Backbeat)
        for beat in [1.0, 3.0]:
            insert_note(drum_take, bar_offset + beat, 0.25, 38, velocity_base + 15)
        # Hi-Hats (16ths, open on off-beats)
        for sub in range(16):
            beat_pos = sub * 0.25
            is_offbeat = (sub % 2 != 0)
            is_eighth_and = (sub % 4 == 2)
            
            if is_eighth_and:
                # Open Hat
                insert_note(drum_take, bar_offset + beat_pos, 0.25, 46, velocity_base)
            else:
                # Closed Hat
                vel = velocity_base - 30 if is_offbeat else velocity_base - 10
                insert_note(drum_take, bar_offset + beat_pos, 0.125, 42, vel)
    RPR.RPR_MIDI_Sort(drum_take)

    # --- TRACK 2: FUNKY BASS (Step 2 in Video) ---
    bass_track, bass_take = add_track_with_midi(f"{track_name}_Bass")
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Syncopated minor/dorian bass riff
    bass_riff = [
        (0.0,  0, 0.25),   # Downbeat Root
        (0.75, 0, 0.25),   # Anticipation Root
        (1.5,  3, 0.25),   # 4th
        (2.0,  0, 0.25),   # Downbeat Root
        (2.5,  2, 0.25),   # minor 3rd
        (3.0,  0, 0.25),   # Root
        (3.75, 4, 0.25)    # 5th anticipation
    ]
    
    for b in range(bars):
        bar_offset = b * 4.0
        for start_offset, scale_deg, length in bass_riff:
            pitch = bass_root + scale_intervals[scale_deg]
            insert_note(bass_take, bar_offset + start_offset, length, pitch, velocity_base)
    RPR.RPR_MIDI_Sort(bass_take)

    # --- TRACK 3: FUNKY GUITAR/KEYS (Step 1 in Video) ---
    keys_track, keys_take = add_track_with_midi(f"{track_name}_Keys")
    RPR.RPR_TrackFX_AddByName(keys_track, "ReaSynth", False, -1)
    
    # Minor 7th chord (Root, m3, P5, m7)
    chord_pitches = [
        keys_root, 
        keys_root + scale_intervals[2], 
        keys_root + scale_intervals[4], 
        keys_root + scale_intervals[6]
    ]
    
    # Syncopated 16th stabs
    keys_rhythm = [0.5, 1.25, 2.5, 3.75]
    
    for b in range(bars):
        bar_offset = b * 4.0
        for start_offset in keys_rhythm:
            for pitch in chord_pitches:
                insert_note(keys_take, bar_offset + start_offset, 0.125, pitch, velocity_base - 10)
    RPR.RPR_MIDI_Sort(keys_take)

    # --- TRACK 4: VOCODER SETUP (Step 4 in Video) ---
    # We add a dedicated track with ReaVocoder to satisfy the sound design step
    vocoder_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(vocoder_track_idx, True)
    vocoder_track = RPR.RPR_GetTrack(0, vocoder_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(vocoder_track, "P_NAME", f"{track_name}_Vocoder", True)
    
    # Add a Synth as Carrier, and ReaVocoder
    RPR.RPR_TrackFX_AddByName(vocoder_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(vocoder_track, "ReaVocoder", False, -1)

    return f"Created Nu-Disco Groove '{track_name}' in {key} {scale} with Drums, Bass, Keys, and Vocoder track over {bars} bars at {bpm} BPM."
```
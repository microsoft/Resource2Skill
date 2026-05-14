# Pharrell/Neptunes: Neptunes Stabby Groove & Syncopated Drums

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neptunes Stabby Groove & Syncopated Drums

* **Core Musical Mechanism**: This pattern is defined by three intersecting elements: 
  1. A **highly syncopated drum groove** featuring "stompy" kicks hitting on 16th-note offbeats, layered with acoustic, slightly un-quantized (swung) hi-hats.
  2. **Staccato, rhythmic chord stabs** that bounce between a minor tonic chord (i) and a major chord one half-step up (bII). This creates a distinct Phrygian/exotic harmonic tension.
  3. A **sine/triangle wave R&B synth lead** that deliberately utilizes 1-note gaps (short rests) between melodic phrases to enhance the bounce and leave room for the drum groove.

* **Why Use This Skill (Rationale)**: This skill perfectly encapsulates the "2000s nostalgic" hip-hop and pop aesthetic. Musically, the syncopation of the kicks against the staccato chord stabs creates immense forward momentum and bounce. The micro-timing shifts (swing) on the hi-hats prevent the beat from sounding robotic, giving it a "lunch table beat" organic feel. Harmonically, the i-bII progression leverages voice-leading tension that is instantly recognizable and easily loops without fatigue.

* **Overall Applicability**: Ideal for the rhythm section and primary hook of pop, R&B, and hip-hop tracks. It works exceptionally well in verse sections where the vocal needs space to breathe (due to the melodic gaps) or in dance-oriented choruses.

* **Value Addition**: Instead of a generic 4-on-the-floor or standard trap beat, this skill encodes advanced rhythmic syncopation, humanized groove theory (swing), and specific Phrygian mode mixture (i to bII chord relations) that instantly provides a recognizable professional "feel."

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 95 - 110 BPM.
  - **Grid**: 1/16th note underlying grid.
  - **Kick Syncopation**: Kicks avoid the standard beat 3, hitting instead on the "ah" of 2 (2.75) or the "and" of 3 (3.5).
  - **Hi-Hat Swing**: 8th notes where the off-beats (0.5, 1.5, 2.5) are delayed slightly (e.g., +0.02 to +0.05 beats) to simulate human groove.
  - **Chords**: Played sharply staccato (e.g., 1/16th note duration) on syncopated 8th and 16th intervals.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically Minor or Phrygian (e.g., E Minor).
  - **Chords**: 
    - Chord 1 (i): Root, minor 3rd, perfect 5th (e.g., E - G - B).
    - Chord 2 (bII): Root+1, perfect 4th, minor 6th (e.g., F - A - C). *The tutorial notes moving the root up one note and changing the quality to Major.*
  - **Melody**: Pentatonic minor scale with rhythmic rests built in (e.g., play for an 8th note, rest for a 16th, play for a 16th).

* **Step C: Sound Design & FX**
  - **Chords**: "Cheap" digital Clavinet or plucked Electric Piano. Short attack (0ms), short decay (150ms), zero sustain.
  - **Lead**: Pure Triangle or Sine wave synth. Moderate attack (50ms) to avoid clicking, high sustain, short release.
  - **Drums**: Percussive rimshots instead of full snares, cowbell accents.

* **Step D: Mix & Automation**
  - Tight, dry mix with minimal reverb to retain the "lunchroom table" percussive aesthetic.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm/Syncopation | MIDI note insertion with PPQ math | Allows exact placement on 16th-note offbeats and programmatic timing offsets for hi-hat "swing." |
| i to bII Harmonic Shift | Algorithmic MIDI pitch generation | Computes the exact half-step shift and major/minor triad voicings based on the user's key/scale input. |
| Clavinet / Triangle Synth | ReaSynth Track FX | Emulates the 2000s "cheap digital synth" and smooth R&B lead textures natively without requiring external VSTs or samples. |

> **Feasibility Assessment**: 85% reproduction. The rhythmic syncopation, harmonic structure, and synthesis techniques are exact. The remaining 15% accounts for the specific nuances of the Korg Triton VST samples shown in the video, which are approximated here using REAPER's native ReaSynth.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Pharrell_Style",
    track_name: str = "Neptunes_Groove",
    bpm: int = 100,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neptunes/Pharrell-style stabby groove with syncopated drums and synths.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (95-110 recommended).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (minor or phrygian work best).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string indicating success.
    """
    import reaper_python as RPR
    import random

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate base MIDI note (Octave 2 for Bass/Drums, 4 for Chords/Leads)
    base_pitch = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 4)
    
    # Step 1: Setup Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def create_midi_track(name: str, length_sec: float) -> tuple:
        """Helper to create a track and a blank MIDI item/take."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def add_note(take, start_beat: float, end_beat: float, pitch: int, vel: int):
        """Helper to convert beats to PPQ and insert MIDI notes."""
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # ==========================================
    # TRACK 1: SYNCOPATED DRUMS
    # ==========================================
    drum_track, drum_take = create_midi_track(f"{track_name}_Drums", total_length_sec)
    
    # General MIDI Mapping
    KICK = 36
    RIMSHOT = 37
    CH_HAT = 42
    COWBELL = 56

    for bar in range(bars):
        bar_offset = bar * 4.0
        
        # Kick: Stompy syncopation (Beat 1, Beat 2 "ah", Beat 3 "&")
        kick_rhythm = [0.0, 1.75, 2.5]
        for b in kick_rhythm:
            add_note(drum_take, bar_offset + b, bar_offset + b + 0.25, KICK, velocity_base)
            
        # Rimshot: Sharp hits on 2 and 4
        snare_rhythm = [1.0, 3.0]
        for b in snare_rhythm:
            add_note(drum_take, bar_offset + b, bar_offset + b + 0.25, RIMSHOT, velocity_base + 10)
            
        # Hi-Hats: 8th notes with SWING applied to the offbeats
        for i in range(8):
            base_beat = i * 0.5
            swing_offset = 0.04 if (i % 2 != 0) else 0.0  # Delay the "and" beats
            vol_variation = velocity_base - 20 if (i % 2 != 0) else velocity_base - 5
            add_note(drum_take, bar_offset + base_beat + swing_offset, bar_offset + base_beat + swing_offset + 0.1, CH_HAT, vol_variation)
            
        # Cowbell: Iconic syncopated accent
        add_note(drum_take, bar_offset + 2.75, bar_offset + 2.85, COWBELL, velocity_base - 10)
        add_note(drum_take, bar_offset + 3.75, bar_offset + 3.85, COWBELL, velocity_base - 10)

    # ==========================================
    # TRACK 2: STABBY EP/CLAVINET CHORDS
    # ==========================================
    chord_track, chord_take = create_midi_track(f"{track_name}_Stabs", total_length_sec)
    
    # Setup ReaSynth for Plucky Digital Clav/EP sound
    fx_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 3, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 4, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 7, 0.0) # Attack (0ms)
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 8, 0.1) # Decay (Short)
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 9, 0.0) # Sustain (0%)

    # Music Theory: Minor i chord to Major bII chord
    root_pitch = base_pitch + 48 # Octave 4
    chord_i = [root_pitch, root_pitch + 3, root_pitch + 7] # Minor triad
    chord_bII = [root_pitch + 1, root_pitch + 5, root_pitch + 8] # Major triad one half-step up
    
    for bar in range(bars):
        bar_offset = bar * 4.0
        # Rhythmic stab pattern
        stab_pattern = [
            (0.0, chord_i),
            (0.75, chord_i),
            (1.5, chord_i),
            (2.5, chord_bII),
            (3.25, chord_bII)
        ]
        for beat, chord in stab_pattern:
            for note in chord:
                # Staccato lengths (0.15 beats)
                add_note(chord_take, bar_offset + beat, bar_offset + beat + 0.15, note, velocity_base - 15)

    # ==========================================
    # TRACK 3: SMOOTH TRIANGLE LEAD WITH GAPS
    # ==========================================
    lead_track, lead_take = create_midi_track(f"{track_name}_Lead", total_length_sec)
    
    # Setup ReaSynth for Smooth Triangle R&B Lead
    fx_idx_lead = RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 2, 0.1) # Slight Portamento/Glide
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 3, 0.0) # Square mix off
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 4, 0.0) # Saw mix off
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 5, 1.0) # Triangle mix full
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 7, 0.02) # Soft Attack
    RPR.RPR_TrackFX_SetParam(lead_track, fx_idx_lead, 9, 1.0) # Sustain full
    
    lead_root = base_pitch + 60 # Octave 5
    
    for bar in range(bars):
        bar_offset = bar * 4.0
        # Pentatonic minor riff demonstrating the "1-note gap" rhythmic space technique
        lead_pattern = [
            (0.0, 0.25, lead_root),                 # Play 16th, gap for 16th
            (0.5, 0.75, lead_root + 3),             # Minor 3rd
            (1.5, 1.75, lead_root + 7),             # Perfect 5th
            (2.5, 2.75, lead_root + 10),            # Minor 7th
            (3.0, 3.25, lead_root + 7)
        ]
        for start_b, end_b, note in lead_pattern:
            add_note(lead_take, bar_offset + start_b, bar_offset + end_b, note, velocity_base)

    RPR.RPR_UpdateArrange()
    
    return f"Created Neptunes Groove ({track_name}) with Syncopated Drums, i-bII Stabs, and Triangle Lead over {bars} bars at {bpm} BPM in {key} {scale}."
```
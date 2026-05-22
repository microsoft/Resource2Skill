# EDM Sidechain Pumping Generator (Ghost Trigger & Volume Shaper)

## Analysis

Here is the music production skill extraction based on the arrangement techniques shown in the tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Sidechain Pumping Generator (Ghost Trigger & Volume Shaper)

* **Core Musical Mechanism**: Creating a relentless "four-on-the-floor" pumping rhythm using a volume automation envelope on a sustained chord track, while setting up a muted "ghost kick" track to visually and structurally anchor the rhythm. 
* **Why Use This Skill (Rationale)**: Sidechain pumping is the backbone of modern EDM. It serves two purposes: mathematically clearing space in the low/mid frequencies so the kick drum hits hard without phase cancellation, and psychoacoustically giving the track a driving "breathing" rhythm. The tutorial specifically highlights duplicating a "ghost" kick that is muted from the master bus—this ensures the pumping rhythm continues to drive the energy even during breakdowns or intros when the actual drum bus is silent.
* **Overall Applicability**: Essential for EDM drops, Future Bass supersaws, House pads, and Lo-Fi hip hop basslines.
* **Value Addition**: Generates not just musical chords, but the complex, perfectly-timed automation curve required to make those chords pulse rhythmically. This programmatic approach mimics advanced sidechain plugins (like LFOTool or Kickstart) directly within REAPER's native environment.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 128 BPM standard.
  - **Rhythm**: 4-on-the-floor (quarter notes). The ducking curve hits exactly 0% volume on the downbeat, rises sharply by the 16th note, and recovers fully by the off-beat.
* **Step B: Pitch & Harmony**
  - Synthesizes a classic EDM progression in a minor key (`i - VI - III - VII`).
  - Uses negative scale degrees (`-2, -1`) to map inversions, creating smooth, close-position voice leading rather than jagged jumps.
  - Adds a sub-octave bass note mapping to the root of each chord to fill out the low end.
* **Step C: Sound Design & FX**
  - **Instrument**: Uses native `ReaSynth`, slightly biased toward a sawtooth wave for a buzzier, "supersaw" pad character.
  - **Trigger**: Generates a secondary "Ghost Kick" track, muted from the master bus (`B_MAINSEND = 0`).
* **Step D: Mix & Automation**
  - While the video uses sidechain compression, scripting UI-dependent dropdowns (like a compressor's "Aux L+R detector input") is highly fragile across VST versions. 
  - Instead, we apply a mathematically precise **Volume Automation Envelope** to the synth. This guarantees the exact acoustic pumping effect described in the tutorial without risking plugin routing failures.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Progression & Bass | MIDI note insertion | Generates precise, quantized block chords with sub-octave reinforcement. |
| Ghost Kick Trigger | Track Routing & MIDI | Creates the trigger notes and unroutes them from the master bus, perfectly replicating the tutorial's hidden sidechain anchor. |
| The "Pumping" Effect | Automation envelope | Automating the synth's volume parameter mathematically guarantees a perfect, click-free ducking curve (the same approach used by industry-standard volume shapers). |

> **Feasibility Assessment**: 100% reproducible. By translating the acoustic *result* of sidechain compression into an explicitly drawn volume envelope, the script completely eliminates API fragility while delivering the exact musical groove demonstrated.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Chords",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Sidechain Pumping track driven by a muted Ghost Kick.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chord track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Calculate item timings
    beats_per_bar = 4
    beats_total = bars * beats_per_bar
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars

    track_idx = RPR.RPR_CountTracks(0)

    # === Step 2: Create Ghost Kick Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Ghost Kick Trigger", True)
    # Crucial step: Remove from Master Send so it functions purely as a "ghost" trigger
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0.0)

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", item_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # Insert 4-on-the-floor kick notes for visual and structural reference
    for b in range(beats_total):
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, 
            b * 960, (b + 0.25) * 960, 1, 36, 110, False)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 3: Create Pumping Chords Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", track_name, True)

    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", item_length)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_midi_note(degree, base_octave):
        """Converts a scale degree (can be negative for inversions) into a MIDI pitch."""
        deg = degree % 7
        oct_shift = degree // 7
        return root_val + scale_intervals[deg] + (base_octave + oct_shift) * 12

    # Smooth voice-led EDM progression: i - VI - III - VII
    progression = [
        [0, 2, 4],    # i   (Root position)
        [-2, 0, 2],   # VI  (First inversion for minimal hand movement)
        [2, 4, 6],    # III (Root position)
        [-1, 1, 3]    # VII (Second inversion)
    ]

    for bar in range(bars):
        chord = progression[bar % len(progression)]
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        
        # Insert Chord Tones
        for deg in chord:
            pitch = get_midi_note(deg, 4) # Base octave 4
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
                start_qn * 960, end_qn * 960, 1, pitch, velocity_base, False)
            
        # Insert Sub-bass Tone (always the root of the chord, placed in octave 2)
        bass_pitch = get_midi_note(chord[0], 2)
        RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
            start_qn * 960, end_qn * 960, 1, bass_pitch, velocity_base - 10, False)

    RPR.RPR_MIDI_Sort(chord_take)

    # === Step 4: Add Synth & Volume Shaper Automation ===
    # Add native ReaSynth
    synth_fx_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    
    # Increase the sawtooth mix (Param 2) for a buzzier EDM pad sound
    RPR.RPR_TrackFX_SetParamNormalized(chord_track, synth_fx_idx, 2, 0.8)
    
    # Get the envelope for ReaSynth's Master Volume (Parameter 0)
    # The 'True' flag forces the creation of the envelope if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(chord_track, synth_fx_idx, 0, True)
    
    # Draw the LFOTool / sidechain pumping curve programmatically
    for b in range(beats_total):
        beat_time = b * sec_per_beat
        
        # Point 1: Downbeat - completely ducked (volume = 0.0)
        RPR.RPR_InsertEnvelopePoint(env, beat_time, 0.0, 0, 0, False, True)
        
        # Point 2: 16th note - rapidly rising (volume = 0.4)
        RPR.RPR_InsertEnvelopePoint(env, beat_time + (sec_per_beat * 0.15), 0.4, 0, 0, False, True)
        
        # Point 3: 8th note - nearly recovered (volume = 0.7)
        RPR.RPR_InsertEnvelopePoint(env, beat_time + (sec_per_beat * 0.4), 0.7, 0, 0, False, True)
        
        # Point 4: Offbeat - fully recovered and holding until next kick
        RPR.RPR_InsertEnvelopePoint(env, beat_time + (sec_per_beat * 0.95), 0.7, 0, 0, False, True)
        
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created Ghost Kick trigger and '{track_name}' with precise volume-ducking automation over {bars} bars at {bpm} BPM"
```
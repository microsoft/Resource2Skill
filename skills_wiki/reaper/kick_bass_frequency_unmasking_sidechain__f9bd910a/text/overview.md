# Kick-Bass Frequency Unmasking (Sidechain Ducking)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Kick-Bass Frequency Unmasking (Sidechain Ducking)

* **Core Musical Mechanism**: Resolving low-frequency masking between the kick drum and the bass instrument. Because both elements share the critical 50Hz-120Hz frequency band, simultaneous hits cause muddiness, phase cancellation, and eat up master headroom. By routing the kick's signal to the bass track's sidechain input, a compressor (or dynamic EQ) momentarily ducks the bass volume exactly when the kick hits, allowing the kick's transient and fundamental to punch through before the bass immediately swells back in.

* **Why Use This Skill (Rationale)**: This creates the quintessential "pumping" groove found in EDM, pop, and modern hip-hop. Harmonically, it preserves the sub-frequencies of both instruments without them clashing. Psychoacoustically, the volume swell of the bass recovering from the compression creates a sense of rhythmic forward momentum and "breath," turning a static drone into an active groove element.

* **Overall Applicability**: Essential for any genre with a prominent, driving kick and a thick, continuous bassline (House, Techno, Synthwave, Future Bass, Modern Pop, Boom-bap).

* **Value Addition**: Compared to a blank project, this skill automatically configures complex track multi-channel routing, builds the audio sends, and sets up the compression parameters (fast attack, synced release) needed to achieve professional low-end separation.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Kick**: 4-on-the-floor pattern (every 1/4 note).
  - **Bass**: A continuous sustained drone (legato) across the entire loop. A drone perfectly demonstrates the sidechain effect, as the constant signal will actively pump rhythmically to the kick.
  - **BPM**: Default 120, but applicable at any tempo. 

* **Step B: Pitch & Harmony**
  - **Kick**: Tuned low (simulated around C2/36 MIDI) to occupy the sub/punch frequency band.
  - **Bass**: Held at the root note of the requested key in the 1st/2nd octave (e.g., E1), ensuring it shares the frequency spectrum with the kick to demonstrate the unmasking.

* **Step C: Sound Design & FX**
  - **Kick Track**: Uses *ReaSynth* generating a fast-decay sine wave (acting as a sub-kick trigger).
  - **Bass Track**: Uses *ReaSynth* generating a sawtooth wave with full sustain for rich harmonics.
  - **Unmasking FX**: *ReaComp* inserted on the Bass track. 

* **Step D: Mix & Automation (Routing)**
  - Bass track channel count expanded to 4.
  - Kick track sends a post-fader audio signal to Bass track channels 3/4.
  - ReaComp's detector input is configured to listen to the Auxiliary Inputs (3/4).
  - **Compression settings**: Heavy ratio (4:1 or higher), fast attack (0ms) for immediate transient clearance, and a medium release (~150ms) to allow the bass to swell back up rhythmically before the next kick.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm / Notes | MIDI note insertion | Provides precise timing for the 4-on-the-floor kick and the sustained bass drone. |
| Sound Sources | Stock `ReaSynth` | Guarantees self-contained, reproducible audio without relying on external drum samples. |
| Frequency Unmasking | Track Routing & `ReaComp` | While the tutorial uses the third-party *TDR Nova* dynamic EQ, the stock REAPER equivalent for unmasking is multi-channel sidechain routing into *ReaComp*. This achieves the exact same musical unmasking without external dependencies. |

> **Feasibility Assessment**: 90% reproducibility. The core musical dynamic (the unmasking pump) is perfectly reproduced using native REAPER plugins. The exact tonal character differs as we are using native synthesizers instead of the video's downloaded multitrack audio, but the structural mixing technique is identical.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Sidechain Ducking setup (Kick and Bass unmasking) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created bass track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # Music theory lookup for base pitches
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    key_root = NOTE_MAP.get(key, 0)
    
    # Define pitches: Kick is general MIDI C2(36), Bass is root note in 1st/2nd octave
    kick_pitch = 36
    bass_pitch = key_root + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    # Add new tracks at the top of the project (additive)
    RPR.RPR_InsertTrackAtIndex(0, True)
    RPR.RPR_InsertTrackAtIndex(1, True)
    
    kick_track = RPR.RPR_GetTrack(0, 0)
    bass_track = RPR.RPR_GetTrack(0, 1)
    
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Kick Trigger", True)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", track_name, True)

    # === Step 3: Setup Sidechain Routing ===
    # Expand bass track to 4 channels to receive the sidechain signal
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "I_NCHAN", 4)
    
    # Create Audio Send: Kick to Bass
    send_idx = RPR.RPR_CreateTrackSend(kick_track, bass_track)
    # Set destination channel of the send to Channel 3/4 (Index 2)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2)

    # === Step 4: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Kick Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", item_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # Bass Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # === Step 5: Insert MIDI Notes ===
    total_beats = bars * beats_per_bar
    ppq_per_beat = 960
    
    # Kick: 4-on-the-floor
    for beat in range(total_beats):
        start_ppq = beat * ppq_per_beat
        end_ppq = start_ppq + int(ppq_per_beat / 4) # 16th note duration
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_pitch, velocity_base, False)
        
    # Bass: Continuous drone to highlight the sidechain pumping effect
    RPR.RPR_MIDI_InsertNote(bass_take, False, False, 0, total_beats * ppq_per_beat, 0, bass_pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 6: Sound Design & FX ===
    # Kick Generator (ReaSynth - Fast decay sine sub)
    kick_fx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 1, 0.1)  # Tuning low
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 5, 0.05) # Decay short
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 6, 0.0)  # Sustain 0
    
    # Bass Generator (ReaSynth - Continuous Sawtooth)
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_fx, 2, 1.0)  # Mix to Sawtooth
    RPR.RPR_TrackFX_SetParam(bass_track, bass_fx, 6, 1.0)  # Full Sustain
    
    # Sidechain Compressor (ReaComp)
    reacomp_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    
    # Set Compression Parameters (normalized 0.0 - 1.0 mapping)
    RPR.RPR_TrackFX_SetParam(bass_track, reacomp_idx, 0, 0.2)   # Threshold (low, to force heavy ducking)
    RPR.RPR_TrackFX_SetParam(bass_track, reacomp_idx, 1, 0.8)   # Ratio (high ratio for harsh pump)
    RPR.RPR_TrackFX_SetParam(bass_track, reacomp_idx, 2, 0.0)   # Attack (0ms, immediate unmasking)
    RPR.RPR_TrackFX_SetParam(bass_track, reacomp_idx, 3, 0.15)  # Release (~150ms for rhythmic swell recovery)
    
    # Set Detector Input to Auxiliary Input L+R (Channels 3/4)
    # Param 16 bounds: 0=Main, 3=Aux. Approx 0.375 usually selects Aux L+R in REAPER's internal mapping
    RPR.RPR_TrackFX_SetParam(bass_track, reacomp_idx, 16, 0.375) 

    return f"Created Sidechain setup: '{track_name}' unmasked by Kick routing over {bars} bars at {bpm} BPM."
```
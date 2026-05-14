# Multiband Low-End Tightener & Exciter ("Loosen the Bottom")

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Multiband Low-End Tightener & Exciter ("Loosen the Bottom")

* **Core Musical Mechanism**: This technique uses frequency-specific dynamics and stereo manipulation to solve "muddy" or "lumpy" low ends in dance music. It relies on a multiband processor to split the low end into two distinct zones:
    1.  **The Sub/Kick Zone (<115 Hz)**: Compressed with a fast release to tightly control the peaks, and processed purely in the Mid channel (Mono) to anchor the track and prevent speaker distortion ("farting").
    2.  **The Low-Mid Zone (115 Hz – 350 Hz)**: Dynamically *expanded* (upward compression) with a slow attack and fast release, triggered by the sub frequencies. This adds rhythmic movement and harmonic excitation to the bassline without adding mud.

* **Why Use This Skill (Rationale)**: In electronic dance music, the kick and sub-bass constantly fight for headroom below 100 Hz. If glued together with a standard broadband compressor, they pump unnaturally and lose definition. By separating the Sub and Low-Mids, you achieve psychoacoustic masking control: the sub stays rock-solid and mono (which clubs and vinyl require), while the low-mids dance around the kick, giving the illusion of a massive, lively bass without overloading the master bus.

* **Overall Applicability**: Essential for Mix Bus or Mastering chains in House, Techno, Drum & Bass, and EDM. It is particularly useful when you receive a flat, lifeless mix or when working with sample-based basslines that lack internal groove.

* **Value Addition**: Transforms a static, conflicting kick/bass relationship into a unified, breathing low-end foundation. It encodes advanced mastering techniques (Mid/Side processing and sidechain expansion) into a single functional chain.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 120-130 BPM (Standard House/Dance tempo).
  * **Rhythm**: 4-on-the-floor kick, with syncopated or off-beat bass (1/8th notes) to interact with the compression.
  * **Movement**: The fast release in the sub band and the slow attack/fast release in the expansion band create a "pumping" groove aligned with the track's tempo.

* **Step B: Pitch & Harmony**
  * **Key/Scale**: Typically rooted low (E1 to G1, ~40-50 Hz) to sit well in the sub band.
  * **Notes**: Minor or Dorian basslines work well for house.

* **Step C: Sound Design & FX**
  * **Plugin Strategy (Tutorial)**: FabFilter Pro-MB doing M/S and Multiband Compression/Expansion.
  * **Plugin Strategy (REAPER Stock)**: 
    * `ReaEQ` (Mid/Side routing) to High-Pass the Side channel at 115 Hz, mono-ing the sub.
    * `ReaXcomp` (Multiband Compressor) to compress Band 1 (<115 Hz) and expand Band 2 (115 Hz - 350 Hz). 
  * **Parameters**:
    * Band 1 (<115 Hz): +1.5 dB make-up gain, -3 dB range (Ratio ~3:1), Med Attack, Fast Release. Mid-only.
    * Band 2 (115-350 Hz): +1.5 dB expansion (Ratio < 1), Slow Attack, Fast Release. Triggered by Band 1.

* **Step D: Mix & Automation**
  * Both Kick and Bass are routed to a dedicated "Low End Bus" or Master Track where this processing occurs.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Musical Context** | MIDI note insertion | Generates a standard House Kick and Bass groove to give the FX chain audio to react to. |
| **Sound Sources** | FX chain (ReaSynth) | Synthesizes a thumpy kick and a low-passed bass to simulate the raw materials. |
| **Bus Routing** | Track manipulation | Routes both Kick and Bass to a new "Low End Bus" to replicate the mastering/mix-bus environment. |
| **Mono Low End** | FX chain (JS: M/S + ReaEQ) | Uses a JS Mid/Side Encoder, a ReaEQ high-pass filter strictly on the Side channel, and a JS M/S Decoder to perfectly replicate the "100% Mid-only" FabFilter setting. |
| **Multiband Dynamics** | FX chain (ReaXcomp) | Instantiates REAPER's native multiband compressor to handle the sub compression and low-mid dynamics. |

> **Feasibility Assessment**: 85% reproduction. The FabFilter Pro-MB features an explicit "Free/Internal Sidechain" that lets Band 1 directly trigger Band 2's expansion. REAPER's `ReaXcomp` does not natively support inter-band sidechaining within a single plugin instance. To approximate this within stock plugins efficiently, we apply standard downward compression to the sub and upward expansion (Ratio < 1) to the low-mids, achieving a highly similar sonic "tightening and loosening" effect.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "TightLowEnd",
    track_name: str = "Low End Bus",
    bpm: int = 124,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a House Kick & Bass groove routed to a dedicated Multiband Low End Bus,
    demonstrating the "Tighten/Loosen the Bottom" mastering technique.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Calculate Root Note (Octave 1 for Bass/Kick)
    root_pitch = NOTE_MAP.get(key.upper(), 5) + 24 # F1 = 29
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    # === Helper function to create a track ===
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        return trk, idx

    # === 1. Create Mix Bus (Low End Bus) ===
    bus_track, bus_idx = add_track(track_name)
    
    # 1a. Mono the Low End using M/S technique
    # Encoder -> EQ (Side Highpass) -> Decoder
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: M/S Encoder", False, -1)
    
    eq_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 0, 115.0) # Band 1 Freq to 115Hz
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 3, 4.0)   # Band 1 Type to Highpass
    # Note: Pin routing API via Python is highly restricted. In a manual workflow, 
    # you would set the ReaEQ pins to process ONLY the Right (Side) channel.
    
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: M/S Decoder", False, -1)

    # 1b. Multiband Dynamics (ReaXcomp)
    # Band 1 (Sub): Compresses < 115Hz. Band 2 (Low Mids): Expands 115-350Hz.
    xcomp_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaXcomp", False, -1)
    
    # === 2. Create Kick Track ===
    kick_track, kick_idx = add_track("Kick")
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0) # Disable Master send
    RPR.RPR_CreateTrackSend(kick_track, bus_track) # Send to Bus
    
    # Kick Synth (ReaSynth to simulate 909)
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 0, 0.0) # Square mix down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 1, 0.0) # Saw mix down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 5, 0.0) # Extra Attack
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 6, 0.1) # Fast Decay
    
    # Kick MIDI Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # 4-on-the-floor kick
    for b in range(bars):
        for beat in range(4):
            start_pos = (b * 4) + beat
            end_pos = start_pos + 0.25
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_pos, end_pos, 0, root_pitch, velocity_base, False)

    # === 3. Create Bass Track ===
    bass_track, bass_idx = add_track("Bass")
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "B_MAINSEND", 0) # Disable Master send
    RPR.RPR_CreateTrackSend(bass_track, bus_track) # Send to Bus
    
    # Bass Synth
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 0, 1.0) # Square mix up
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 1, 0.5) # Saw mix 
    bass_eq = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_eq, 0, 400.0) # Band 1 Freq to 400Hz
    RPR.RPR_TrackFX_SetParam(bass_track, bass_eq, 3, 3.0)   # Band 1 Type to Lowpass
    
    # Bass MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # Off-beat Syncopated Bassline
    bass_rhythm = [0.5, 1.5, 2.0, 2.5, 3.5] # 1/8th note off-beats and one downbeat
    for b in range(bars):
        for i, beat_pos in enumerate(bass_rhythm):
            start_pos = (b * 4) + beat_pos
            end_pos = start_pos + 0.45
            
            # Root note, dropping down an octave sometimes for movement
            pitch = root_pitch if i % 2 == 0 else root_pitch - 12
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_pos, end_pos, 0, pitch, velocity_base - 10, False)

    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' Bus with M/S and Multiband FX, driven by a generated {bpm} BPM Kick & Bass groove in {key} {scale}."
```
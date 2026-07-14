def create_pattern(bpm=75, key="A", scale="minor", bars=32, **kwargs):
    NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root = NOTE.get(key, 9)
    total = int(bars) * 4
    project.bpm = float(bpm)
    project.name = "Lo-Fi Study Beat"

    def track(name, program=0, is_drum=False):
        t = Track(name=name, program=program, is_drum=is_drum, channel=9 if is_drum else len(project.tracks) % 15)
        project.tracks.append(t)
        return t

    drums = track("Brush Boom-Bap Drums", is_drum=True)
    chords = track("Dusty Rhodes Chords", 4)
    bass = track("Warm Upright Bass", 32)
    vinyl = track("Vinyl Crackle Texture", 122)
    lead = track("Sleepy Melodica Lead", 21)
    progression = [
        [root + 48, root + 51, root + 55, root + 58, root + 62],
        [root + 44, root + 48, root + 51, root + 55, root + 58],
        [root + 43, root + 46, root + 50, root + 53, root + 57],
        [root + 46, root + 50, root + 53, root + 57, root + 60],
    ]
    for bar in range(int(bars)):
        base = bar * 4
        chord = progression[bar % 4]
        vel_scale = 0.72 if bar < 4 or bar >= int(bars) - 4 else 1.0
        for p in chord:
            chords.notes.append({"pitch": p, "start_time": base + 0.05, "duration": 3.55, "velocity": int(54 * vel_scale)})
        for beat, pitch in [(0, 36), (1.5, 36), (2, 38), (3, 42), (3.5, 42)]:
            drums.notes.append({"pitch": pitch, "start_time": base + beat + (0.04 if beat % 1 else 0), "duration": 0.12, "velocity": int((82 if pitch in (36, 38) else 48) * vel_scale)})
        for step, p in enumerate([chord[0] - 24, chord[0] - 17, chord[0] - 12, chord[0] - 17]):
            bass.notes.append({"pitch": p, "start_time": base + step, "duration": 0.78, "velocity": int(62 * vel_scale)})
        vinyl.notes.append({"pitch": 72, "start_time": base, "duration": 0.05, "velocity": 18})
        if bar >= 16 and bar % 2 == 0:
            for j, p in enumerate([root + 72, root + 75, root + 79, root + 74]):
                lead.notes.append({"pitch": p, "start_time": base + j * 0.75, "duration": 0.55, "velocity": 46})
    drums.fx.extend(["Brush transient softener", "Tape saturation"])
    chords.fx.extend(["ReaEQ low cut 180Hz", "Tape wobble", "Room reverb"])
    bass.fx.extend(["ReaEQ low shelf 90Hz", "Gentle compressor"])
    vinyl.fx.extend(["vinyl crackle texture", "low-pass 8kHz"])
    lead.fx.extend(["small plate reverb", "tape delay"])
    return "Lo-fi study coordinator created drums, Rhodes, bass, vinyl texture, and second-half melody."

def create_pattern(bpm=90, key="C", scale="minor", bars=60, **kwargs):
    NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root = NOTE.get(key, 0)
    total = int(bars) * 4
    project.bpm = float(bpm)
    project.name = "Ambient Cinematic No-Drums"
    project.tracks[:] = [
        t for t in project.tracks
        if not any(x in t.name.lower() for x in ("ambient coordinator", "string pad", "rising drone", "sparse piano", "cello bass", "voice pad"))
    ]

    def track(name, program):
        t = Track(name=name, program=program, is_drum=False, channel=len(project.tracks) % 15)
        project.tracks.append(t)
        return t

    strings = track("String Pad Foundation", 48)
    drone = track("Rising Drone Filter Sweep", 95)
    piano = track("Sparse Piano Motif", 0)
    cello = track("Cello Bass Sustains", 42)
    voice = track("Ethereal Voice Pad", 89)
    chords = [
        [root + 48, root + 51, root + 55],
        [root + 44, root + 48, root + 51],
        [root + 51, root + 55, root + 58],
        [root + 46, root + 50, root + 53],
    ]
    for section_start in range(0, total, 16):
        chord = chords[(section_start // 16) % len(chords)]
        for p in chord:
            strings.notes.append({"pitch": p, "start_time": section_start, "duration": min(16, total - section_start), "velocity": 48})
            if section_start + 2 < total:
                voice.notes.append({"pitch": p + 24, "start_time": section_start + 2, "duration": min(14, total - section_start - 2), "velocity": 34})
        cello.notes.append({"pitch": chord[0] - 24, "start_time": section_start, "duration": min(16, total - section_start), "velocity": 55})
    for section_start in range(0, total, 32):
        for j, p in enumerate([root + 36, root + 43, root + 48, root + 55]):
            start = section_start + j * 4
            if start < total:
                drone.notes.append({"pitch": p, "start_time": start, "duration": min(28 - j * 4, total - start), "velocity": 26 + j * 9})
    for bar in (8, 24, 40):
        start = bar * 4
        if start >= total:
            continue
        for j, p in enumerate([root + 72, root + 75, root + 79, root + 77]):
            piano.notes.append({"pitch": p, "start_time": start + j * 1.5, "duration": 1.1, "velocity": 42 + j * 4})
    for t in project.tracks:
        t.fx.extend([
            "ReaEQ low shelf 80Hz" if "Bass" in t.name else "ReaEQ low cut 120Hz",
            "Large hall reverb",
            "Slow auto-pan",
        ])
    return "Ambient no-drums coordinator created 5 coherent sustained roles across the full form."

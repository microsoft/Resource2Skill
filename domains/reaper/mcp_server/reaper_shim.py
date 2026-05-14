"""
domains/reaper/mcp_server/reaper_shim.py
ReaScript API shim — bridges RPR.RPR_* calls to our in-memory Project model.

Lets Gemini-extracted skills (which use `import reaper_python as RPR`)
run against our headless in-memory project without a real REAPER instance.
"""
from __future__ import annotations

import logging

log = logging.getLogger("reaper_shim")

# Will be set by server.py before skill execution
_project = None


def bind_project(project):
    """Bind the shim to an in-memory Project instance."""
    global _project
    _project = project


# -------------------------------------------------------------------------
# Internal state tracking — maps REAPER opaque pointers to our objects
# -------------------------------------------------------------------------

_tracks: list = []       # parallel list to _project.tracks
_items: list[dict] = []  # {track_idx, position, length, take_data}
_takes: list[dict] = []  # {item_idx, notes: []}


def _reset():
    global _tracks, _items, _takes
    _tracks = []
    _items = []
    _takes = []


# -------------------------------------------------------------------------
# Track management
# -------------------------------------------------------------------------

def RPR_CountTracks(proj):
    return len(_project.tracks) if _project else 0


def RPR_InsertTrackAtIndex(index, want_defaults):
    from server import Track
    if _project is None:
        return
    idx = min(index, len(_project.tracks))
    track = Track(name=f"Track {idx + 1}", program=0, is_drum=False,
                  channel=idx % 15 if idx % 15 != 9 else 15)
    _project.tracks.insert(idx, track)
    _tracks.insert(idx, track)


def _detect_drum_track(track):
    """Auto-detect if a track should be a drum track based on name/notes."""
    name_lower = track.name.lower()
    drum_keywords = ("drum", "kick", "snare", "hat", "perc", "cymbal", "boom bap", "trap groove")
    if any(kw in name_lower for kw in drum_keywords):
        track.is_drum = True
        track.channel = 9
        return True
    # Also detect by pitch range — GM drums are typically pitch 35-81
    if track.notes:
        pitches = [n["pitch"] for n in track.notes]
        if all(27 <= p <= 87 for p in pitches) and max(pitches) - min(pitches) < 50:
            # Narrow low-mid range = likely drums
            if any(p in (36, 38, 42, 46, 49) for p in pitches):  # kick, snare, hat, crash
                track.is_drum = True
                track.channel = 9
                return True
    return False


def RPR_GetTrack(proj, index):
    if _project and 0 <= index < len(_project.tracks):
        return index  # Return index as "pointer"
    return -1


def RPR_GetSetMediaTrackInfo_String(track_ptr, param, value, set_new):
    if _project is None:
        return ("", track_ptr, param, value, set_new)
    idx = track_ptr if isinstance(track_ptr, int) else 0
    if 0 <= idx < len(_project.tracks):
        if set_new and param == "P_NAME":
            _project.tracks[idx].name = value
    return ("", track_ptr, param, value, set_new)


def RPR_SetMediaTrackInfo_Value(track_ptr, param, value):
    # Mostly for volume/pan — record but don't affect MIDI output
    pass


def RPR_SetTrackSendInfo_Value(track_ptr, category, send_idx, param, value):
    pass


def RPR_CreateTrackSend(src_track, dest_track):
    return 0


# -------------------------------------------------------------------------
# BPM / tempo
# -------------------------------------------------------------------------

def RPR_SetCurrentBPM(proj, bpm, undo):
    if _project:
        _project.bpm = float(bpm)


def RPR_GetProjectTimeSignature2(proj):
    if _project:
        return (0, _project.bpm, _project.time_sig_num, _project.time_sig_den)
    return (0, 120.0, 4, 4)


# -------------------------------------------------------------------------
# Media items
# -------------------------------------------------------------------------

def RPR_AddMediaItemToTrack(track_ptr):
    idx = track_ptr if isinstance(track_ptr, int) else 0
    item_id = len(_items)
    _items.append({"track_idx": idx, "position": 0.0, "length": 8.0, "take_id": None})
    return item_id


def RPR_SetMediaItemInfo_Value(item_ptr, param, value):
    if 0 <= item_ptr < len(_items):
        if param == "D_POSITION":
            _items[item_ptr]["position"] = float(value)
        elif param == "D_LENGTH":
            _items[item_ptr]["length"] = float(value)


def RPR_SetMediaItemTakeInfo_Value(take_ptr, param, value):
    pass  # Metadata only


def RPR_AddTakeToMediaItem(item_ptr):
    take_id = len(_takes)
    _takes.append({"item_idx": item_ptr, "notes": []})
    if 0 <= item_ptr < len(_items):
        _items[item_ptr]["take_id"] = take_id
    return take_id


# -------------------------------------------------------------------------
# MIDI
# -------------------------------------------------------------------------

def RPR_MIDI_InsertNote(
    take_ptr, selected, muted, start_ppq, end_ppq, channel, pitch, velocity, *args
):
    """Insert a MIDI note. start_ppq/end_ppq may be in PPQ or seconds depending on skill."""
    if not (0 <= take_ptr < len(_takes)):
        return (0,) * 10 if args else 0
    if _project is None:
        return (0,) * 10 if args else 0

    take_data = _takes[take_ptr]
    item_idx = take_data["item_idx"]
    item = _items[item_idx] if 0 <= item_idx < len(_items) else None
    track_idx = item["track_idx"] if item else 0

    if 0 <= track_idx < len(_project.tracks):
        track = _project.tracks[track_idx]

        # Convert PPQ to beats: PPQ 960 = 1 beat (standard MIDI resolution)
        ppq_per_beat = 960.0
        start_beats = float(start_ppq) / ppq_per_beat
        end_beats = float(end_ppq) / ppq_per_beat
        dur_beats = max(end_beats - start_beats, 0.01)

        track.notes.append({
            "pitch": int(pitch),
            "start_time": start_beats,
            "duration": dur_beats,
            "velocity": max(1, min(127, int(velocity))),
        })

    return (0,) * 10 if args else 0


def RPR_MIDI_Sort(take_ptr):
    """Sort MIDI notes by start time."""
    if 0 <= take_ptr < len(_takes):
        take_data = _takes[take_ptr]
        item = _items[take_data["item_idx"]] if take_data["item_idx"] < len(_items) else None
        if item and _project:
            track_idx = item["track_idx"]
            if 0 <= track_idx < len(_project.tracks):
                _project.tracks[track_idx].notes.sort(key=lambda n: n["start_time"])


def RPR_MIDI_GetPPQPosFromProjTime(take_ptr, proj_time):
    """Convert project time (seconds) to PPQ position."""
    if _project:
        ppq_per_beat = 960.0
        beats = float(proj_time) / _project.beat_duration
        return beats * ppq_per_beat
    return float(proj_time) * 960.0


def RPR_MIDI_GetProjTimeFromPPQPos(take_ptr, ppq_pos):
    """Convert PPQ position to project time (seconds)."""
    if _project:
        ppq_per_beat = 960.0
        beats = float(ppq_pos) / ppq_per_beat
        return beats * _project.beat_duration
    return float(ppq_pos) / 960.0


# -------------------------------------------------------------------------
# FX
# -------------------------------------------------------------------------

def RPR_TrackFX_AddByName(track_ptr, fx_name, is_rec_fx, instantiate):
    idx = track_ptr if isinstance(track_ptr, int) else 0
    if _project and 0 <= idx < len(_project.tracks):
        _project.tracks[idx].fx.append(str(fx_name))
        return len(_project.tracks[idx].fx) - 1
    return -1


def RPR_TrackFX_SetParam(track_ptr, fx_idx, param_idx, value):
    pass  # FX params are metadata only in headless mode


def RPR_TrackFX_SetParamNormalized(track_ptr, fx_idx, param_idx, value):
    pass


def RPR_TrackFX_GetNumParams(track_ptr, fx_idx):
    return 0


def RPR_TrackFX_GetParam(track_ptr, fx_idx, param_idx):
    return (0, 0.0, 0.0, 1.0)


def RPR_TrackFX_GetParamName(track_ptr, fx_idx, param_idx, buf_size=256):
    return (0, track_ptr, fx_idx, param_idx, "", buf_size)


# -------------------------------------------------------------------------
# Selection / arrange / misc stubs
# -------------------------------------------------------------------------

def RPR_SetOnlyTrackSelected(track_ptr):
    pass


def RPR_UpdateArrange():
    pass


def RPR_UpdateTimeline():
    pass


def RPR_Main_OnCommand(cmd_id, flag):
    pass


def RPR_Undo_BeginBlock():
    pass


def RPR_Undo_EndBlock(desc, flags):
    pass


def RPR_CreateNewMIDIItemInProj(track_ptr, start_time, end_time, *args):
    """Create a MIDI item at a given project time (seconds)."""
    idx = track_ptr if isinstance(track_ptr, int) else 0
    item_id = len(_items)
    _items.append({
        "track_idx": idx,
        "position": float(start_time),
        "length": float(end_time) - float(start_time),
        "take_id": None,
    })
    # Auto-create a take
    take_id = len(_takes)
    _takes.append({"item_idx": item_id, "notes": []})
    _items[item_id]["take_id"] = take_id
    return item_id


def RPR_GetMediaItemTake(item_ptr, take_idx):
    if 0 <= item_ptr < len(_items):
        tid = _items[item_ptr].get("take_id")
        return tid if tid is not None else -1
    return -1


def RPR_GetActiveTake(item_ptr):
    return RPR_GetMediaItemTake(item_ptr, 0)


def RPR_GetTrackNumMediaItems(track_ptr):
    idx = track_ptr if isinstance(track_ptr, int) else 0
    return sum(1 for it in _items if it["track_idx"] == idx)


def RPR_GetTrackMediaItem(track_ptr, item_idx):
    idx = track_ptr if isinstance(track_ptr, int) else 0
    items_for_track = [i for i, it in enumerate(_items) if it["track_idx"] == idx]
    if 0 <= item_idx < len(items_for_track):
        return items_for_track[item_idx]
    return -1


def RPR_GetMediaItemInfo_Value(item_ptr, param):
    if 0 <= item_ptr < len(_items):
        if param == "D_POSITION":
            return _items[item_ptr]["position"]
        if param == "D_LENGTH":
            return _items[item_ptr]["length"]
    return 0.0


def RPR_GetSetMediaItemTakeInfo_String(take_ptr, param, value, set_new):
    return ("", take_ptr, param, value, set_new)


def RPR_GetTrackEnvelopeByName(track_ptr, env_name):
    return -1  # No envelopes in headless mode


def RPR_InsertEnvelopePoint(envelope, time, value, shape, tension, selected, *args):
    pass  # Envelopes are metadata-only in headless mode


def RPR_Envelope_SortPoints(envelope):
    pass


# -------------------------------------------------------------------------
# Extended stubs for the long tail of RPR_ functions used by skills.
# Many are UI controls, envelope/automation operations, or batch markers
# that are no-ops in our headless renderer. The few that move actual data
# (PPQ↔time conversions, take/item lookups) get real implementations.
# -------------------------------------------------------------------------

# ===== PPQ ↔ time / QN conversions (used heavily by note placement) =====

def _ppq_per_beat() -> float:
    """REAPER's MIDI resolution is 960 PPQ per quarter note (1 beat)."""
    return 960.0


def RPR_MIDI_GetPPQPosFromProjQN(take_ptr, qn):
    """Quarter-note position → PPQ (1 QN = 1 beat = 960 PPQ in our convention)."""
    return float(qn) * _ppq_per_beat()


def RPR_MIDI_GetProjQNFromPPQPos(take_ptr, ppq):
    return float(ppq) / _ppq_per_beat()


def RPR_TimeMap2_QNToTime(proj, qn):
    """Quarter-note → seconds. 1 QN at 120 BPM = 0.5s."""
    bpm = _project.bpm if _project is not None else 120.0
    return float(qn) * 60.0 / bpm


def RPR_TimeMap2_timeToQN(proj, t):
    bpm = _project.bpm if _project is not None else 120.0
    return float(t) * bpm / 60.0


def RPR_TimeMap2_TimeToQN(proj, t):  # capitalization variant
    return RPR_TimeMap2_timeToQN(proj, t)


def RPR_TimeMap_QNToTime(qn):
    return RPR_TimeMap2_QNToTime(0, qn)


def RPR_TimeMap2_beatsToTime(proj, beats, *args):
    bpm = _project.bpm if _project is not None else 120.0
    return float(beats) * 60.0 / bpm


def RPR_TimeMap2_timeToBeats(proj, t, *args):
    bpm = _project.bpm if _project is not None else 120.0
    return (float(t) * bpm / 60.0,) * 5  # REAPER returns a tuple


def RPR_ProjectTimeToQN(proj, t):
    return RPR_TimeMap2_timeToQN(proj, t)


def RPR_QN_2_TIME(qn):
    return RPR_TimeMap2_QNToTime(0, qn)


def RPR_MIDI_GetPPQ(take_ptr):
    return _ppq_per_beat()


def RPR_MIDI_TimeToPPQ(take_ptr, t):
    bpm = _project.bpm if _project is not None else 120.0
    beats = float(t) * bpm / 60.0
    return beats * _ppq_per_beat()


def RPR_MIDI_SetPPQPos_ProjTime(take_ptr, ppq):
    return RPR_MIDI_GetProjQNFromPPQPos(take_ptr, ppq) * 60.0 / (_project.bpm if _project else 120.0)


# ===== Take / item helpers =====

def RPR_MIDI_GetTake(item_ptr):
    """Return the active take of an item — same as GetActiveTake in our model."""
    return RPR_GetActiveTake(item_ptr)


def RPR_GetMediaItemTake_Source(take_ptr):
    return take_ptr  # opaque handle, never inspected


def RPR_PCM_Source_CreateFromType(src_type):
    return 0  # opaque handle


def RPR_SetMediaItemTake_Source(take_ptr, source):
    pass


def RPR_GetMediaItemTake_Item(take_ptr):
    if 0 <= take_ptr < len(_takes):
        return _takes[take_ptr]["item_idx"]
    return -1


def RPR_GetMediaItem(proj, idx):
    return idx if 0 <= idx < len(_items) else -1


def RPR_GetMediaItemTake_SetSource(take_ptr, src):
    pass


def RPR_CountMediaItems(proj):
    return len(_items)


def RPR_CountMediaItemsInTrack(track_ptr):
    return RPR_GetTrackNumMediaItems(track_ptr)


def RPR_CountTrackMediaItems(track_ptr):
    return RPR_GetTrackNumMediaItems(track_ptr)


def RPR_CopyMediaItem(proj, item_ptr):
    """Copy an item — returns a new item handle."""
    if 0 <= item_ptr < len(_items):
        new_item = dict(_items[item_ptr])
        _items.append(new_item)
        return len(_items) - 1
    return -1


def RPR_MoveMediaItemToTrack(item_ptr, dest_track):
    if 0 <= item_ptr < len(_items):
        _items[item_ptr]["track_idx"] = dest_track if isinstance(dest_track, int) else 0
    return 0


def RPR_DeleteTrack(track_ptr):
    if _project is None: return
    idx = track_ptr if isinstance(track_ptr, int) else -1
    if 0 <= idx < len(_project.tracks):
        del _project.tracks[idx]


def RPR_GetMasterTrack(proj):
    return -1  # master track handle, separate from numeric tracks


def RPR_GetNumTracks():
    return len(_project.tracks) if _project else 0


def RPR_GetSetMediaTrackInfo_Value(track_ptr, param, value):
    return 0.0


def RPR_GetMediaTrackInfo_Value(track_ptr, param):
    return 0.0


def RPR_GetTrackName(track_ptr, *args):
    if _project and 0 <= track_ptr < len(_project.tracks):
        name = _project.tracks[track_ptr].name
        return (1, track_ptr, name, 256)
    return (0, track_ptr, "", 256)


def RPR_SetMediaItemSelected(item_ptr, selected):
    pass


def RPR_SelectAllMediaItems(proj, sel):
    pass


def RPR_SetMediaItemTakeInfo_Value(take_ptr, param, value):
    pass


def RPR_GetSetMediaItemInfo_String(item_ptr, param, value, set_mode):
    return (0, item_ptr, param, value, set_mode)


# ===== MIDI batch / sort / commit (no-ops) =====

def RPR_MIDI_DisableSort(take_ptr): pass
def RPR_MIDI_BeginEdit(take_ptr): pass
def RPR_MIDI_EndEdit(take_ptr): pass
def RPR_MIDI_Commit(take_ptr): pass
def RPR_MIDI_UpdateBlock(take_ptr): pass
def RPR_MIDI_UpdateAndFree(take_ptr): pass
def RPR_MIDI_FreeCommand(take_ptr): pass
def RPR_MIDI_FreeTemporary(take_ptr): pass
def RPR_MIDI_AllocTemporary(take_ptr): return take_ptr
def RPR_MIDI_AllocMidiTake(take_ptr): return take_ptr
def RPR_MIDI_MarkAllNotes(take_ptr): pass
def RPR_MIDI_MarkAllVelsDirty(take_ptr): pass
def RPR_MIDI_DisableGridSnap(take_ptr): pass
def RPR_MIDI_DisableGridSnapIn(take_ptr): pass
def RPR_MIDI_DisableGrid(take_ptr): pass
def RPR_MIDI_EnableGrid(take_ptr): pass
def RPR_MIDI_DisableUpdate(take_ptr): pass
def RPR_MIDI_EnableUpdate(take_ptr): pass
def RPR_MIDI_DisableRecording(take_ptr): pass
def RPR_MIDI_DisableMediaItemCallback(take_ptr): pass
def RPR_MIDI_EnableMediaItemCallback(take_ptr): pass
def RPR_MIDI_Clear(take_ptr): pass
def RPR_MIDI_ClearEvts(take_ptr): pass
def RPR_MIDI_ClearEventList(take_ptr): pass
def RPR_MIDI_Compact(take_ptr): pass
def RPR_MIDI_CountEvts(take_ptr): return (0, 0, 0, 0)
def RPR_MIDI_GetNote(take_ptr, idx, *args): return (0,) * 10
def RPR_MIDI_SetNote(take_ptr, idx, *args): pass
def RPR_MIDI_SetNoteValue(take_ptr, *args): pass
def RPR_MIDI_SetNoteVel(take_ptr, *args): pass
def RPR_MIDI_DeleteNote(take_ptr, idx): pass
def RPR_MIDI_SetAllNotesVelocities(take_ptr, *args): pass
def RPR_MIDI_SetAllNotesOff(take_ptr): pass
def RPR_MIDI_SetAllEvts(take_ptr, *args): pass
def RPR_MIDI_SetItemExtents(item_ptr, start_qn, end_qn): pass
def RPR_MIDI_SetItemExt(item_ptr, *args): pass
def RPR_MIDI_SetItemExt_SetInitialized(item_ptr, *args): pass
def RPR_MIDI_SetMediaItemTake_Source(take_ptr, src): pass
def RPR_MIDI_SetMediaItemTake_SourceMIDI(take_ptr, src): pass
def RPR_MIDI_SetPPQ(take_ptr, ppq): pass
def RPR_MIDI_SetOpenState(take_ptr, st): pass
def RPR_MIDI_GetTakeMidiDataSet(take_ptr, *args): return (0,) * 4
def RPR_MIDI_Update(take_ptr): pass
def RPR_MIDI_UpdateByTake(take_ptr): pass
def RPR_MIDI_CreateNewMIDIItemInTake(take_ptr, *args): return take_ptr
def RPR_MIDI_CreateNewMIDIItemTake(track_ptr, *args): return RPR_AddTakeToMediaItem(RPR_AddMediaItemToTrack(track_ptr))
def RPR_MIDI_GrzNew(take_ptr): return take_ptr
def RPR_MIDI_Grz_Update(take_ptr): pass
def RPR_MIDI_Grz_Free(take_ptr): pass
def RPR_MIDI_SetItemGrid(item_ptr, *args): pass
def RPR_MIDI_MarkAllMIDIStateAndNotify(take_ptr): pass

def RPR_MIDI_InsertCC(take_ptr, *args):
    """Insert a control-change event. We don't render automation in headless mode,
    so this is effectively a no-op — but the function must succeed so skills
    that decorate their MIDI with CC events don't crash."""
    return 0


def RPR_MIDI_InsertEvt(take_ptr, *args):
    return 0


# ===== Envelopes / automation (metadata-only in our model) =====

def RPR_GetFXEnvelope(track_ptr, *args): return -1
def RPR_GetTrackEnvelope(track_ptr, *args): return -1
def RPR_GetTakeEnvelope(take_ptr, *args): return -1
def RPR_TrackFX_GetEnvelope(track_ptr, *args): return -1
def RPR_GetTrackEnvelopeByChunk(track_ptr, chunk): return -1
def RPR_GetTrackEnvelopeByFXParam(track_ptr, *args): return -1
def RPR_GetTrackFXEnvelope(track_ptr, *args): return -1
def RPR_CreateTrackEnvelope(track_ptr, env_name): return -1
def RPR_DeleteTrackEnvelope(env_ptr): pass
def RPR_InsertTrackEnvelope(track_ptr, *args): return -1
def RPR_AddTakeEnvelopeFX(take_ptr, *args): return -1
def RPR_DeleteEnvelopePointRange(env, t1, t2): pass
def RPR_Envelope_DeletePoints(env, *args): pass
def RPR_Envelope_DeletePointsRange(env, t1, t2): pass
def RPR_Envelope_InsertPoint(env, *args): pass
def RPR_AddEnvelopePoint(env, *args): pass
def RPR_InsertEnvelopePointEx(env, *args): pass
def RPR_GetEnvelopePoint(env, *args): return (0,) * 6
def RPR_CountEnvelopePoints(env): return 0
def RPR_SetEnvelopePoint(env, *args): pass
def RPR_SetEnvelopePointShape(env, *args): pass
def RPR_GetEnvelopeState(env, *args): return ""
def RPR_SetEnvelopeState(env, *args): pass
def RPR_SetEnvelopeStateChunk(env, *args): pass
def RPR_Envelope_SetChunk(env, *args): pass
def RPR_Envelope_Sort(env): pass
def RPR_Envelope_SortDsts(env): pass
def RPR_Envelope_SortOrder(env): pass
def RPR_Envelope_SortPointsEx(env): pass
def RPR_Envelope_SortR(env): pass
def RPR_Envelope_SortRect(env): pass
def RPR_Envelope_SortRects(env): pass
def RPR_Envelope_SortRegisters(env): pass
def RPR_Envelope_SortRqst(env): pass
def RPR_Envelope_SortStates(env): pass
def RPR_Envelope_SortTrackEnvelopes(env): pass
def RPR_GetSetEnvelopeStateString(env, *args): return ""
def RPR_GetSetTrackEnvelopeInfo_String(env, *args): return ""
def RPR_BR_EnvSetShowInTrackControlPanel(env, *args): pass
def RPR_TrackFX_SetEnvelope(track_ptr, *args): pass
def RPR_TrackFX_SetEnvelopeState(track_ptr, *args): pass
def RPR_TrackFX_SetEnvelopeParam(track_ptr, *args): pass
def RPR_GetSetAutomationItemInfo(*args): return 0.0
def RPR_InsertAutomationItem(*args): return -1


# ===== FX extras =====

def RPR_TrackFX_GetCount(track_ptr):
    if _project and 0 <= track_ptr < len(_project.tracks):
        return len(_project.tracks[track_ptr].fx)
    return 0


def RPR_TrackFX_GetByName(track_ptr, fx_name, *args): return -1
def RPR_TrackFX_GetFXByName(track_ptr, fx_name, *args): return -1
def RPR_TrackFX_GetFXIdx(track_ptr, *args): return -1
def RPR_TrackFX_GetFXIdxByName(track_ptr, fx_name): return -1
def RPR_TrackFX_GetFXName(track_ptr, *args): return (0, track_ptr, 0, "", 256)
def RPR_TrackFX_GetFX(track_ptr, *args): return -1
def RPR_TrackFX_GetFXGUID(track_ptr, *args): return ""
def RPR_TrackFX_GetEnabled(track_ptr, *args): return True
def RPR_TrackFX_SetEnabled(track_ptr, *args): pass
def RPR_TrackFX_SetPreset(track_ptr, *args): pass
def RPR_TrackFX_SetEQParam(track_ptr, *args): pass
def RPR_TrackFX_SetEQBandEnabled(track_ptr, *args): pass
def RPR_TrackFX_SetEQBandParams(track_ptr, *args): pass
def RPR_TrackFX_SetEQBandType(track_ptr, *args): pass
def RPR_TrackFX_GetParamEx(track_ptr, *args): return (0.0, 0.0, 1.0, 0.5)
def RPR_TrackFX_GetParamFromNormalized(track_ptr, *args): return 0.0
def RPR_TrackFX_SetOpen(track_ptr, *args): pass
def RPR_TrackFX_SetTrackFXOpen(track_ptr, *args): pass
def RPR_TrackFX_SetPinMappings(track_ptr, *args): pass
def RPR_TrackFX_AddParameter(track_ptr, *args): return -1
def RPR_TrackFX_Delete(track_ptr, *args): pass
def RPR_TrackFX_GetJS(track_ptr, *args): return ""

def RPR_TakeFX_AddByName(take_ptr, fx_name, *args):
    """Take-level FX: forward to the take's track."""
    if 0 <= take_ptr < len(_takes):
        item_idx = _takes[take_ptr]["item_idx"]
        if 0 <= item_idx < len(_items):
            track_idx = _items[item_idx]["track_idx"]
            return RPR_TrackFX_AddByName(track_idx, fx_name, False, 1)
    return -1


def RPR_TakeFX_GetCount(take_ptr): return 0
def RPR_TakeFX_SetParam(take_ptr, *args): pass
def RPR_TakeFX_SetPreset(take_ptr, *args): pass


# ===== Project / transport / UI no-ops =====

def RPR_PreventUIRefresh(off): pass
def RPR_UpdateArrange(): pass
def RPR_UpdateTimeline(): pass
def RPR_UpdateItemInProject(item_ptr): pass
def RPR_UpdateItem(item_ptr): pass
def RPR_TrackList_AdjustWindows(*args): pass
def RPR_TrackList_UpdateAllCantBeUndone(): pass
def RPR_MarkAllMIDIItemsDirty(): pass
def RPR_MarkTrackItemsDirty(track_ptr): pass
def RPR_Undo_BeginBlock(): pass
def RPR_Undo_BeginBlock2(proj): pass
def RPR_Undo_EndBlock2(proj, desc, flags): pass
def RPR_Main_OnCommand(cmd, flag): pass
def RPR_OnCommand(cmd, flag): pass
def RPR_OnMidiEditorCommand(*args): pass
def RPR_NamedCommandLookup(name): return 0
def RPR_GetToggleCommandState(cmd): return 0
def RPR_GetToggleCommandStateEx(*args): return 0
def RPR_MIDIEditor_OnCommand(*args): pass
def RPR_MIDIEditor_GetActive(): return -1
def RPR_MIDIEditor_CreateOrGetMIDIEditor(): return -1
def RPR_MIDIEditor_LastFocused_OnCommand(*args): pass
def RPR_MIDIEditor_SetActiveTake(*args): pass
def RPR_GetCursorPosition(): return 0.0
def RPR_GetPlayPosition(): return 0.0
def RPR_SetEditCurPos(*args): pass
def RPR_OnStopButton(): pass
def RPR_CSurf_OnStop(): pass
def RPR_CSurf_OnTempoChange(*args): pass
def RPR_CSurf_OnMidiChange(*args): pass
def RPR_GetSet_LoopTimeRange(*args): return (0.0, 0.0, 0.0, 0)
def RPR_GetSet_LoopTimeRange2(*args): return (0.0, 0.0, 0.0, 0)
def RPR_GetSetRepeat(state): return 0
def RPR_AddProjectMarker(*args): return 0
def RPR_AddProjectMarker2(*args): return 0
def RPR_GetProjectName(*args): return ""
def RPR_GetSetProjectInfo_String(*args): return (0, "")
def RPR_WritePrivateProfileString(*args): return 0
def RPR_GetProjectBPM(): return _project.bpm if _project else 120.0
def RPR_Master_GetTempo(): return _project.bpm if _project else 120.0
def RPR_GetProjectTimeSignature(): return (4.0, 4.0)
def RPR_TimeMap_GetMeasures(*args): return 0
def RPR_TimeMap_GetMeasuresAndBeatInfo(*args): return (0, 0, 0.0)
def RPR_SetTempoTimeSigMarker(*args): return 0
def RPR_SetOnlyTrackSelected(track_ptr): pass
def RPR_SetTrackSelected(track_ptr, sel): pass
def RPR_SetTrackColor(track_ptr, color): pass
def RPR_ColorToNative(r, g, b): return (r << 16) | (g << 8) | b
def RPR_DBToNormalized(db): return min(max((db + 60) / 72, 0), 1)
def RPR_DB2SL(db): return min(max(10 ** (db / 20), 0), 4)
def RPR_log(msg): pass
def RPR_log10(x):
    import math
    return math.log10(x) if x > 0 else 0
def RPR_ShowConsoleMsg(msg): pass
def RPR_GetSetTrackState(track_ptr, *args): return ""
def RPR_GetTrackState(track_ptr, *args): return (0, "")
def RPR_SetTrackState(track_ptr, *args): pass
def RPR_SetTrackStateChunk(track_ptr, *args): pass
def RPR_GetSetObjectState(obj, *args): return ""
def RPR_SetTrackUIState(track_ptr, *args): pass
def RPR_SetTrackUIAutomationMode(track_ptr, *args): pass
def RPR_SetTrackUIDisarm(track_ptr, *args): pass
def RPR_SetTrackAutomationMode(track_ptr, *args): pass
def RPR_GetSetMediaItemTake_Source(take_ptr, *args): return 0
def RPR_TakeIsMIDI(take_ptr): return 1
def RPR_GetTrackSendInfo_Set(*args): return 0
def RPR_GetTrackNumSends(track_ptr, cat): return 0
def RPR_SplitMediaItem(item_ptr, t): return item_ptr
def RPR_RPR_SetCurrentBPM(*args):
    return RPR_SetCurrentBPM(*args[:3]) if len(args) >= 3 else None
def RPR_CreateNewMIDIItemInTake(track_ptr, *args):
    item = RPR_AddMediaItemToTrack(track_ptr)
    return RPR_AddTakeToMediaItem(item)
def RPR_CreateNewMediaItem(track_ptr): return RPR_AddMediaItemToTrack(track_ptr)
def RPR_JS_Window_SetSource(*args): pass
def RPR_SNM_SetMediaItemTake_SourceMIDI(*args): pass


# -------------------------------------------------------------------------
# Permissive fallback for any RPR_ function we haven't enumerated. This
# means future skills that use exotic API calls don't crash — they just
# silently no-op. Returns a callable that swallows args and returns 0.
# -------------------------------------------------------------------------
def __getattr__(name):
    if name.startswith("RPR_"):
        def _stub(*args, **kwargs):
            return 0
        _stub.__name__ = f"_stub_{name}"
        return _stub
    raise AttributeError(name)


# All RPR_ functions are exposed at module level so that
# `import reaper_python as RPR; RPR.RPR_InsertTrackAtIndex(...)` works.

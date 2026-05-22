import reaper_python as RPR

# Curve shape constants for automation points
# RPR_GetEnvelopePointShape docs for possible values.
# 0 = linear
# 1 = square
# 2 = slow start/end
# 3 = fast start/end
# 4 = bezier (requires tension parameter, not handled in this simplified demo)
CURVE_SHAPES = {
    "linear": 0,
    "square": 1,
    "slow_start_end": 2,
    "fast_start_end": 3
}

def create_video_transition(
    project_name: str = "ReaperVideoTransitions", # Not directly used by code, but for contextual awareness
    transition_type: str = "dissolve",  # "dissolve", "fade_to_black", "dip_to_white", "slide_left_crop"
    transition_duration_beats: float = 4.0,
    gap_duration_beats: float = 2.0,  # Only for "fade_to_black" and "dip_to_white"
    curve_type: str = "slow_start_end", # "linear", "square", "slow_start_end", "fast_start_end"
    bpm: int = 120,
    **kwargs,
) -> str:
    """
    Creates a video transition between two dummy video clips in REAPER.
    The dummy clips are generated solid colors (blue and red).

    Args:
        project_name: Project identifier (for logging/context).
        transition_type: Type of transition ("dissolve", "fade_to_black", "dip_to_white", "slide_left_crop").
        transition_duration_beats: Length of the transition effect in beats.
        gap_duration_beats: Duration of pure black/white/cropped area in beats for specific transitions.
        curve_type: Automation curve shape ("linear", "square", "slow_start_end", "fast_start_end").
        bpm: Tempo in BPM.
        **kwargs: Additional overrides (not used in this example).

    Returns:
        Status string describing what was created.
    """
    RPR.Undo_BeginBlock2(0) # Start an undo block for atomic operation

    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Convert beats to time (seconds)
    beats_to_time = lambda b: RPR.RPR_TimeMap2_beatsToTime(0, b)
    transition_time = beats_to_time(transition_duration_beats)
    gap_time = beats_to_time(gap_duration_beats)
    
    # Get curve shape constant
    curve_shape_idx = CURVE_SHAPES.get(curve_type, 2) # Default to slow_start_end

    # --- Setup Tracks ---
    # Determine the starting index for new tracks to be additive
    base_track_idx = RPR.RPR_CountTracks(0)

    # Track 1: First Video (Blue)
    RPR.RPR_InsertTrackAtIndex(base_track_idx, True)
    track1 = RPR.RPR_GetTrack(0, base_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track1, "P_NAME", f"{transition_type} - Video 1 (Blue)", True)
    
    # Track 2: Second Video (Red) - this track will be revealed
    RPR.RPR_InsertTrackAtIndex(base_track_idx + 1, True)
    track2 = RPR.RPR_GetTrack(0, base_track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track2, "P_NAME", f"{transition_type} - Video 2 (Red)", True)

    # --- Place Dummy Video Items and Apply Color Generators ---
    # Define item timings based on transition type
    # All transitions start at 0.0 for the first video for simplicity in this demo.
    
    item1_start_time = 0.0
    # Make item1 long enough to cover its part of the transition, plus some lead-in/out
    item1_active_length = transition_time * 2 + gap_time # For fades, covers fade out + gap
    if transition_type in ["dissolve", "slide_left_crop"]:
        item1_active_length = transition_time + transition_time # Cover overlap for first item
    item1_overall_length = item1_active_length + transition_time # Add extra for context

    # item2_start_time is where the transition visually *begins* to involve the second item
    item2_visual_transition_start_time = item1_start_time + (transition_time if transition_type in ["dissolve", "slide_left_crop"] else (transition_time + gap_time))
    item2_overall_length = transition_time * 2 + gap_time # Make item2 long enough

    # Item 1 on Track 1 (Blue)
    item1_reaper = RPR.RPR_AddMediaItemToTrack(track1)
    RPR.RPR_SetMediaItemInfo_Value(item1_reaper, "D_POSITION", item1_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item1_reaper, "D_LENGTH", item1_overall_length)
    take1 = RPR.RPR_GetActiveTake(item1_reaper)
    # Add a Video processor FX to the take to generate a solid blue color
    RPR.RPR_TakeFX_AddByName(take1, "Video processor", False, -1)
    fx_idx_take1 = RPR.RPR_TakeFX_GetCount(take1) - 1
    RPR.RPR_TakeFX_SetPreset(take1, fx_idx_take1, "Simple color generator - Blue") 
    
    # Item 2 on Track 2 (Red)
    item2_reaper = RPR.RPR_AddMediaItemToTrack(track2)
    RPR.RPR_SetMediaItemInfo_Value(item2_reaper, "D_POSITION", item2_visual_transition_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item2_reaper, "D_LENGTH", item2_overall_length)
    take2 = RPR.RPR_GetActiveTake(item2_reaper)
    # Add a Video processor FX to the take to generate a solid red color
    RPR.RPR_TakeFX_AddByName(take2, "Video processor", False, -1)
    fx_idx_take2 = RPR.RPR_TakeFX_GetCount(take2) - 1
    RPR.RPR_TakeFX_SetPreset(take2, fx_idx_take2, "Simple color generator - Red")


    # --- Apply Transition Logic ---
    status_msg = ""

    if transition_type == "dissolve":
        # Add Video processor FX to track 1 for opacity control
        track_fx_idx1 = RPR.RPR_TrackFX_AddByName(track1, "Video processor", False, -1)
        # Parameter 11 (index 10) is Opacity for default Video processor FX on track
        env = RPR.RPR_GetTrackEnvelopeByName(track1, f"FX {track_fx_idx1 + 1} param 11") 
        RPR.RPR_SetEnvelopeState(env, True) # Enable envelope

        # Opacity of Track 1 goes from 1.0 (visible) to 0.0 (transparent) during transition_time
        RPR.RPR_InsertEnvelopePoint(env, item2_visual_transition_start_time, 1.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env, item2_visual_transition_start_time + transition_time, 0.0, curve_shape_idx, 0.5, False, True)
        
        status_msg = f"Created '{transition_type}' transition over {transition_duration_beats} beats ({curve_type} curve)."

    elif transition_type == "fade_to_black":
        # Adjust item lengths to create a black gap where nothing is visible
        item1_fade_out_start_time = item2_visual_transition_start_time - transition_time 
        item1_fade_out_end_time = item2_visual_transition_start_time
        
        RPR.RPR_SetMediaItemInfo_Value(item1_reaper, "D_LENGTH", item1_fade_out_end_time)
        RPR.RPR_SetMediaItemInfo_Value(item2_reaper, "D_POSITION", item1_fade_out_end_time + gap_time)
        
        # Track 1 fades out to black
        track_fx_idx1 = RPR.RPR_TrackFX_AddByName(track1, "Video processor", False, -1)
        env1 = RPR.RPR_GetTrackEnvelopeByName(track1, f"FX {track_fx_idx1 + 1} param 11")
        RPR.RPR_SetEnvelopeState(env1, True)
        RPR.RPR_InsertEnvelopePoint(env1, item1_fade_out_start_time, 1.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env1, item1_fade_out_end_time, 0.0, curve_shape_idx, 0.5, False, True)

        # Track 2 fades in from black
        track_fx_idx2 = RPR.RPR_TrackFX_AddByName(track2, "Video processor", False, -1)
        env2 = RPR.RPR_GetTrackEnvelopeByName(track2, f"FX {track_fx_idx2 + 1} param 11")
        RPR.RPR_SetEnvelopeState(env2, True)
        item2_actual_start = RPR.RPR_GetMediaItemInfo_Value(item2_reaper, "D_POSITION")
        RPR.RPR_InsertEnvelopePoint(env2, item2_actual_start, 0.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env2, item2_actual_start + transition_time, 1.0, curve_shape_idx, 0.5, False, True)
        
        status_msg = f"Created '{transition_type}' transition over {transition_duration_beats} beats with {gap_duration_beats} beat gap ({curve_type} curve)."

    elif transition_type == "dip_to_white":
        # Track 3: White solid background. Inserted below video tracks.
        RPR.RPR_InsertTrackAtIndex(base_track_idx + 2, True)
        track3 = RPR.RPR_GetTrack(0, base_track_idx + 2)
        RPR.RPR_GetSetMediaTrackInfo_String(track3, "P_NAME", f"{transition_type} - White Background", True)

        # White item timing: covers the fade-out of video 1, the gap, and the fade-in of video 2
        white_item_display_start = item1_start_time + transition_time 
        white_item_display_end = white_item_display_start + transition_time + gap_time + transition_time
        
        white_item_reaper = RPR.RPR_AddMediaItemToTrack(track3)
        RPR.RPR_SetMediaItemInfo_Value(white_item_reaper, "D_POSITION", white_item_display_start)
        RPR.RPR_SetMediaItemInfo_Value(white_item_reaper, "D_LENGTH", white_item_display_end - white_item_display_start)
        white_take = RPR.RPR_GetActiveTake(white_item_reaper)
        RPR.RPR_TakeFX_AddByName(white_take, "Video processor", False, -1)
        fx_idx_white = RPR.RPR_TakeFX_GetCount(white_take) - 1
        RPR.RPR_TakeFX_SetPreset(white_take, fx_idx_white, "Simple color generator - White")

        # Adjust item positions for clarity in timeline
        item1_fade_out_start_time = item2_visual_transition_start_time - transition_time
        item1_fade_out_end_time = item2_visual_transition_start_time
        RPR.RPR_SetMediaItemInfo_Value(item1_reaper, "D_LENGTH", item1_fade_out_end_time)
        RPR.RPR_SetMediaItemInfo_Value(item2_reaper, "D_POSITION", item1_fade_out_end_time + gap_time)
        
        # Track 1 fades out to white
        track_fx_idx1 = RPR.RPR_TrackFX_AddByName(track1, "Video processor", False, -1)
        env1 = RPR.RPR_GetTrackEnvelopeByName(track1, f"FX {track_fx_idx1 + 1} param 11")
        RPR.RPR_SetEnvelopeState(env1, True)
        RPR.RPR_InsertEnvelopePoint(env1, item1_fade_out_start_time, 1.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env1, item1_fade_out_end_time, 0.0, curve_shape_idx, 0.5, False, True)

        # Track 2 fades in from white
        track_fx_idx2 = RPR.RPR_TrackFX_AddByName(track2, "Video processor", False, -1)
        env2 = RPR.RPR_GetTrackEnvelopeByName(track2, f"FX {track_fx_idx2 + 1} param 11")
        RPR.RPR_SetEnvelopeState(env2, True)
        item2_actual_start = RPR.RPR_GetMediaItemInfo_Value(item2_reaper, "D_POSITION")
        RPR.RPR_InsertEnvelopePoint(env2, item2_actual_start, 0.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env2, item2_actual_start + transition_time, 1.0, curve_shape_idx, 0.5, False, True)
        
        status_msg = f"Created '{transition_type}' transition over {transition_duration_beats} beats with {gap_duration_beats} beat gap ({curve_type} curve)."

    elif transition_type == "slide_left_crop":
        # Track 1 crops from left, revealing Track 2 underneath
        # Items are already overlapping
        
        # Add Video processor FX to track 1 for cropping
        track_fx_idx1 = RPR.RPR_TrackFX_AddByName(track1, "Video processor", False, -1)
        env = RPR.RPR_GetTrackEnvelopeByName(track1, f"FX {track_fx_idx1 + 1} param 4") # Param 4 is Crop L (index 3)
        RPR.RPR_SetEnvelopeState(env, True)

        # Crop L from 0.0 (no crop) to 1.0 (full crop)
        # Transition happens from item2_visual_transition_start_time to item2_visual_transition_start_time + transition_time
        RPR.RPR_InsertEnvelopePoint(env, item2_visual_transition_start_time, 0.0, curve_shape_idx, 0.5, False, True)
        RPR.RPR_InsertEnvelopePoint(env, item2_visual_transition_start_time + transition_time, 1.0, curve_shape_idx, 0.5, False, True)
        
        status_msg = f"Created '{transition_type}' transition over {transition_duration_beats} beats ({curve_type} curve)."
    
    else:
        RPR.Undo_EndBlock2(0, "Create Video Transition - Failed", 0)
        return f"Error: Unknown transition type '{transition_type}'"

    RPR.UpdateArrange() # Refresh REAPER's UI
    # RPR.Main_OnCommand(40889, 0) # Update all FX windows - this can be too aggressive and annoying for repeated use
    RPR.Undo_EndBlock2(0, f"Create {transition_type} Video Transition", 1) # End undo block
    return status_msg


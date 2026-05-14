import reaper_python as RPR
import os

# Helper to find a parameter index by name in a Video Processor FX
def get_video_processor_param_idx(track, fx_idx, param_name):
    """Retrieves the parameter index for a given named parameter on a Video Processor FX."""
    num_params = RPR.RPR_TrackFX_GetNumParams(track, fx_idx)
    for i in range(num_params):
        # The third argument is a buffer to receive the name, 256 is its size
        success, name = RPR.RPR_TrackFX_GetParamName(track, fx_idx, i, "", 256)
        if success and name.strip().lower() == param_name.lower():
            return i
    return -1

# Helper to automate a Video Processor parameter
def automate_video_param(track, fx_idx, param_name, points, curve_shape):
    """
    Automates a specific Video Processor parameter with given points and curve shape.
    points: List of (time, normalized_value) tuples.
    curve_shape: 0=Linear, 1=Square, 2=Slow Start/End, 3=Fast Start/End, 4=Bezier.
    """
    param_idx = get_video_processor_param_idx(track, fx_idx, param_name)
    if param_idx == -1:
        RPR.RPR_ShowConsoleMsg(f"Error: Parameter '{param_name}' not found on Video Processor on track '{RPR.RPR_GetTrackName(track, '', 256)[1]}'.\n")
        return

    envelope = RPR.RPR_GetTrackEnvelope(track, param_idx)
    if not envelope:
        # Create envelope if it doesn't exist
        RPR.RPR_TrackFX_SetEnvelope(track, fx_idx, param_idx, True)
        envelope = RPR.RPR_GetTrackEnvelope(track, param_idx)
        if not envelope:
            RPR.RPR_ShowConsoleMsg(f"Error: Could not create envelope for '{param_name}' on track '{RPR.RPR_GetTrackName(track, '', 256)[1]}'.\n")
            return

    # To ensure clean automation for a specific transition, clear points in the affected range
    if points:
        RPR.RPR_DeleteEnvelopePointRange(envelope, points[0][0] - 0.1, points[-1][0] + 0.1) 
        
    for time, value in points:
        # RPR_Envelope_InsertPoint(envelope, time, value, shape, tension, selected, no_sort)
        RPR.RPR_Envelope_InsertPoint(envelope, time, value, curve_shape, 0.5, True, False) # 0.5 is default bezier tension

    RPR.RPR_TrackFX_SetTrackFXOpen(track, fx_idx, True) # Open FX window to make automation visible
    RPR.RPR_SetTrackSelected(track, True) # Select track to make envelope visible
    RPR.RPR_Main_OnCommand(40141, 0) # Show track envelope for last touched parameter

def create_video_transition(
    project_name: str = "ReaperVideoEdit", # Not used directly in script, for logging purposes
    transition_type: str = "dissolve", # "dissolve", "fade_to_black", "fade_to_white", "slide_left", "slide_right", "crop_left", "crop_right"
    duration_seconds: float = 1.0, # Length of the transition in seconds
    start_time_sec: float = 5.0, # The timeline position where the transition effect starts
    video_path_1: str = None, # Full path to the first video file (e.g., "C:\\Videos\\clip1.mp4")
    video_path_2: str = None, # Full path to the second video file (e.g., "C:\\Videos\\clip2.mp4")
    track_idx_base: int = -1, # Index of the first track to use. -1 to add new tracks at the end.
    curve_shape: int = 2, # Automation curve shape (0=Linear, 1=Square, 2=Slow Start/End, 3=Fast Start/End, 4=Bezier)
    **kwargs, # Additional overrides
) -> str:
    """
    Creates a basic video transition in the current REAPER project.

    Args:
        project_name: A descriptive project identifier.
        transition_type: The type of transition to create.
        duration_seconds: The duration of the transition effect in seconds.
        start_time_sec: The absolute time in the project where the transition animation begins.
        video_path_1: The file path for the first video clip.
        video_path_2: The file path for the second video clip.
        track_idx_base: The starting track index. -1 appends new tracks.
        curve_shape: The shape of the automation curve for smooth transitions.

    Returns:
        A status string indicating the success or failure of the operation.
    """
    # --- Input Validation ---
    if video_path_1 is None or not os.path.exists(video_path_1):
        return f"Error: video_path_1 '{video_path_1}' is invalid or not found. Please provide actual paths."
    if video_path_2 is None or not os.path.exists(video_path_2):
        return f"Error: video_path_2 '{video_path_2}' is invalid or not found. Please provide actual paths."
    if duration_seconds <= 0:
        return "Error: duration_seconds must be a positive value."
    if start_time_sec < 0:
        return "Error: start_time_sec cannot be negative."

    RPR.Undo_BeginBlock()

    # --- Determine Track Indices ---
    if track_idx_base == -1:
        track_idx_base = RPR.RPR_CountTracks(0)

    track_v1_idx = track_idx_base
    track_v2_idx = track_idx_base + 1
    track_color_idx = track_idx_base + 2 # Only used for fade_to_white/black color overlay

    # --- Create Tracks ---
    # Track for Video 1 (top layer for most transitions)
    RPR.RPR_InsertTrackAtIndex(track_v1_idx, True)
    track_v1 = RPR.RPR_GetTrack(0, track_v1_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_v1, "P_NAME", f"Video {track_v1_idx + 1} - {os.path.basename(video_path_1)}", True)

    # Track for Video 2 (bottom layer for most transitions)
    RPR.RPR_InsertTrackAtIndex(track_v2_idx, True)
    track_v2 = RPR.RPR_GetTrack(0, track_v2_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_v2, "P_NAME", f"Video {track_v2_idx + 1} - {os.path.basename(video_path_2)}", True)

    track_color = None
    if transition_type in ["fade_to_black", "fade_to_white"]:
        RPR.RPR_InsertTrackAtIndex(track_color_idx, True)
        track_color = RPR.RPR_GetTrack(0, track_color_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track_color, "P_NAME", f"Video {track_color_idx + 1} - {transition_type.replace('_', ' ').title()}", True)

    # --- Add Video Processor FX to relevant tracks ---
    fx_v1_idx = RPR.RPR_TrackFX_AddByName(track_v1, "Video processor", False, -1)
    fx_v2_idx = RPR.RPR_TrackFX_AddByName(track_v2, "Video processor", False, -1)

    if track_color:
        fx_color_idx = RPR.RPR_TrackFX_AddByName(track_color, "Video processor", False, -1)
        if transition_type == "fade_to_black":
            RPR.RPR_TrackFX_SetPreset(track_color, fx_color_idx, "Color - black solid")
        else: # fade_to_white
            RPR.RPR_TrackFX_SetPreset(track_color, fx_color_idx, "Color - white solid")
        # Ensure the color track is below video tracks and has full opacity
        automate_video_param(track_color, fx_color_idx, "opacity", [(start_time_sec, 1.0), (start_time_sec + duration_seconds, 1.0)], 0)


    # --- Calculate Transition Timings ---
    # `start_time_sec` is the point where the first video's fade-out starts for dissolve,
    # or the start of the solid color for fade to black/white,
    # or the start of the sliding/cropping for slide/crop.
    # The transition spans from start_time_sec to start_time_sec + duration_seconds

    # --- Transition Logic ---
    status_msg = "No transition created (unsupported type or error)."

    if transition_type == "dissolve":
        # Item 1 on Track 1, Item 2 on Track 2 (revealed underneath)
        # Both clips exist for the full duration of the overlap.
        item_v1 = RPR.RPR_AddMediaItemToTrack(track_v1)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_POSITION", start_time_sec)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_LENGTH", duration_seconds)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v1, 0), video_path_1, False)

        item_v2 = RPR.RPR_AddMediaItemToTrack(track_v2)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_POSITION", start_time_sec)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_LENGTH", duration_seconds)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v2, 0), video_path_2, False)

        # Automate opacity of Track 1 from 1.0 to 0.0
        points = [
            (start_time_sec, 1.0),
            (start_time_sec + duration_seconds, 0.0)
        ]
        automate_video_param(track_v1, fx_v1_idx, "opacity", points, curve_shape)
        
        status_msg = f"Created dissolve transition from '{os.path.basename(video_path_1)}' to '{os.path.basename(video_path_2)}' starting at {start_time_sec}s over {duration_seconds}s."

    elif transition_type in ["fade_to_black", "fade_to_white"]:
        # Item 1 on Track 1 fades out, then color track is visible, then Item 2 on Track 2 fades in
        
        # Clip 1: ends as it fades out to the color
        item_v1 = RPR.RPR_AddMediaItemToTrack(track_v1)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_POSITION", start_time_sec - duration_seconds / 2.0)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_LENGTH", duration_seconds / 2.0)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v1, 0), video_path_1, False)
        
        # The color item is placed from where V1 ends its fade out to where V2 starts its fade in
        item_color = RPR.RPR_AddMediaItemToTrack(track_color)
        RPR.RPR_SetMediaItemInfo_Value(item_color, "D_POSITION", start_time_sec)
        RPR.RPR_SetMediaItemInfo_Value(item_color, "D_LENGTH", duration_seconds)
        # Color preset already set above

        # Clip 2: starts as it fades in from the color
        item_v2 = RPR.RPR_AddMediaItemToTrack(track_v2)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_POSITION", start_time_sec + duration_seconds / 2.0)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_LENGTH", duration_seconds / 2.0)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v2, 0), video_path_2, False)

        # Automate opacity of Track 1 to fade out
        points_v1 = [
            (start_time_sec - duration_seconds / 2.0, 1.0),
            (start_time_sec, 0.0)
        ]
        automate_video_param(track_v1, fx_v1_idx, "opacity", points_v1, curve_shape)

        # Automate opacity of Track 2 to fade in
        points_v2 = [
            (start_time_sec + duration_seconds / 2.0, 0.0),
            (start_time_sec + duration_seconds, 1.0)
        ]
        automate_video_param(track_v2, fx_v2_idx, "opacity", points_v2, curve_shape)
        
        status_msg = f"Created {transition_type.replace('_',' ')} transition from '{os.path.basename(video_path_1)}' to '{os.path.basename(video_path_2)}' starting at {start_time_sec}s over {duration_seconds}s."

    elif transition_type.startswith(("slide_", "crop_")):
        # Item 1 on Track 1 (top), Item 2 on Track 2 (bottom)
        # Item 1 slides/crops out, revealing Item 2 underneath
        item_v1 = RPR.RPR_AddMediaItemToTrack(track_v1)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_POSITION", start_time_sec)
        RPR.RPR_SetMediaItemInfo_Value(item_v1, "D_LENGTH", duration_seconds)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v1, 0), video_path_1, False)

        item_v2 = RPR.RPR_AddMediaItemToTrack(track_v2)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_POSITION", start_time_sec)
        RPR.RPR_SetMediaItemInfo_Value(item_v2, "D_LENGTH", duration_seconds)
        RPR.RPR_SetMediaItemTake_Source(RPR.RPR_GetMediaItemTake(item_v2, 0), video_path_2, False)

        param_name = ""
        start_val_v1, end_val_v1 = 0.0, 0.0 # Normalized values for Track 1
        start_val_v2, end_val_v2 = 0.0, 0.0 # Normalized values for Track 2

        if transition_type == "slide_left":
            param_name = "x_position"
            start_val_v1, end_val_v1 = 0.0, -1.0 # V1 from center to off-left
            start_val_v2, end_val_v2 = 1.0, 0.0 # V2 from off-right to center
        elif transition_type == "slide_right":
            param_name = "x_position"
            start_val_v1, end_val_v1 = 0.0, 1.0 # V1 from center to off-right
            start_val_v2, end_val_v2 = -1.0, 0.0 # V2 from off-left to center
        elif transition_type == "crop_left":
            param_name = "crop_left"
            start_val_v1, end_val_v1 = 0.0, 1.0 # V1 from no crop to full crop
            start_val_v2, end_val_v2 = 1.0, 0.0 # V2 from full crop to no crop
        elif transition_type == "crop_right":
            param_name = "crop_right"
            start_val_v1, end_val_v1 = 0.0, 1.0 # V1 from no crop to full crop
            start_val_v2, end_val_v2 = 1.0, 0.0 # V2 from full crop to no crop
        # Additional slide_up/down (y_position) or crop_top/bottom transitions can be added here following similar logic.

        if param_name:
            points_v1 = [
                (start_time_sec, start_val_v1),
                (start_time_sec + duration_seconds, end_val_v1)
            ]
            automate_video_param(track_v1, fx_v1_idx, param_name, points_v1, curve_shape)
            
            # Automate Track 2 to slide/crop in (revealing itself)
            points_v2 = [
                (start_time_sec, start_val_v2),
                (start_time_sec + duration_seconds, end_val_v2)
            ]
            automate_video_param(track_v2, fx_v2_idx, param_name, points_v2, curve_shape)
            
            status_msg = f"Created {transition_type.replace('_',' ')} transition from '{os.path.basename(video_path_1)}' to '{os.path.basename(video_path_2)}' starting at {start_time_sec}s over {duration_seconds}s."
        else:
            status_msg = f"Error: Unsupported transition type '{transition_type}' for slide/crop."

    RPR.Undo_EndBlock(f"Create Video Transition: {transition_type.replace('_', ' ').title()}", True)
    return status_msg


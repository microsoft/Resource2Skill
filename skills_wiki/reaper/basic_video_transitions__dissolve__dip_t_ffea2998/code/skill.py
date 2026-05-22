import reaper_python as RPR
import time # For unique track names if needed, but not strictly used here.

def create_video_transitions(
    project_name: str = "ReaperVideoTransitions",
    transition_duration_sec: float = 1.0,
    item_duration_sec: float = 3.0,
    bpm: int = 120, # BPM is not directly used for video effects, but can help align timing.
    **kwargs,
) -> str:
    """
    Creates a demonstration of basic video transitions (Dissolve, Fade to Black, Dip to White, Slide Crop)
    in the current REAPER project using Video Processor JSFX and automation.

    Args:
        project_name: Project identifier (for logging).
        transition_duration_sec: Duration for each transition in seconds.
        item_duration_sec: Duration for each video segment before/after transition.
        bpm: Tempo (for context, not directly used in video effects).
        **kwargs: Additional overrides (not used for this specific skill but kept for consistency).

    Returns:
        Status string, e.g., "Created video transition demo tracks."
    """
    
    # === Helper function to add a Video Processor FX and get an envelope for a parameter ===
    # param_idx: The index of the parameter to automate (e.g., 10 for Opacity, 3 for Crop Left)
    # envelope_name_suffix: A unique suffix for the envelope name (e.g., "Opacity", "Crop Left")
    def add_vp_and_envelope(track, param_idx, envelope_name_suffix):
        # Add "Video processor" JSFX (default preset)
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "Video processor", False, -1)
        RPR.RPR_TrackFX_SetOpen(track, fx_idx, True) # Open FX window for visual feedback

        # The generic Video processor might not have named parameters, so we use a constructed name
        envelope_name = f"Video processor FX{fx_idx+1} {envelope_name_suffix}" 
        
        # Ensure the envelope for this parameter exists
        env = RPR.RPR_GetTrackEnvelopeByName(track, envelope_name)
        if not env:
            RPR.RPR_InsertTrackEnvelope(track, param_idx) 
            env = RPR.RPR_GetTrackEnvelopeByName(track, envelope_name)
        RPR.RPR_SetTrackEnvelopeState(env, 1) # Ensure envelope is visible and active
        return fx_idx, env

    # === Setup Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    current_time = 0.0

    RPR.RPR_TrackList_AdjustWindows(False) # Prevent UI redraw until done

    # --- Transition 1: Dissolve ---
    # Clip A (Top Layer) fades out, revealing Clip B (Bottom Layer)
    
    # Create Track 1 (top video: Clip A)
    track_idx1 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx1, True)
    track1 = RPR.RPR_GetTrack(0, track_idx1)
    RPR.RPR_GetSetMediaTrackInfo_String(track1, "P_NAME", f"Video - Dissolve Top", True)

    # Create Track 2 (bottom video: Clip B)
    track_idx2 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx2, True)
    track2 = RPR.RPR_GetTrack(0, track_idx2)
    RPR.RPR_GetSetMediaTrackInfo_String(track2, "P_NAME", f"Video - Dissolve Bottom", True)

    # Add dummy video items
    item1_start = current_time
    item1_end = current_time + item_duration_sec + transition_duration_sec # Clip A extends through transition
    item1 = RPR.RPR_AddMediaItemToTrack(track1)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_POSITION", item1_start)
    RPR.RPR_SetMediaItemInfo_Value(item1, "D_LENGTH", item1_end - item1_start)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item1, 0), "P_NAME", "Clip A", True)

    item2_start = current_time + item_duration_sec # Clip B starts at transition start
    item2_end = item2_start + item_duration_sec # Clip B
    item2 = RPR.RPR_AddMediaItemToTrack(track2)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_POSITION", item2_start)
    RPR.RPR_SetMediaItemInfo_Value(item2, "D_LENGTH", item2_end - item2_start)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item2, 0), "P_NAME", "Clip B", True)

    # Add Video Processor to the top track (track1) for opacity automation
    # For a dissolve, the top layer (Clip A) fades out.
    # Opacity parameter for generic Video processor: assumed index 10 (common for custom scripts) or trial-and-error
    opacity_fx_idx, opacity_env = add_vp_and_envelope(track1, 10, "Opacity") 
    
    # Add automation points: 100% (value 1.0) -> 0% (value 0.0)
    RPR.RPR_InsertEnvelopePoint(opacity_env, item_duration_sec, 1.0, 0, 0, True, False) # Before transition, full opacity
    RPR.RPR_InsertEnvelopePoint(opacity_env, item_duration_sec + transition_duration_sec, 0.0, 0, 0, True, False) # After transition, zero opacity
    
    # Set curve shape for dissolve to "Slow start end" (shape 2 in REAPER's envelope point shapes)
    RPR.RPR_SetEnvelopePointShape(opacity_env, 0, 2) 
    RPR.RPR_SetEnvelopePointShape(opacity_env, 1, 2) 

    current_time = item1_end + item_duration_sec # Advance time for next transition

    # --- Transition 2: Fade to Black ---
    # Clip C fades to black, then Clip D fades in from black.

    # Create Track 3 (video: Clip C)
    track_idx3 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx3, True)
    track3 = RPR.RPR_GetTrack(0, track_idx3)
    RPR.RPR_GetSetMediaTrackInfo_String(track3, "P_NAME", f"Video - Fade Out Black", True)

    # Add dummy video item (Clip C)
    item3 = RPR.RPR_AddMediaItemToTrack(track3)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item3, "D_LENGTH", item_duration_sec + transition_duration_sec)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item3, 0), "P_NAME", "Clip C", True)

    # Add Video Processor to track3 for opacity automation
    opacity_fx_idx3, opacity_env3 = add_vp_and_envelope(track3, 10, "Opacity")

    # Fade out Clip C to black
    fade_out_start_time = current_time + item_duration_sec
    RPR.RPR_InsertEnvelopePoint(opacity_env3, fade_out_start_time, 1.0, 0, 0, True, False)
    RPR.RPR_InsertEnvelopePoint(opacity_env3, fade_out_start_time + transition_duration_sec, 0.0, 0, 0, True, False)
    RPR.RPR_SetEnvelopePointShape(opacity_env3, 0, 2)
    RPR.RPR_SetEnvelopePointShape(opacity_env3, 1, 2)

    current_time = fade_out_start_time + transition_duration_sec # Time when fully black

    # Create Track 4 (next video: Clip D)
    track_idx4 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx4, True)
    track4 = RPR.RPR_GetTrack(0, track_idx4)
    RPR.RPR_GetSetMediaTrackInfo_String(track4, "P_NAME", f"Video - Fade In Black", True)

    # Add dummy video item (Clip D)
    item4 = RPR.RPR_AddMediaItemToTrack(track4)
    RPR.RPR_SetMediaItemInfo_Value(item4, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item4, "D_LENGTH", item_duration_sec)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item4, 0), "P_NAME", "Clip D", True)

    # Add Video Processor to track4 for opacity automation
    opacity_fx_idx4, opacity_env4 = add_vp_and_envelope(track4, 10, "Opacity")

    # Fade in Clip D from black
    fade_in_start_time = current_time
    RPR.RPR_InsertEnvelopePoint(opacity_env4, fade_in_start_time, 0.0, 0, 0, True, False) # Starts at 0% opacity
    RPR.RPR_InsertEnvelopePoint(opacity_env4, fade_in_start_time + transition_duration_sec, 1.0, 0, 0, True, False) # Ends at 100% opacity
    RPR.RPR_SetEnvelopePointShape(opacity_env4, 0, 2)
    RPR.RPR_SetEnvelopePointShape(opacity_env4, 1, 2)

    current_time = fade_in_start_time + item_duration_sec + transition_duration_sec # Advance time

    # --- Transition 3: Dip to White ---
    # Clip E dips to white, then Clip F dips from white.

    # Create Track 5 (video: Clip E)
    track_idx5 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx5, True)
    track5 = RPR.RPR_GetTrack(0, track_idx5)
    RPR.RPR_GetSetMediaTrackInfo_String(track5, "P_NAME", f"Video - Dip Out White", True)

    # Create Track 6 (white background)
    track_idx6 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx6, True)
    track6 = RPR.RPR_GetTrack(0, track_idx6)
    RPR.RPR_GetSetMediaTrackInfo_String(track6, "P_NAME", f"White Background Layer", True)

    # Add a Video Processor to generate white color on track 6
    white_vp_fx_idx = RPR.RPR_TrackFX_AddByName(track6, "Video processor", False, -1)
    # The tutorial mentions "JT Essential Color Controls (video)" preset for solid color
    RPR.RPR_TrackFX_SetPreset(track6, white_vp_fx_idx, "JT Essential Color Controls (video)")
    RPR.RPR_TrackFX_SetParam(track6, white_vp_fx_idx, 0, 1.0) # Assuming Param 0 is Red
    RPR.RPR_TrackFX_SetParam(track6, white_vp_fx_idx, 1, 1.0) # Assuming Param 1 is Green
    RPR.RPR_TrackFX_SetParam(track6, white_vp_fx_idx, 2, 1.0) # Assuming Param 2 is Blue (all 1.0 = white)
    RPR.RPR_TrackFX_SetOpen(track6, white_vp_fx_idx, True) # Open FX window for visual feedback

    # Add dummy video item (Clip E)
    item5 = RPR.RPR_AddMediaItemToTrack(track5)
    RPR.RPR_SetMediaItemInfo_Value(item5, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item5, "D_LENGTH", item_duration_sec + transition_duration_sec)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item5, 0), "P_NAME", "Clip E", True)

    # Add Video Processor to track5 for opacity automation
    opacity_fx_idx5, opacity_env5 = add_vp_and_envelope(track5, 10, "Opacity")

    # Dip out Clip E to white
    dip_out_start_time = current_time + item_duration_sec
    RPR.RPR_InsertEnvelopePoint(opacity_env5, dip_out_start_time, 1.0, 0, 0, True, False)
    RPR.RPR_InsertEnvelopePoint(opacity_env5, dip_out_start_time + transition_duration_sec, 0.0, 0, 0, True, False)
    RPR.RPR_SetEnvelopePointShape(opacity_env5, 0, 2)
    RPR.RPR_SetEnvelopePointShape(opacity_env5, 1, 2)

    current_time = dip_out_start_time + transition_duration_sec # Time when fully white

    # Create Track 7 (next video: Clip F)
    track_idx7 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx7, True)
    track7 = RPR.RPR_GetTrack(0, track_idx7)
    RPR.RPR_GetSetMediaTrackInfo_String(track7, "P_NAME", f"Video - Dip In White", True)

    # Add dummy video item (Clip F)
    item7 = RPR.RPR_AddMediaItemToTrack(track7)
    RPR.RPR_SetMediaItemInfo_Value(item7, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item7, "D_LENGTH", item_duration_sec)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item7, 0), "P_NAME", "Clip F", True)

    # Add Video Processor to track7 for opacity automation
    opacity_fx_idx7, opacity_env7 = add_vp_and_envelope(track7, 10, "Opacity")

    # Dip in Clip F from white
    dip_in_start_time = current_time
    RPR.RPR_InsertEnvelopePoint(opacity_env7, dip_in_start_time, 0.0, 0, 0, True, False)
    RPR.RPR_InsertEnvelopePoint(opacity_env7, dip_in_start_time + transition_duration_sec, 1.0, 0, 0, True, False)
    RPR.RPR_SetEnvelopePointShape(opacity_env7, 0, 2)
    RPR.RPR_SetEnvelopePointShape(opacity_env7, 1, 2)

    current_time = dip_in_start_time + item_duration_sec + transition_duration_sec # Advance time

    # --- Transition 4: Slide Crop Left ---
    # Clip G slides off screen from the left, revealing Clip H.

    # Create Track 8 (top video: Clip G)
    track_idx8 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx8, True)
    track8 = RPR.RPR_GetTrack(0, track_idx8)
    RPR.RPR_GetSetMediaTrackInfo_String(track8, "P_NAME", f"Video - Slide Crop Top", True)

    # Create Track 9 (bottom video: Clip H)
    track_idx9 = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx9, True)
    track9 = RPR.RPR_GetTrack(0, track_idx9)
    RPR.RPR_GetSetMediaTrackInfo_String(track9, "P_NAME", f"Video - Slide Crop Bottom", True)

    # Add dummy video items
    item8_start = current_time
    item8_end = current_time + item_duration_sec + transition_duration_sec # Clip G extends through transition
    item8 = RPR.RPR_AddMediaItemToTrack(track8)
    RPR.RPR_SetMediaItemInfo_Value(item8, "D_POSITION", item8_start)
    RPR.RPR_SetMediaItemInfo_Value(item8, "D_LENGTH", item8_end - item8_start)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item8, 0), "P_NAME", "Clip G", True)

    item9_start = current_time + item_duration_sec # Clip H starts at transition start
    item9_end = item9_start + item_duration_sec
    item9 = RPR.RPR_AddMediaItemToTrack(track9)
    RPR.RPR_SetMediaItemInfo_Value(item9, "D_POSITION", item9_start)
    RPR.RPR_SetMediaItemInfo_Value(item9, "D_LENGTH", item9_end - item9_start)
    RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(item9, 0), "P_NAME", "Clip H", True)

    # Add Video Processor to the top track (track8) for Crop Left automation
    # Crop Left is typically param index 3 for "JT Essential Video Controls" preset.
    # Value range for crop parameters is usually 0.0 (no crop) to 1.0 (fully cropped).
    crop_fx_idx8, crop_env8 = add_vp_and_envelope(track8, 3, "Crop Left")

    # Automate Crop Left (0.0 means no crop, 1.0 means fully cropped from left)
    crop_start_time = current_time + item_duration_sec
    RPR.RPR_InsertEnvelopePoint(crop_env8, crop_start_time, 0.0, 0, 0, True, False) # Start with no crop
    RPR.RPR_InsertEnvelopePoint(crop_env8, crop_start_time + transition_duration_sec, 1.0, 0, 0, True, False) # Fully cropped
    RPR.RPR_SetEnvelopePointShape(crop_env8, 0, 2)
    RPR.RPR_SetEnvelopePointShape(crop_env8, 1, 2)
    
    RPR.RPR_TrackList_AdjustWindows(True) # Re-enable UI redraw
    RPR.RPR_UpdateArrange()

    return f"Created basic video transition demo with Dissolve, Fade to Black, Dip to White, and Slide Crop Left transitions."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicRig",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for rig
    **kwargs,
) -> str:
    """
    Create a Procedural Cinematic Tracking Camera Rig.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig components.
        location: (x, y, z) world-space position of the focal target.
        scale: Radius of the camera sweep/orbit.
        material_color: Unused for cameras/empties.
        **kwargs: Additional overrides (e.g., frames=250 for loop duration).
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configuration
    anim_frames = kwargs.get('frames', 250)
    radius = scale * 5.0

    # === Step 1: Create Master Controller ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    master_empty = bpy.context.active_object
    master_empty.name = f"{object_name}_Master"
    master_empty.empty_display_size = scale * 0.2

    # === Step 2: Create Focus Target ===
    bpy.ops.object.empty_add(type='SPHERE', location=location)
    target_empty = bpy.context.active_object
    target_empty.name = f"{object_name}_FocusTarget"
    target_empty.empty_display_size = scale * 0.5
    target_empty.parent = master_empty

    # === Step 3: Create Camera Track (Bezier Circle) ===
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=location)
    cam_track = bpy.context.active_object
    cam_track.name = f"{object_name}_Track"
    cam_track.parent = master_empty
    
    # Optional: Tilt the track slightly for a more dynamic orbit
    cam_track.rotation_euler = (0.2, 0.0, 0.0)

    # === Step 4: Create Camera ===
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.name = f"{object_name}_Cam"
    
    # Setup Lens & Depth of Field
    camera.data.lens = 50.0  # 50mm standard focal length
    camera.data.dof.use_dof = True
    camera.data.dof.focus_object = target_empty
    camera.data.dof.aperture_fstop = 2.8
    
    # Set this camera as the active scene camera
    scene.camera = camera

    # === Step 5: Setup Constraints ===
    # 1. Follow Path
    follow_path = camera.constraints.new(type='FOLLOW_PATH')
    follow_path.target = cam_track
    follow_path.use_fixed_position = True # Allows 0.0 - 1.0 offset animation
    follow_path.forward_axis = 'TRACK_NEGATIVE_Z'
    follow_path.up_axis = 'UP_Y'
    
    # 2. Track To
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = target_empty
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

    # === Step 6: Animate the Camera Sweep ===
    # Keyframe start
    follow_path.offset_factor = 0.0
    follow_path.keyframe_insert(data_path="offset_factor", frame=1)
    
    # Keyframe end
    follow_path.offset_factor = 1.0
    follow_path.keyframe_insert(data_path="offset_factor", frame=anim_frames + 1) # +1 ensures frame 1 and 250 are sequential for perfect loops

    # Ensure linear interpolation for smooth, constant-speed orbit
    if camera.animation_data and camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            if fcurve.data_path == "constraints[\"Follow Path\"].offset_factor":
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                    
    # Ensure scene length accommodates the animation
    scene.frame_end = max(scene.frame_end, anim_frames)

    return f"Created '{object_name}' rig at {location}. Camera constrained to track, focusing on Target."

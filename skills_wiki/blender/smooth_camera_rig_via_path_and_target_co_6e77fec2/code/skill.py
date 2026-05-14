def create_object(
    scene_name: str = "Scene",
    object_name: str = "SmoothCamRig",
    location: tuple = (0.0, 0.0, 1.0),
    scale: float = 5.0,
    material_color: tuple = (0.0, 0.0, 0.0),  # Unused for invisible rigs
    **kwargs,
) -> str:
    """
    Create a Smooth Camera Rig in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the rig components.
        location: (x, y, z) focal point the camera will look at.
        scale: Radius of the camera path (distance from target).
        material_color: Unused.
        **kwargs: Additional overrides (e.g., animation_frames).

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    anim_frames = kwargs.get("animation_frames", 250)

    # === Step 1: Create Target Empty ===
    bpy.ops.object.empty_add(type='SPHERE', radius=0.5, location=location)
    target = bpy.context.active_object
    target.name = f"{object_name}_Target"
    
    # === Step 2: Create Camera Path (Bezier Circle) ===
    # Elevate the path slightly above the target for a dynamic downward angle
    path_loc = (location[0], location[1], location[2] + (scale * 0.4))
    bpy.ops.curve.primitive_bezier_circle_add(radius=scale, location=path_loc)
    path = bpy.context.active_object
    path.name = f"{object_name}_Path"
    
    # Parent path to target so moving the target moves the entire rig
    path.parent = target
    
    # === Step 3: Create Camera ===
    bpy.ops.object.camera_add(location=path_loc)
    cam = bpy.context.active_object
    cam.name = f"{object_name}_Camera"
    
    # Set this camera as the active scene camera
    scene.camera = cam
    
    # === Step 4: Apply Constraints ===
    # 1. Follow Path (handles translation)
    follow_const = cam.constraints.new(type='FOLLOW_PATH')
    follow_const.target = path
    follow_const.forward_axis = 'TRACK_NEGATIVE_Z'
    follow_const.up_axis = 'UP_Y'
    follow_const.use_fixed_location = True  # Allows animating 0-1 offset factor
    
    # 2. Track To (handles rotation/aiming)
    track_const = cam.constraints.new(type='TRACK_TO')
    track_const.target = target
    track_const.track_axis = 'TRACK_NEGATIVE_Z'
    track_const.up_axis = 'UP_Y'
    
    # === Step 5: Animate the Sweep ===
    # Keyframe offset from 0.0 to 1.0 over the duration
    follow_const.offset_factor = 0.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=1)
    
    follow_const.offset_factor = 1.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=anim_frames)
    
    # Force Linear interpolation for constant speed (no ease-in/out)
    if cam.animation_data and cam.animation_data.action:
        for fcurve in cam.animation_data.action.fcurves:
            if fcurve.data_path == 'constraints["Follow Path"].offset_factor':
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                    
    # Setup Depth of Field to automatically focus on the Target
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = target
    cam.data.dof.aperture_fstop = 2.8

    # Clean up selection
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created Camera Rig '{object_name}' orbiting {location} with radius {scale}."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicCameraRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for cameras
    **kwargs,
) -> str:
    """
    Create a Path-Following Cinematic Camera Rig in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the camera, track, and target objects.
        location: Center point of the tracking path.
        scale: Scales the radius of the camera path.
        material_color: Unused.
        **kwargs: 
            duration_frames (int): Length of the animation loop.
            focal_length (float): Lens size in mm (e.g., 35.0 wide, 50.0 standard).
            look_at_location (tuple): 3D coordinate the camera looks at.

    Returns:
        Status string describing the created camera rig.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Parametric Setup
    path_radius = scale * 10.0
    duration_frames = kwargs.get("duration_frames", 250)
    focal_length = kwargs.get("focal_length", 50.0)
    
    # Default elevations if not explicitly provided
    path_loc = (location[0], location[1], location[2] + scale * 2.0)
    look_at_location = kwargs.get("look_at_location", (location[0], location[1], location[2] + scale * 1.0))

    # === Step 1: Create the Tracking Path (Bezier Circle) ===
    bpy.ops.curve.primitive_bezier_circle_add(radius=path_radius, location=path_loc)
    path_obj = bpy.context.active_object
    path_obj.name = f"{object_name}_Track"
    
    # === Step 2: Create the Look-At / Focus Target (Empty) ===
    bpy.ops.object.empty_add(type='CROSS', radius=scale, location=look_at_location)
    target_obj = bpy.context.active_object
    target_obj.name = f"{object_name}_Target"

    # === Step 3: Create and Configure Camera ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Data")
    cam_data.lens = focal_length
    
    # Cinematic Viewport & Render Settings
    cam_data.show_passepartout = True
    cam_data.passepartout_alpha = 0.95
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target_obj
    cam_data.dof.aperture_fstop = 2.8
    
    cam_obj = bpy.data.objects.new(name=object_name, object_data=cam_data)
    scene.collection.objects.link(cam_obj)

    # Clear unneeded local transforms (driven by constraints)
    cam_obj.location = (0, 0, 0)
    cam_obj.rotation_euler = (0, 0, 0)

    # === Step 4: Setup Camera Constraints ===
    # 4a. Follow Path Constraint
    cst_path = cam_obj.constraints.new(type='FOLLOW_PATH')
    cst_path.target = path_obj
    cst_path.use_curve_follow = True
    cst_path.forward_axis = 'TRACK_NEGATIVE_Z'
    cst_path.up_axis = 'UP_Y'
    cst_path.use_fixed_location = True # Enables offset factor animation

    # 4b. Track To Constraint (Look-at behavior)
    cst_track = cam_obj.constraints.new(type='TRACK_TO')
    cst_track.target = target_obj
    cst_track.track_axis = 'TRACK_NEGATIVE_Z'
    cst_track.up_axis = 'UP_Y'

    # === Step 5: Animate the Rig ===
    # Insert start and end keyframes
    cst_path.offset_factor = 0.0
    cst_path.keyframe_insert(data_path="offset_factor", frame=1)
    
    cst_path.offset_factor = 1.0
    cst_path.keyframe_insert(data_path="offset_factor", frame=duration_frames)

    # Force LINEAR interpolation for smooth, continuous dolly movement
    if cam_obj.animation_data and cam_obj.animation_data.action:
        for fcurve in cam_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    # Make this rig the active scene camera
    scene.camera = cam_obj

    return f"Created Cinematic Camera Rig '{object_name}' (Lens: {focal_length}mm) following track '{path_obj.name}' and focused on '{target_obj.name}'"

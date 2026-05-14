def create_object(
    scene_name: str = "Scene",
    object_name: str = "OrbitCamera",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0),
    **kwargs,
) -> str:
    """
    Create a Procedural Camera Orbit setup.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the camera and path setup.
        location: (x, y, z) focal point the camera will orbit and look at.
        scale: Multiplier for the orbit radius.
        material_color: Unused (kept for signature compatibility).
        **kwargs: 
            path_radius (float): Base radius of the circular path.
            path_height (float): Z-axis elevation of the camera.
            orbit_frames (int): Duration of the 360-degree loop in frames.

    Returns:
        Status string describing the generated rig.
    """
    import bpy
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Extract kwargs with defaults
    path_radius = kwargs.get("path_radius", 5.0)
    path_height = kwargs.get("path_height", 2.0)
    orbit_frames = kwargs.get("orbit_frames", 150)
    
    actual_radius = path_radius * scale
    
    # Ensure we are in object mode before adding primitives
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # === Step 1: Create Focal Target (Empty) ===
    target_name = f"{object_name}_Target"
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
    target_obj = bpy.context.active_object
    target_obj.name = target_name
    
    # === Step 2: Create Orbit Path (Bezier Circle) ===
    path_name = f"{object_name}_Path"
    path_loc = (location[0], location[1], location[2] + path_height)
    bpy.ops.curve.primitive_bezier_circle_add(
        radius=actual_radius, 
        align='WORLD', 
        location=path_loc
    )
    path_obj = bpy.context.active_object
    path_obj.name = path_name
    
    # === Step 3: Create Camera ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Data")
    cam_obj = bpy.data.objects.new(name=object_name, object_data=cam_data)
    scene.collection.objects.link(cam_obj)
    
    # Zero out transforms so constraints dictate position/rotation entirely
    cam_obj.location = (0.0, 0.0, 0.0)
    cam_obj.rotation_euler = (0.0, 0.0, 0.0)
    
    # === Step 4: Setup Constraints ===
    # 1. Follow Path
    follow_const = cam_obj.constraints.new(type='FOLLOW_PATH')
    follow_const.target = path_obj
    follow_const.use_curve_follow = False # Let Track To handle orientation
    
    # 2. Track To
    track_const = cam_obj.constraints.new(type='TRACK_TO')
    track_const.target = target_obj
    track_const.track_axis = 'TRACK_NEGATIVE_Z'  # Camera looks out of -Z
    track_const.up_axis = 'UP_Y'                 # Camera up is Y
    
    # === Step 5: Animate the Loop ===
    # Insert keyframes for the Follow Path offset
    follow_const.offset_factor = 0.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=1)
    
    follow_const.offset_factor = 1.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=orbit_frames + 1) # +1 so frame 1 and end aren't identical (prevents stutter in loops)
    
    # Force Linear interpolation for constant rotation speed
    if cam_obj.animation_data and cam_obj.animation_data.action:
        for fcurve in cam_obj.animation_data.action.fcurves:
            if "offset_factor" in fcurve.data_path:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                    
    # Optional: Update scene timeline to match
    scene.frame_start = 1
    scene.frame_end = orbit_frames
    
    # Deselect all and select the camera
    bpy.ops.object.select_all(action='DESELECT')
    cam_obj.select_set(True)
    bpy.context.view_layer.objects.active = cam_obj

    return f"Created '{object_name}' setup: looping orbital camera at radius {actual_radius:.2f}, tracking {location} over {orbit_frames} frames."

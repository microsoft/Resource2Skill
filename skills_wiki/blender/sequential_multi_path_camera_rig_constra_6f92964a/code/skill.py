def create_object(
    scene_name: str = "Scene",
    object_name: str = "MultiPathCameraRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Sequential Multi-Path Camera Rig in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created rig objects.
        location: (x, y, z) world-space position (center point of the rig).
        scale: Uniform scale factor for the camera paths.
        material_color: Ignored for rig creation, kept for standard signature.
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the creation of the rig.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)
    
    # Ensure playhead is at frame 1 for clean setup
    scene.frame_set(1)

    # === Step 1: Create Tracking Target (Subject) ===
    bpy.ops.object.empty_add(type='CUBE', radius=scale * 0.5, location=base_loc)
    subject = bpy.context.active_object
    subject.name = f"{object_name}_Target"

    # === Step 2: Create Camera Paths ===
    # Path 1 (e.g., Left sweeping arc)
    bpy.ops.curve.primitive_bezier_circle_add(
        radius=5 * scale, 
        location=base_loc + Vector((-5 * scale, 0, 2 * scale))
    )
    path1 = bpy.context.active_object
    path1.name = f"{object_name}_Path1"
    
    # Path 2 (e.g., Right sweeping arc)
    bpy.ops.curve.primitive_bezier_circle_add(
        radius=8 * scale, 
        location=base_loc + Vector((5 * scale, 4 * scale, 4 * scale))
    )
    path2 = bpy.context.active_object
    path2.name = f"{object_name}_Path2"
    # Tilt Path 2 slightly for dynamic motion
    path2.rotation_euler[0] = 0.5

    # === Step 3: Create Camera ===
    # Start at origin relative to rig so constraints dictate actual world space
    bpy.ops.object.camera_add(location=base_loc)
    cam = bpy.context.active_object
    cam.name = f"{object_name}_Camera"

    # === Step 4: Add & Configure Constraints ===
    
    # Constraint 1: Follow Path 1
    con_path1 = cam.constraints.new(type='FOLLOW_PATH')
    con_path1.name = "Follow Path 1"
    con_path1.target = path1
    con_path1.use_fixed_location = True # Corresponds to UI "Fixed Position"
    
    # Constraint 2: Follow Path 2
    con_path2 = cam.constraints.new(type='FOLLOW_PATH')
    con_path2.name = "Follow Path 2"
    con_path2.target = path2
    con_path2.use_fixed_location = True
    con_path2.influence = 0.0 # Disabled initially
    
    # Constraint 3: Track To Subject
    con_track = cam.constraints.new(type='TRACK_TO')
    con_track.name = "Track Subject"
    con_track.target = subject
    con_track.track_axis = 'TRACK_NEGATIVE_Z'
    con_track.up_axis = 'UP_Y'

    # === Step 5: Keyframe Animation Pipeline ===
    
    # 1. Drive Path 1 (Frames 1 to 100)
    con_path1.offset_factor = 0.0
    con_path1.keyframe_insert(data_path="offset_factor", frame=1)
    con_path1.offset_factor = 1.0
    con_path1.keyframe_insert(data_path="offset_factor", frame=100)
    
    # 2. Drive Path 2 (Frames 100 to 200)
    con_path2.offset_factor = 0.0
    con_path2.keyframe_insert(data_path="offset_factor", frame=100)
    con_path2.offset_factor = 1.0
    con_path2.keyframe_insert(data_path="offset_factor", frame=200)
    
    # 3. Crossfade Influence smoothly (Frames 100 to 150)
    # Path 1 fading out
    con_path1.influence = 1.0
    con_path1.keyframe_insert(data_path="influence", frame=100)
    con_path1.influence = 0.0
    con_path1.keyframe_insert(data_path="influence", frame=150)
    
    # Path 2 fading in
    con_path2.influence = 0.0
    con_path2.keyframe_insert(data_path="influence", frame=100)
    con_path2.influence = 1.0
    con_path2.keyframe_insert(data_path="influence", frame=150)

    # Set timeline range to view the full effect
    scene.frame_start = 1
    scene.frame_end = 200

    return f"Created '{object_name}' rig at {location}. Press SPACE to play 200-frame crossfaded camera tracking animation."

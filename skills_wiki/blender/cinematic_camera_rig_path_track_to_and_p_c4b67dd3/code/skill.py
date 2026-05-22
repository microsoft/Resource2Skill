def create_cinematic_camera_rig(
    scene_name: str = "Scene",
    object_name: str = "CinematicRig",
    location: tuple = (0.0, 0.0, 0.0),
    target_location: tuple = (0.0, 0.0, 1.0),
    path_radius: float = 8.0,
    shake_intensity: float = 0.02,
    **kwargs,
) -> str:
    """
    Create a constraint-based camera rig with smooth path movement, 
    automatic target tracking, and procedural handheld shake.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig objects.
        location: (x, y, z) center position for the camera path orbit.
        target_location: (x, y, z) point the camera will always look at and focus on.
        path_radius: Size of the circular path curve.
        shake_intensity: Amplitude of the procedural camera shake (in radians).
        **kwargs: Additional parameters (e.g., duration_frames).

    Returns:
        Status string describing the created rig.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection
    
    duration_frames = kwargs.get('duration_frames', 250)

    # === Step 1: Create the Target Empty ===
    target_name = f"{object_name}_Target"
    target = bpy.data.objects.new(target_name, None)
    target.empty_display_type = 'CROSS'
    target.empty_display_size = 1.0
    target.location = target_location
    collection.objects.link(target)

    # === Step 2: Create the Circular Bezier Path ===
    curve_data = bpy.data.curves.new(f"{object_name}_PathData", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 24
    
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(3) # Adds 3 to the existing 1, total 4 points
    
    # Mathematically construct a perfect circle
    kappa = 0.552284749831 # Constant for circular bezier handles
    for i in range(4):
        angle = i * (math.pi / 2)
        x = math.cos(angle) * path_radius
        y = math.sin(angle) * path_radius
        
        pt = spline.bezier_points[i]
        pt.co = (x, y, 0)
        
        tx = -math.sin(angle) * path_radius * kappa
        ty = math.cos(angle) * path_radius * kappa
        
        pt.handle_left = (x - tx, y - ty, 0)
        pt.handle_right = (x + tx, y + ty, 0)
        pt.handle_left_type = 'ALIGNED'
        pt.handle_right_type = 'ALIGNED'
        
    spline.use_cyclic_u = True
    
    path_obj = bpy.data.objects.new(f"{object_name}_Path", curve_data)
    path_obj.location = location
    collection.objects.link(path_obj)

    # === Step 3: Create the Gimbal Empty ===
    # The Gimbal handles the constraints so the Camera remains free for shake offsets
    gimbal_name = f"{object_name}_Gimbal"
    gimbal = bpy.data.objects.new(gimbal_name, None)
    gimbal.empty_display_type = 'ARROWS'
    gimbal.empty_display_size = 0.5
    collection.objects.link(gimbal)
    
    # Follow Path Constraint
    follow_path = gimbal.constraints.new(type='FOLLOW_PATH')
    follow_path.target = path_obj
    follow_path.use_fixed_location = True
    
    # Track To Constraint
    track_to = gimbal.constraints.new(type='TRACK_TO')
    track_to.target = target
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'
    
    # Animate Gimbal along the path with ease-in/ease-out (Bezier)
    gimbal.animation_data_create()
    gimbal_action = bpy.data.actions.new(name=f"{object_name}_GimbalAnim")
    gimbal.animation_data.action = gimbal_action
    
    fcu_path = gimbal_action.fcurves.new(data_path=f'constraints["{follow_path.name}"].offset_factor')
    kp1 = fcu_path.keyframe_points.insert(1, 0.0)
    kp2 = fcu_path.keyframe_points.insert(duration_frames, 1.0)
    kp1.interpolation = 'BEZIER'
    kp2.interpolation = 'BEZIER'

    # === Step 4: Create the Camera ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_CamData")
    cam_data.lens = 50 # Standard 50mm focal length
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target
    cam_data.dof.aperture_fstop = 2.8
    
    cam_obj = bpy.data.objects.new(object_name, cam_data)
    cam_obj.parent = gimbal
    cam_obj.location = (0, 0, 0)
    cam_obj.rotation_euler = (0, 0, 0)
    collection.objects.link(cam_obj)
    
    # === Step 5: Add Procedural Camera Shake ===
    if shake_intensity > 0:
        cam_obj.animation_data_create()
        cam_action = bpy.data.actions.new(name=f"{object_name}_Shake")
        cam_obj.animation_data.action = cam_action
        
        # Apply independent noise modifiers to X, Y, and Z rotation
        for i in range(3):
            fcu = cam_action.fcurves.new(data_path="rotation_euler", index=i)
            # Insert baseline keyframe to anchor the noise modifier
            fcu.keyframe_points.insert(1, 0.0)
            
            mod = fcu.modifiers.new(type='NOISE')
            mod.scale = 15.0  # Frequency (lower = faster shake)
            mod.strength = shake_intensity # Amplitude in radians
            mod.phase = i * 1000.0 # Phase offset so axes shake independently
            mod.depth = 2

    # Make the camera the active scene camera
    scene.camera = cam_obj

    return f"Created Cinematic Rig '{object_name}': Target at {target_location}, Path radius {path_radius}, Duration {duration_frames}f."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "HandheldCamera",
    location: tuple = (0.0, -8.0, 1.5),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for cameras
    **kwargs,
) -> str:
    """
    Create a Cinematic Handheld Tracking Camera Rig in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the camera rig.
        location: (x, y, z) world-space position of the camera.
        scale: Unused for cameras.
        material_color: Unused for cameras.
        **kwargs: 
            target_location (tuple): Where the camera should look. Default (0, 0, 1).
            shake_strength (float): Intensity of the handheld shake. Default 0.05.
            shake_scale (float): Speed of the shake (higher = slower). Default 20.0.
            focal_length (float): Lens focal length in mm. Default 35.0.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Parse kwargs
    target_loc = kwargs.get('target_location', (0.0, 0.0, 1.0))
    shake_strength = kwargs.get('shake_strength', 0.025)
    shake_scale = kwargs.get('shake_scale', 25.0)
    focal_length = kwargs.get('focal_length', 35.0)

    # === Step 1: Create the Target Empty ===
    bpy.ops.object.empty_add(type='SPHERE', radius=0.2, location=target_loc)
    target_empty = bpy.context.active_object
    target_empty.name = f"{object_name}_Target"
    
    if scene.collection:
        # Link is handled by op, but ensure it's organized
        pass

    # === Step 2: Create the Gimbal Empty (Handles Tracking) ===
    bpy.ops.object.empty_add(type='ARROWS', radius=0.5, location=location)
    gimbal_empty = bpy.context.active_object
    gimbal_empty.name = f"{object_name}_Gimbal"

    # Add Track To Constraint to Gimbal
    track_constraint = gimbal_empty.constraints.new(type='TRACK_TO')
    track_constraint.target = target_empty
    track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_constraint.up_axis = 'UP_Y'

    # === Step 3: Create the Camera ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Data")
    cam_data.lens = focal_length
    
    # Optional: Setup Depth of Field pointing at target
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target_empty
    cam_data.dof.aperture_fstop = 2.8

    camera_obj = bpy.data.objects.new(object_name, cam_data)
    scene.collection.objects.link(camera_obj)
    
    camera_obj.location = location
    # Parent Camera to Gimbal (Zeroes out local transform so it perfectly follows the gimbal)
    camera_obj.parent = gimbal_empty
    camera_obj.matrix_parent_inverse = gimbal_empty.matrix_world.inverted()
    camera_obj.location = (0, 0, 0)
    camera_obj.rotation_euler = (0, 0, 0)

    # === Step 4: Add Procedural Handheld Shake (Graph Editor Noise) ===
    # We must insert a dummy keyframe so animation data/fcurves exist to apply modifiers to
    camera_obj.keyframe_insert(data_path="rotation_euler", frame=1)

    if camera_obj.animation_data and camera_obj.animation_data.action:
        for fcurve in camera_obj.animation_data.action.fcurves:
            if fcurve.data_path == "rotation_euler":
                # Add Noise Modifier
                noise_mod = fcurve.modifiers.new(type='NOISE')
                noise_mod.scale = shake_scale
                noise_mod.strength = shake_strength
                
                # Offset phase based on axis (array_index 0=X, 1=Y, 2=Z)
                # This prevents the camera from shaking in a perfect diagonal line
                noise_mod.phase = fcurve.array_index * 123.45
                
                # Blend in/out can be set, but we leave it infinitely running
                noise_mod.blend_type = 'REPLACE'

    # Ensure view layer updates to evaluate constraints
    bpy.context.view_layer.update()

    return f"Created '{object_name}' rig at {location} tracking target at {target_loc} with procedural handheld shake."

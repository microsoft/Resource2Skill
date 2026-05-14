def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for camera, kept for signature
    **kwargs,
) -> str:
    """
    Create a Professional Cinematic Camera Rig in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the rig collection and base object prefixes.
        location: (x, y, z) world-space position for the rig center.
        scale: Uniform scale factor for the dolly track radius and empties.
        material_color: Unused.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Organizational Setup ===
    # Create a dedicated collection for the rig to make it easily appendable
    rig_collection = bpy.data.collections.new(object_name)
    scene.collection.children.link(rig_collection)

    def link_to_rig(obj):
        """Helper to move an object from active collection to the rig collection."""
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        rig_collection.objects.link(obj)

    # === Step 2: Track & Empties ===
    
    # 2a. Create the Dolly Track (Path)
    bpy.ops.curve.primitive_bezier_circle_add(radius=5.0 * scale, location=location)
    path_obj = bpy.context.active_object
    path_obj.name = f"{object_name}_DollyTrack"
    path_obj.data.use_path = True
    link_to_rig(path_obj)

    # 2b. Create the Focal Target (FT) Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    ft_empty = bpy.context.active_object
    ft_empty.name = f"{object_name}_FocalTarget_FT"
    link_to_rig(ft_empty)

    # 2c. Create the Focus Point (FP) Empty (Controls Depth of Field)
    # Positioned slightly offset so it doesn't perfectly overlap FT immediately
    fp_loc = (location[0], location[1] - (2.0 * scale), location[2])
    bpy.ops.object.empty_add(type='SPHERE', location=fp_loc)
    fp_empty = bpy.context.active_object
    fp_empty.name = f"{object_name}_FocusPoint_FP"
    fp_empty.scale = (0.5 * scale, 0.5 * scale, 0.5 * scale)
    link_to_rig(fp_empty)

    # FP Constraint: Copies FT location but allows relative offset sliding
    fp_const = fp_empty.constraints.new('COPY_LOCATION')
    fp_const.target = ft_empty
    fp_const.use_offset = True

    # === Step 3: Camera Setup ===
    
    # Must be instantiated at 0,0,0 so it sits perfectly on the path curve
    bpy.ops.object.camera_add(location=(0, 0, 0)) 
    cam_obj = bpy.context.active_object
    cam_obj.name = f"{object_name}_Camera"
    link_to_rig(cam_obj)

    # Camera Properties
    cam_data = cam_obj.data
    cam_data.lens = 50.0  # 50mm focal length
    cam_data.show_limits = True
    cam_data.show_name = True
    cam_data.passepartout_alpha = 1.0 # Black out off-screen geometry

    # Depth of Field Config
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = fp_empty
    cam_data.dof.aperture_fstop = 2.8

    # === Step 4: Camera Constraints (Order of Operations is Critical) ===
    
    # Constraint 1: Follow Path (Calculated first)
    path_const = cam_obj.constraints.new('FOLLOW_PATH')
    path_const.target = path_obj
    path_const.use_curve_follow = True
    path_const.forward_axis = 'FORWARD_Y'
    path_const.up_axis = 'UP_Z'

    # Constraint 2: Damped Track (Calculated second, pivoting the camera inward)
    track_const = cam_obj.constraints.new('DAMPED_TRACK')
    track_const.target = ft_empty
    track_const.track_axis = 'TRACK_NEGATIVE_Z'

    # Clean selection state
    bpy.ops.object.select_all(action='DESELECT')
    cam_obj.select_set(True)
    bpy.context.view_layer.objects.active = cam_obj

    return f"Created '{object_name}' rig collection at {location} containing Camera, DollyTrack, and Focus Empties."

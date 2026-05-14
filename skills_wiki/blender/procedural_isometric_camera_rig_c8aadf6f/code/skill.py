def create_object(
    scene_name: str = "Scene",
    object_name: str = "IsometricCamera",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 15.0,  # Repurposed to control 'Ortho Scale' (Zoom)
    material_color: tuple = (0.8, 0.2, 0.1), # Unused for camera, kept for signature
    **kwargs,
) -> str:
    """
    Create a mathematically perfect Isometric Camera rig in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the camera and target objects.
        location: The (x, y, z) focus point the camera will look at.
        scale: Sets the Orthographic Scale (determines how "zoomed in" the view is).
        material_color: Unused.
        **kwargs: 
            distance (float): Physical distance of the camera from the target.
            make_active (bool): Whether to set this as the scene's active rendering camera.
            
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection
    
    # === Step 1: Create the Target Empty (Focus Point) ===
    target_name = f"{object_name}_Target"
    
    # Handle duplicate naming safely
    if target_name in bpy.data.objects:
        target_name = f"{target_name}_new"
        
    target_empty = bpy.data.objects.new(target_name, None)
    target_empty.empty_display_size = 2.0
    target_empty.empty_display_type = 'CROSS'
    target_empty.location = Vector(location)
    collection.objects.link(target_empty)
    
    # === Step 2: Create the Orthographic Camera ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Data")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = scale  # Controls framing / zoom
    
    cam_obj = bpy.data.objects.new(object_name, cam_data)
    
    # Calculate True Isometric Position:
    # A vector where X, Y, and Z magnitudes are equal creates the perfect isometric angle.
    # Standard orientation looks from the Bottom-Right-Front (-Y axis is "Front" in Blender).
    distance = kwargs.get('distance', 25.0)
    iso_offset = Vector((distance, -distance, distance))
    
    cam_obj.location = target_empty.location + iso_offset
    collection.objects.link(cam_obj)
    
    # === Step 3: Apply the Rigging Constraints ===
    track_const = cam_obj.constraints.new(type='TRACK_TO')
    track_const.target = target_empty
    track_const.track_axis = 'TRACK_NEGATIVE_Z'
    track_const.up_axis = 'UP_Y'
    
    # === Step 4: Finalize ===
    # Optionally make it the active camera
    make_active = kwargs.get('make_active', True)
    if make_active:
        scene.camera = cam_obj
        
    return f"Created Isometric Camera Rig '{object_name}' focused at {location} with Ortho Scale {scale}."

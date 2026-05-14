def create_object(
    scene_name: str = "Scene",
    object_name: str = "AnimatedSlider",
    location: tuple = (0, 0, 1),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create Basic Looping Transform Animation in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space starting position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides (loop_duration, move_axis, move_distance).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # === Step 4: Animation / Keyframes ===
    # Retrieve optional animation parameters from kwargs or use defaults
    loop_duration = kwargs.get("loop_duration", 48)  # 48 frames = 2 seconds at 24fps
    move_axis = kwargs.get("move_axis", 0)           # 0 for X, 1 for Y, 2 for Z
    move_distance = kwargs.get("move_distance", 5.0)

    start_frame = 1
    mid_frame = start_frame + (loop_duration // 2)
    end_frame = start_frame + loop_duration

    # 1. Start Keyframe (Initial Position)
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # 2. Mid Keyframe (Offset Position)
    obj.location[move_axis] += move_distance
    obj.keyframe_insert(data_path="location", frame=mid_frame)

    # 3. End Keyframe (Back to Initial Position to create a seamless loop)
    obj.location[move_axis] -= move_distance
    obj.keyframe_insert(data_path="location", frame=end_frame)
    
    # Ensure the scene timeline is at least long enough to show the full loop
    if scene.frame_end < end_frame:
        scene.frame_end = end_frame
        
    # Link object to the correct scene collection if not already
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created '{object_name}' at {location} with a {loop_duration}-frame looping animation on axis {move_axis}."

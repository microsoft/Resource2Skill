def create_animated_object(
    scene_name: str = "Scene",
    object_name: str = "AnimatedCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.5, 0.8),
    start_frame: int = 1,
    end_frame: int = 60,
    move_distance: float = 5.0,
    **kwargs,
) -> str:
    """
    Create an animated object demonstrating keyframes, Bezier interpolation, 
    and custom Graph Editor handle adjustments.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) starting world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        start_frame: Frame where animation begins.
        end_frame: Frame where animation stops.
        move_distance: Distance to travel along the X axis.

    Returns:
        Status string describing the created animation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
    obj.data.materials.append(mat)

    # === Step 3: Animation & Keyframing ===
    # Ensure animation data and action exist
    if not obj.animation_data:
        obj.animation_data_create()
    action = bpy.data.actions.new(name=f"{object_name}_Action")
    obj.animation_data.action = action

    # Keyframe 1: Start State
    obj.location = Vector(location)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (scale, scale, scale)
    
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Keyframe 2: End State (Moved, rotated, and scaled)
    obj.location = Vector(location) + Vector((move_distance, 0.0, 0.0))
    obj.rotation_euler = (math.pi / 2, 0.0, math.pi) # Rotate to make movement obvious
    obj.scale = (scale * 1.5, scale * 1.5, scale * 1.5)
    
    obj.keyframe_insert(data_path="location", frame=end_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)
    obj.keyframe_insert(data_path="scale", frame=end_frame)

    # === Step 4: Graph Editor / Interpolation Adjustments ===
    for fcurve in action.fcurves:
        for kf in fcurve.keyframe_points:
            # Set default interpolation to smooth ease-in/ease-out
            kf.interpolation = 'BEZIER'

        # Replicate a "sharp stop" effect by modifying the X-location curve handles
        if fcurve.data_path == "location" and fcurve.array_index == 0:
            start_kf = fcurve.keyframe_points[0]
            end_kf = fcurve.keyframe_points[-1]
            
            # Make the end keyframe handle 'FREE' so we can manipulate it
            end_kf.handle_left_type = 'FREE'
            
            # Flatten the left handle of the end keyframe to create a sudden, harsh stop
            # rather than a gradual deceleration
            end_kf.handle_left.y = end_kf.co.y
            end_kf.handle_left.x = end_kf.co.x - (end_frame - start_frame) * 0.1

    # Ensure the scene plays long enough to see the animation
    if scene.frame_end < end_frame + 20:
        scene.frame_end = end_frame + 20

    return f"Created animated '{object_name}' at {location}. Animation spans frames {start_frame}-{end_frame} with Bezier easing."

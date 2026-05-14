def create_object(
    scene_name: str = "Scene",
    object_name: str = "BlockingPlus_Ball",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.1, 0.2),
    **kwargs,
) -> str:
    """
    Create a Bouncing Ball demonstrating the "Blocking Plus" animation workflow.
    
    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space base position.
        scale: Uniform scale factor for the ball and its bounce height.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
    ball = bpy.context.active_object
    ball.name = object_name
    
    # Store base location to offset the animation correctly in world space
    base_loc = Vector(location)
    
    # Smooth the geometry
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3
    ball.data.materials.append(mat)

    # === Step 3: Animation (Blocking Plus Workflow) ===
    # Instead of just keying the start, middle, and end, we add "Blocking Plus" 
    # breakdown frames to dictate the weight, hang time, and velocity to the computer.
    
    def insert_pose(frame: int, z_offset: float, scale_vec: tuple):
        # Apply base location + animated Z offset
        ball.location = base_loc + Vector((0, 0, z_offset * scale))
        # Apply base scale * animated squash/stretch scale
        ball.scale = (scale_vec[0] * scale, scale_vec[1] * scale, scale_vec[2] * scale)
        
        # Insert keyframes
        ball.keyframe_insert(data_path="location", index=2, frame=frame)
        ball.keyframe_insert(data_path="scale", frame=frame)

    # -- Primary Blocking Keys (The bare minimum) --
    # Peak (Start)
    insert_pose(1,  5.0, (1.0, 1.0, 1.0))
    # Contact (Squash on the floor)
    insert_pose(10, 0.5, (1.3, 1.3, 0.5))
    # Peak (End)
    insert_pose(20, 5.0, (1.0, 1.0, 1.0))

    # -- Blocking Plus Breakdown Keys (The secret sauce) --
    # Hang time (Gravity slow-down near the top) - Only falls 0.5 units in 4 frames
    insert_pose(5,  4.5, (1.0, 1.0, 1.0))
    
    # Stretch (Max velocity right before hit) - Falls 3.4 units in 4 frames
    insert_pose(9,  1.1, (0.8, 0.8, 1.2))
    
    # Stretch (Max velocity right after hit)
    insert_pose(11, 1.1, (0.8, 0.8, 1.2))
    
    # Hang time (Gravity slow-down approaching top)
    insert_pose(16, 4.5, (1.0, 1.0, 1.0))

    # === Step 4: Splining ===
    # Set interpolation to BEZIER.
    # Because we added Blocking Plus keys, the Bezier interpolation will look 
    # snappy and physical automatically, avoiding the dreaded "spline float".
    if ball.animation_data and ball.animation_data.action:
        for fcurve in ball.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'

    # Set scene frame range to loop nicely around the animation
    scene.frame_start = 1
    scene.frame_end = 20

    return f"Created animated '{object_name}' at {location} demonstrating the Blocking Plus workflow."

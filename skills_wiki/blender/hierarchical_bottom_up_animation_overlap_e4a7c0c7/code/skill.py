def create_object(
    scene_name: str = "Scene",
    object_name: str = "AnimHierarchy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.5, 0.8),
    **kwargs,
) -> str:
    """
    Create a hierarchical kinematic chain demonstrating the 
    Blocking -> Splining workflow with procedural overlap animation.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position of the Root COG.
        scale: Uniform scale factor for the hierarchy thickness/length.
        material_color: (R, G, B) base color for the root object.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Materials ===
    mat_root = bpy.data.materials.new(name=f"{object_name}_MatRoot")
    mat_root.use_nodes = True
    if mat_root.node_tree:
        mat_root.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*material_color, 1.0)

    mat_child = bpy.data.materials.new(name=f"{object_name}_MatChild")
    mat_child.use_nodes = True
    if mat_child.node_tree:
        mat_child.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.2, 0.1, 1.0)

    # === Step 2: Build FK Hierarchy ===
    parts = []
    num_segments = 4
    segment_height = 2.0 * scale
    thickness = 0.5 * scale

    for i in range(num_segments):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_Seg_{i}"

        # Shift origin to bottom and scale vertices to avoid Object-level scale inheritance issues
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        for v in bm.verts:
            v.co.z += 0.5  # Shift origin to the absolute bottom
            v.co.x *= thickness
            v.co.y *= thickness
            v.co.z *= segment_height
        bm.to_mesh(obj.data)
        bm.free()

        # Parent and Position
        if i == 0:
            obj.location = Vector(location)
            obj.data.materials.append(mat_root)
        else:
            parent = parts[i - 1]
            obj.parent = parent
            obj.location = (0, 0, segment_height)  # Local space offset exactly to top of parent
            obj.data.materials.append(mat_child)

        parts.append(obj)

    # === Step 3: Animation (Root-First & Overlap) ===
    root = parts[0]
    
    # Ensure scene has enough timeline duration to see the effect
    scene.frame_start = 1
    scene.frame_end = 80

    # 3a. Animate COG/Root (The driving force)
    root.keyframe_insert(data_path="location", frame=1)
    root.keyframe_insert(data_path="rotation_euler", frame=1)

    root.location = Vector(location) + Vector((0, 5 * scale, 0))
    root.rotation_euler = (math.radians(-25), 0, 0)
    root.keyframe_insert(data_path="location", frame=15)
    root.keyframe_insert(data_path="rotation_euler", frame=15)

    root.rotation_euler = (0, 0, 0)
    root.keyframe_insert(data_path="rotation_euler", frame=30)

    # 3b. Animate Children (The follow-through / overlap)
    frame_delay = 4 # Stagger keys down the chain

    for i in range(1, num_segments):
        seg = parts[i]
        offset = i * frame_delay
        
        # Start neutral
        seg.keyframe_insert(data_path="rotation_euler", frame=1)
        
        # Drag backwards as root moves forward
        seg.rotation_euler = (math.radians(-35), 0, 0)
        seg.keyframe_insert(data_path="rotation_euler", frame=10 + offset)
        
        # Whip forward as root stops
        seg.rotation_euler = (math.radians(45), 0, 0)
        seg.keyframe_insert(data_path="rotation_euler", frame=22 + offset)
        
        # Overcorrect backwards
        seg.rotation_euler = (math.radians(-15), 0, 0)
        seg.keyframe_insert(data_path="rotation_euler", frame=35 + offset)
        
        # Settle to rest
        seg.rotation_euler = (0, 0, 0)
        seg.keyframe_insert(data_path="rotation_euler", frame=50 + offset)

    # === Step 4: The "Splining" Phase ===
    # Convert all generated keyframes to smooth Bezier curves to finalize mechanical tests
    for obj in parts:
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'
                    keyframe.easing = 'AUTO'

    return f"Created anim hierarchy '{object_name}' with {num_segments} splined segments."

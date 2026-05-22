def create_object(
    scene_name: str = "Scene",
    object_name: str = "AnimWorkflow_Demo",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),  # Unused, overridden by semantic colors
    **kwargs,
) -> str:
    """
    Creates a visual comparison demonstrating the 'Dense Data' animation workflow.
    Generates two arms: a red one animated with sparse keys (floaty), 
    and a green one animated with dense keys (snappy with anticipation/settle).

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Ignored in favor of red/green comparison colors.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create a procedural pivoting arm
    def create_arm(name, offset_loc, color):
        mesh = bpy.data.meshes.new(name=f"{name}_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        
        # Build simple arm geometry using bmesh
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale into an arm shape and offset so the origin (pivot) is at the base
        for v in bm.verts:
            v.co.x *= 0.2
            v.co.z *= 0.2
            v.co.y = (v.co.y + 0.5) * 2.0 # Length of 2, extending along +Y
            
        bm.to_mesh(mesh)
        bm.free()
        
        obj.location = Vector(location) + Vector(offset_loc)
        obj.scale = (scale, scale, scale)
        
        # Assign Material
        mat = bpy.data.materials.new(name=f"{name}_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        obj.data.materials.append(mat)
        
        return obj

    # ==========================================
    # Example 1: SPARSE DATA (The "Floaty Spline" Mistake)
    # ==========================================
    sparse_obj = create_arm(f"{object_name}_Sparse_Bad", (-1 * scale, 0, 0), (0.8, 0.1, 0.1))
    sparse_obj.animation_data_create()
    sparse_action = bpy.data.actions.new(name=f"{sparse_obj.name}_Action")
    sparse_obj.animation_data.action = sparse_action
    
    # Animate Z rotation
    fcurve_sparse = sparse_action.fcurves.new(data_path="rotation_euler", index=2)
    
    # Only A to B keys - software decides the in-betweens (results in lifeless ease)
    sparse_keys = [
        (20, 0), 
        (46, 90)
    ]
    
    for f, ang in sparse_keys:
        kf = fcurve_sparse.keyframe_points.insert(f, math.radians(ang))
        kf.interpolation = 'BEZIER'

    # ==========================================
    # Example 2: DENSE DATA (The "Stepped to Spline" Solution)
    # ==========================================
    dense_obj = create_arm(f"{object_name}_Dense_Good", (1 * scale, 0, 0), (0.1, 0.8, 0.2))
    dense_obj.animation_data_create()
    dense_action = bpy.data.actions.new(name=f"{dense_obj.name}_Action")
    dense_obj.animation_data.action = dense_action
    
    # Animate Z rotation
    fcurve_dense = dense_action.fcurves.new(data_path="rotation_euler", index=2)
    
    # Dense keys defining weight, physics, and intent
    dense_keys = [
        (20, 0),     # Start
        (26, -15),   # Anticipation
        (30, -15),   # Hold anticipation to build energy
        (34, 105),   # Breakdown / Overshoot (fastest part of motion)
        (38, 85),    # Settle rebound
        (42, 92),    # Micro settle
        (46, 90)     # Final rest pose
    ]
    
    for f, ang in dense_keys:
        kf = fcurve_dense.keyframe_points.insert(f, math.radians(ang))
        kf.interpolation = 'BEZIER'
        
    # Ensure timeline allows viewing the animation
    scene.frame_start = 1
    scene.frame_end = 80
    
    return f"Created comparison objects '{sparse_obj.name}' (Red) and '{dense_obj.name}' (Green) at {location}. Press Play (Spacebar) to observe the animation data density difference."

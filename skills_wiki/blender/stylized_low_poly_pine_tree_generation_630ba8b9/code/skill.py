def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the pine needles.
        **kwargs: Additional overrides (e.g., num_layers).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    num_layers = kwargs.get("num_layers", 4)

    # === Step 1: Initialize BMesh ===
    bm = bmesh.new()

    # === Step 2: Create Trunk ===
    trunk_geom = bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=8,
        radius1=0.2 * scale,
        radius2=0.15 * scale,
        depth=1.0 * scale
    )
    
    # create_cone centers depth at 0. Shift it so base is at Z=0
    trunk_verts = trunk_geom['verts']
    bmesh.ops.translate(bm, vec=Vector((0, 0, 0.5 * scale)), verts=trunk_verts)
    
    # Assign Material Index 0 (Trunk) to all current faces
    for f in bm.faces:
        f.material_index = 0

    # === Step 3: Create Leaf Layers ===
    base_radius = 0.8 * scale
    layer_height = 1.2 * scale
    
    for i in range(num_layers):
        # Taper the radius as we go up
        factor = 1.0 - (i / (num_layers + 1))
        current_radius = base_radius * factor
        
        # Save current face count to assign material indices later
        start_face_count = len(bm.faces)
        
        layer_geom = bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=10,
            radius1=current_radius,
            radius2=0.02 * scale, # Tapered top
            depth=layer_height
        )
        
        layer_verts = layer_geom['verts']
        
        # 3a. Shift cone so its base is at the origin (for proper rotation pivoting)
        bmesh.ops.translate(bm, vec=Vector((0, 0, layer_height / 2)), verts=layer_verts)
        
        # 3b. Calculate slight organic rotation
        rot_x = math.radians(8 * (i % 2 - 0.5))
        rot_y = math.radians(8 * ((i + 1) % 2 - 0.5))
        rot_z = math.radians(45 * i) # Twist each layer
        rot_matrix = Euler((rot_x, rot_y, rot_z), 'XYZ').to_matrix()
        
        # Apply rotation around the base
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_matrix, verts=layer_verts)
        
        # 3c. Translate to proper height on the trunk
        z_pos = (0.6 + i * 0.5) * scale
        bmesh.ops.translate(bm, vec=Vector((0, 0, z_pos)), verts=layer_verts)
        
        # 3d. Assign Material Index 1 (Leaves) to new faces
        bm.faces.ensure_lookup_table()
        for f_idx in range(start_face_count, len(bm.faces)):
            bm.faces[f_idx].material_index = 1

    # === Step 4: Finalize Mesh & Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    # Ensure flat shading for low-poly look
    for poly in mesh.polygons:
        poly.use_smooth = False
        
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    obj.location = Vector(location)

    # === Step 5: Materials ===
    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk")
    mat_trunk.use_nodes = True
    if mat_trunk.node_tree:
        bsdf = mat_trunk.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.2, 0.08, 0.03, 1.0) # Deep brown
            bsdf.inputs["Roughness"].default_value = 0.9

    # Leaves Material
    mat_leaves = bpy.data.materials.new(name=f"{object_name}_Leaves")
    mat_leaves.use_nodes = True
    if mat_leaves.node_tree:
        bsdf = mat_leaves.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.8
            
    mesh.materials.append(mat_trunk)  # Slots to Index 0
    mesh.materials.append(mat_leaves) # Slots to Index 1

    return f"Created '{object_name}' at {location} with {num_layers} leafy layers."

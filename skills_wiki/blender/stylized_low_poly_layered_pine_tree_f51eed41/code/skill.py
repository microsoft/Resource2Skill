def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    leaf_color: tuple = (0.05, 0.25, 0.08),
    wood_color: tuple = (0.25, 0.15, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Layered Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        leaf_color: (R, G, B) base color for the canopy.
        wood_color: (R, G, B) base color for the trunk.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Helper: Build Trunk Geometry ---
    def add_trunk(bm, radius_bot, radius_top, height, segments=8):
        verts_top = []
        verts_bot = []
        faces = []
        center_top = bm.verts.new((0, 0, height))
        center_bot = bm.verts.new((0, 0, 0))
        
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle)
            y = math.sin(angle)
            verts_top.append(bm.verts.new((x * radius_top, y * radius_top, height)))
            verts_bot.append(bm.verts.new((x * radius_bot, y * radius_bot, 0)))
            
        for i in range(segments):
            next_i = (i + 1) % segments
            # Side faces
            faces.append(bm.faces.new((verts_bot[i], verts_bot[next_i], verts_top[next_i], verts_top[i])))
            # Top/Bottom caps
            faces.append(bm.faces.new((verts_top[i], verts_top[next_i], center_top)))
            faces.append(bm.faces.new((verts_bot[next_i], verts_bot[i], center_bot)))
        return faces

    # --- Helper: Build Layered Canopy Geometry ---
    def add_tree_tier(bm, z_offset, radius, height, segments=8):
        verts_outer = []
        verts_inner = []
        verts_dip = []
        
        inset_fac = 0.8
        dip_depth = 0.25 * height
        dip_fac = 0.5
        
        peak_vert = bm.verts.new((0, 0, z_offset + height))
        bottom_center_vert = bm.verts.new((0, 0, z_offset - dip_depth))
        faces = []
        
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle)
            y = math.sin(angle)
            
            verts_outer.append(bm.verts.new((x * radius, y * radius, z_offset)))
            verts_inner.append(bm.verts.new((x * radius * inset_fac, y * radius * inset_fac, z_offset)))
            verts_dip.append(bm.verts.new((x * radius * inset_fac * dip_fac, y * radius * inset_fac * dip_fac, z_offset - dip_depth)))
            
        for i in range(segments):
            next_i = (i + 1) % segments
            # Outer sloped cone
            faces.append(bm.faces.new((verts_outer[i], verts_outer[next_i], peak_vert)))
            # Bottom rim (flat thickness)
            faces.append(bm.faces.new((verts_outer[next_i], verts_outer[i], verts_inner[i], verts_inner[next_i])))
            # Inner cavity sloping downwards
            faces.append(bm.faces.new((verts_inner[next_i], verts_inner[i], verts_dip[i], verts_dip[next_i])))
            # Bottom cavity closure
            faces.append(bm.faces.new((verts_dip[next_i], verts_dip[i], bottom_center_vert)))
        return faces

    # === Step 1: Initialize BMesh ===
    bm = bmesh.new()
    num_segments = kwargs.get("segments", 9)  # 9 gives a nice asymmetrical natural look

    # Build Trunk (Assign to Material Index 1)
    trunk_height = 2.0
    trunk_faces = add_trunk(bm, radius_bot=0.3, radius_top=0.15, height=trunk_height, segments=num_segments)
    for f in trunk_faces:
        f.material_index = 1
        
    # Build Canopy Tiers (Assign to Material Index 0)
    num_tiers = 3
    base_z = trunk_height * 0.4 # Start partway up the trunk
    tier_radius = 1.3
    tier_height = 1.6
    
    for i in range(num_tiers):
        tier_faces = add_tree_tier(bm, z_offset=base_z, radius=tier_radius, height=tier_height, segments=num_segments)
        for f in tier_faces:
            f.material_index = 0
            
        # Scale down for the next tier up
        base_z += tier_height * 0.55 
        tier_radius *= 0.75
        tier_height *= 0.85

    # Clean up normals
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # === Step 2: Create Object & Assign Data ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    # Enforce flat shading for the low-poly aesthetic
    for poly in mesh.polygons:
        poly.use_smooth = False

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 3: Set up Materials ===
    leaf_mat_name = "Mat_Stylized_Leaves"
    wood_mat_name = "Mat_Stylized_Wood"
    
    mat_leaves = bpy.data.materials.get(leaf_mat_name)
    if not mat_leaves:
        mat_leaves = bpy.data.materials.new(name=leaf_mat_name)
        mat_leaves.use_nodes = True
        bsdf = mat_leaves.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*leaf_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.9
            
    mat_wood = bpy.data.materials.get(wood_mat_name)
    if not mat_wood:
        mat_wood = bpy.data.materials.new(name=wood_mat_name)
        mat_wood.use_nodes = True
        bsdf = mat_wood.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*wood_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.9

    mesh.materials.append(mat_leaves) # Index 0
    mesh.materials.append(mat_wood)   # Index 1

    # === Step 4: Finalize Transformations ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{obj.name}' at {location} with {num_tiers} canopy tiers."

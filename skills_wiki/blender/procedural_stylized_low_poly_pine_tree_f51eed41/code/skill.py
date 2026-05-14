def create_stylized_tree(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.25, 0.15, 0.05),
    canopy_color: tuple = (0.15, 0.45, 0.15),
    num_tiers: int = 3,
    segments: int = 12,
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        trunk_color: (R, G, B) base color for the trunk.
        canopy_color: (R, G, B) base color for the leaves.
        num_tiers: Number of overlapping canopy layers.
        segments: Radial resolution (lower = more low-poly look).

    Returns:
        Status string with creation details.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Initialize BMesh ===
    bm = bmesh.new()
    mat_trunk_idx = 0
    mat_canopy_idx = 1
    
    # === Step 2: Generate Trunk ===
    trunk_radius_bot = 0.4
    trunk_radius_top = 0.25
    trunk_height = 2.0
    
    trunk_verts_bot = []
    trunk_verts_top = []
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = math.cos(angle)
        y = math.sin(angle)
        trunk_verts_bot.append(bm.verts.new((x * trunk_radius_bot, y * trunk_radius_bot, 0)))
        trunk_verts_top.append(bm.verts.new((x * trunk_radius_top, y * trunk_radius_top, trunk_height)))
        
    for i in range(segments):
        ni = (i + 1) % segments
        f = bm.faces.new((trunk_verts_bot[i], trunk_verts_bot[ni], trunk_verts_top[ni], trunk_verts_top[i]))
        f.material_index = mat_trunk_idx
        
    f_bot = bm.faces.new(list(reversed(trunk_verts_bot)))
    f_bot.material_index = mat_trunk_idx
    f_top = bm.faces.new(trunk_verts_top)
    f_top.material_index = mat_trunk_idx
    
    # === Step 3: Generate Canopy Tiers ===
    canopy_start_z = 1.0
    tier_height = 2.0
    base_radius = 1.8
    overlap = 0.8  # How much consecutive tiers intersect
    
    for tier in range(num_tiers):
        tier_scale = 1.0 - (tier * 0.25)
        r_outer = base_radius * tier_scale
        r_inner = r_outer * 0.6
        r_top = r_outer * 0.05  # Tapered almost to a point
        
        z_bot = canopy_start_z + tier * (tier_height - overlap)
        z_drop = z_bot - 0.4 * tier_scale  # The stylized overhang
        z_top = z_bot + tier_height * tier_scale
        
        v_bot = bm.verts.new((0, 0, z_bot))
        
        outer_verts = []
        inner_verts = []
        top_verts = []
        
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            x = math.cos(angle)
            y = math.sin(angle)
            outer_verts.append(bm.verts.new((x * r_outer, y * r_outer, z_drop)))
            inner_verts.append(bm.verts.new((x * r_inner, y * r_inner, z_bot)))
            top_verts.append(bm.verts.new((x * r_top, y * r_top, z_top)))
            
        for i in range(segments):
            ni = (i + 1) % segments
            # Main sloping side
            f1 = bm.faces.new((outer_verts[i], outer_verts[ni], top_verts[ni], top_verts[i]))
            f1.material_index = mat_canopy_idx
            
            # Skirt overhang (drops down to inner ring)
            f2 = bm.faces.new((outer_verts[i], inner_verts[i], inner_verts[ni], outer_verts[ni]))
            f2.material_index = mat_canopy_idx
            
            # Base bottom connecting to center axis
            f3 = bm.faces.new((v_bot, inner_verts[ni], inner_verts[i]))
            f3.material_index = mat_canopy_idx
            
        # Top cap
        f4 = bm.faces.new(top_verts)
        f4.material_index = mat_canopy_idx

    # Ensure clean normals for shading
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # === Step 4: Finalize Mesh & Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    for poly in mesh.polygons:
        poly.use_smooth = False  # Enforce flat shading for low-poly look
        
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # === Step 5: Materials ===
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk_Mat")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.9

    mat_canopy = bpy.data.materials.new(name=f"{object_name}_Canopy_Mat")
    mat_canopy.use_nodes = True
    bsdf_canopy = mat_canopy.node_tree.nodes.get("Principled BSDF")
    if bsdf_canopy:
        bsdf_canopy.inputs["Base Color"].default_value = (*canopy_color, 1.0)
        bsdf_canopy.inputs["Roughness"].default_value = 0.8
        
    mesh.materials.append(mat_trunk)
    mesh.materials.append(mat_canopy)
    
    # === Step 6: Modifiers & Transforms ===
    # A slight bevel catches highlights on the sharp stylized edges
    bevel = obj.modifiers.new(name="StylizedBevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 2
    bevel.angle_limit = math.radians(30)
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' with {num_tiers} stylized tiers at {location}."

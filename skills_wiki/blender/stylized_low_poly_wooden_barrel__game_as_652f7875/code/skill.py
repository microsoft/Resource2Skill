def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.20, 0.08),  # Wood base color
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Wooden Barrel in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) wood color.
        **kwargs: 
            metal_color: (R, G, B) for the hoops.
            segments: int, polygon resolution (default 12).
            
    Returns:
        Status string describing the generated asset.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Materials ===
    # Wood Material
    wood_mat_name = f"{object_name}_Wood"
    wood_mat = bpy.data.materials.get(wood_mat_name)
    if not wood_mat:
        wood_mat = bpy.data.materials.new(name=wood_mat_name)
        wood_mat.use_nodes = True
        bsdf = wood_mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.9

    # Metal Material
    metal_color = kwargs.get("metal_color", (0.15, 0.15, 0.15))
    metal_mat_name = f"{object_name}_Metal"
    metal_mat = bpy.data.materials.get(metal_mat_name)
    if not metal_mat:
        metal_mat = bpy.data.materials.new(name=metal_mat_name)
        metal_mat.use_nodes = True
        bsdf = metal_mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*metal_color, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.9
            bsdf.inputs['Roughness'].default_value = 0.4

    # === Step 2: Initialize Geometry ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Link materials (Index 0 = Wood, Index 1 = Metal)
    obj.data.materials.append(wood_mat)
    obj.data.materials.append(metal_mat)
    
    bm = bmesh.new()
    segments = kwargs.get("segments", 12)
    
    # Profile for the barrel body (height_z, radius_r)
    profile = [
        (-1.0, 0.75),
        (-0.5, 0.95),
        (0.0, 1.0),
        (0.5, 0.95),
        (1.0, 0.75)
    ]
    
    # === Step 3: Loft the Main Body ===
    rings = []
    for z, r in profile:
        ring = []
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            v = bm.verts.new((x, y, z))
            ring.append(v)
        rings.append(ring)
        
    for r_idx in range(len(rings) - 1):
        ring1 = rings[r_idx]
        ring2 = rings[r_idx + 1]
        for i in range(segments):
            v1 = ring1[i]
            v2 = ring1[(i + 1) % segments]
            v3 = ring2[(i + 1) % segments]
            v4 = ring2[i]
            f = bm.faces.new((v1, v2, v3, v4))
            f.material_index = 0
            f.smooth = False
            
    # === Step 4: Create Inset Caps (avoiding N-gons) ===
    def create_inset_cap(outer_ring, z_outer, z_inner, r_inner):
        center_vert = bm.verts.new((0, 0, z_inner))
        inner_verts = []
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            x = r_inner * math.cos(angle)
            y = r_inner * math.sin(angle)
            inner_verts.append(bm.verts.new((x, y, z_inner)))
            
        for i in range(segments):
            ni = (i + 1) % segments
            
            # Form the lip/rim and the inner triangle fan
            verts_rim = (outer_ring[i], outer_ring[ni], inner_verts[ni], inner_verts[i])
            verts_fan = (inner_verts[i], inner_verts[ni], center_vert)
                
            f_rim = bm.faces.new(verts_rim)
            f_fan = bm.faces.new(verts_fan)
            
            f_rim.material_index = 0
            f_rim.smooth = False
            f_fan.material_index = 0
            f_fan.smooth = False

    create_inset_cap(rings[-1], z_outer=1.0, z_inner=0.92, r_inner=0.65)   # Top Cap
    create_inset_cap(rings[0], z_outer=-1.0, z_inner=-0.92, r_inner=0.65)  # Bottom Cap

    # === Step 5: Generate Floating Metal Bands ===
    def add_metal_band(z_center, radius, height, thickness):
        r_in = radius - 0.02 # Slight overlap to prevent gaps
        r_out = radius + thickness
        z_bot = z_center - height / 2
        z_top = z_center + height / 2
        
        verts_in_bot, verts_in_top = [], []
        verts_out_bot, verts_out_top = [], []
        
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            verts_in_bot.append(bm.verts.new((r_in * cos_a, r_in * sin_a, z_bot)))
            verts_in_top.append(bm.verts.new((r_in * cos_a, r_in * sin_a, z_top)))
            verts_out_bot.append(bm.verts.new((r_out * cos_a, r_out * sin_a, z_bot)))
            verts_out_top.append(bm.verts.new((r_out * cos_a, r_out * sin_a, z_top)))
            
        for i in range(segments):
            ni = (i + 1) % segments
            f1 = bm.faces.new((verts_out_bot[i], verts_out_bot[ni], verts_out_top[ni], verts_out_top[i]))
            f2 = bm.faces.new((verts_out_top[i], verts_out_top[ni], verts_in_top[ni], verts_in_top[i]))
            f3 = bm.faces.new((verts_in_bot[i], verts_in_bot[ni], verts_out_bot[ni], verts_out_bot[i]))
            f4 = bm.faces.new((verts_in_top[i], verts_in_top[ni], verts_in_bot[ni], verts_in_bot[i]))
            
            for f in (f1, f2, f3, f4):
                f.material_index = 1
                f.smooth = False
                
    add_metal_band(z_center=0.45, radius=0.96, height=0.15, thickness=0.05)
    add_metal_band(z_center=-0.45, radius=0.96, height=0.15, thickness=0.05)
    
    # Unify normals globally
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # Write bmesh data back to standard mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # === Step 6: Finalize Placement ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    
    return f"Created '{object_name}' (Low Poly Game Asset) with {len(mesh.polygons)} faces at {location}"

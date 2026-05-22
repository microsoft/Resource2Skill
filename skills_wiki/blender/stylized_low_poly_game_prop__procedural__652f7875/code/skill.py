def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a game-ready Stylized Low-Poly Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the wood in 0-1 range.
        **kwargs: Optional 'metal_color' override.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    metal_color = kwargs.get("metal_color", (0.15, 0.15, 0.15))
    
    verts = []
    faces = []
    
    # === Geometry Math Parameters ===
    segments = 12
    r_base = 0.8
    r_mid = 1.0
    z_height = 1.2
    z_mid = 0.6
    
    # 1. Wood Profile: (radius, z-height)
    profile = [
        (r_base, -z_height),
        (r_mid, -z_mid),
        (r_mid, z_mid),
        (r_base, z_height)
    ]
    
    # Generate Wood Body Vertices
    for r, z in profile:
        for s in range(segments):
            angle = s * 2 * math.pi / segments
            verts.append((r * math.cos(angle), r * math.sin(angle), z))
            
    # Generate Wood Side Faces
    for i in range(3):
        for s in range(segments):
            s_next = (s + 1) % segments
            v1 = i * segments + s
            v2 = i * segments + s_next
            v3 = (i + 1) * segments + s_next
            v4 = (i + 1) * segments + s
            faces.append((v1, v2, v3, v4))
            
    # Generate Inset Caps (Top and Bottom)
    r_inset = r_base - 0.15
    z_inset_depth = 0.1
    
    # Top Inset
    top_inset_start = len(verts)
    for s in range(segments):
        angle = s * 2 * math.pi / segments
        verts.append((r_inset * math.cos(angle), r_inset * math.sin(angle), z_height - z_inset_depth))
    verts.append((0, 0, z_height - z_inset_depth)) # Center vertex
    
    for s in range(segments):
        s_next = (s + 1) % segments
        # Inner rim
        v1 = 3 * segments + s
        v2 = 3 * segments + s_next
        v3 = top_inset_start + s_next
        v4 = top_inset_start + s
        faces.append((v1, v2, v3, v4))
        # Cap flat
        faces.append((top_inset_start + segments, top_inset_start + s_next, top_inset_start + s))

    # Bottom Inset
    bot_inset_start = len(verts)
    for s in range(segments):
        angle = s * 2 * math.pi / segments
        verts.append((r_inset * math.cos(angle), r_inset * math.sin(angle), -z_height + z_inset_depth))
    verts.append((0, 0, -z_height + z_inset_depth)) # Center vertex
    
    for s in range(segments):
        s_next = (s + 1) % segments
        # Inner rim
        v1 = 0 * segments + s
        v2 = 0 * segments + s_next
        v3 = bot_inset_start + s_next
        v4 = bot_inset_start + s
        faces.append((v1, v4, v3, v2))
        # Cap flat
        faces.append((bot_inset_start + segments, bot_inset_start + s, bot_inset_start + s_next))

    wood_faces_count = len(faces)

    # 2. Metal Bands Geometry
    def add_metal_band(z_bottom, z_top, r_outer):
        r_inner = r_outer - 0.08
        start_v = len(verts)
        
        # Rings: inner bot, outer bot, outer top, inner top
        for r, z in [(r_inner, z_bottom), (r_outer, z_bottom), (r_outer, z_top), (r_inner, z_top)]:
            for s in range(segments):
                angle = s * 2 * math.pi / segments
                verts.append((r * math.cos(angle), r * math.sin(angle), z))
                
        for s in range(segments):
            s_next = (s + 1) % segments
            # Outer Face
            faces.append((start_v + segments + s, start_v + segments + s_next, 
                          start_v + 2*segments + s_next, start_v + 2*segments + s))
            # Top Rim
            faces.append((start_v + 2*segments + s, start_v + 2*segments + s_next, 
                          start_v + 3*segments + s_next, start_v + 3*segments + s))
            # Bottom Rim
            faces.append((start_v + 0*segments + s, start_v + 0*segments + s_next, 
                          start_v + 1*segments + s_next, start_v + 1*segments + s))

    # Add lower and upper bands
    add_metal_band(-0.8, -0.5, 1.02)
    add_metal_band(0.5, 0.8, 1.02)
    
    # === Mesh Assembly & Normal Fix ===
    mesh = bpy.data.meshes.new(object_name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    # Use BMesh purely to recalculate normals (solves any winding direction errors)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # === Material Setup ===
    wood_mat = bpy.data.materials.new(name=f"{object_name}_Wood")
    wood_mat.use_nodes = True
    wood_bsdf = wood_mat.node_tree.nodes["Principled BSDF"]
    wood_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
    wood_bsdf.inputs["Roughness"].default_value = 0.85
    
    metal_mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    metal_mat.use_nodes = True
    metal_bsdf = metal_mat.node_tree.nodes["Principled BSDF"]
    metal_bsdf.inputs["Base Color"].default_value = (*metal_color, 1.0)
    metal_bsdf.inputs["Metallic"].default_value = 1.0
    metal_bsdf.inputs["Roughness"].default_value = 0.4
    
    obj.data.materials.append(wood_mat)
    obj.data.materials.append(metal_mat)
    
    # Assign materials based on face index and enforce flat shading
    for i, poly in enumerate(mesh.polygons):
        poly.use_smooth = False # Essential for low-poly look
        if i < wood_faces_count:
            poly.material_index = 0
        else:
            poly.material_index = 1
            
    # === Transform ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created Stylized Low-Poly Prop '{object_name}' with {len(faces)} faces at {location}."

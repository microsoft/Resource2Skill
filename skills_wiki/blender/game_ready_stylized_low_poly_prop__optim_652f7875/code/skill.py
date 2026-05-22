def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    wood_color: tuple = (0.35, 0.18, 0.08, 1.0),
    metal_color: tuple = (0.1, 0.12, 0.15, 1.0),
    segments: int = 12,
    **kwargs,
) -> str:
    """
    Create a Game-Ready Low-Poly Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        wood_color: RGBA base color for the wood.
        metal_color: RGBA base color for the iron bands.
        segments: Number of radial cuts (keep low for stylized look).
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Materials ===
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf_wood = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_wood:
        bsdf_wood.inputs["Base Color"].default_value = wood_color
        bsdf_wood.inputs["Roughness"].default_value = 0.9
        bsdf_wood.inputs["Metallic"].default_value = 0.0

    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_metal:
        bsdf_metal.inputs["Base Color"].default_value = metal_color
        bsdf_metal.inputs["Roughness"].default_value = 0.4
        bsdf_metal.inputs["Metallic"].default_value = 0.9

    # === Step 2: Initialize Object and Mesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Assign materials (Wood = index 0, Metal = index 1)
    obj.data.materials.append(mat_wood)
    obj.data.materials.append(mat_metal)

    bm = bmesh.new()

    # === Step 3: Generate Base Wood Barrel ===
    z_levels = [-1.0, -0.5, 0.0, 0.5, 1.0]
    radii = [0.75, 0.92, 1.0, 0.92, 0.75]
    
    verts = []
    # Create radial rings for the barrel body
    for z, r in zip(z_levels, radii):
        ring = []
        for i in range(segments):
            a = (i / segments) * 2 * math.pi
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        verts.append(ring)
        
    # Stitch side faces
    for r_idx in range(len(z_levels) - 1):
        for i in range(segments):
            next_i = (i + 1) % segments
            f = bm.faces.new((verts[r_idx][i], verts[r_idx][next_i], 
                              verts[r_idx+1][next_i], verts[r_idx+1][i]))
            f.material_index = 0
            f.smooth = False  # Enforce flat, low-poly shading

    # Create Recessed Bottom Cap
    bot_outer = verts[0]
    bot_inner = []
    bot_center = bm.verts.new((0, 0, -0.92)) # Recessed Z
    for i in range(segments):
        a = (i / segments) * 2 * math.pi
        bot_inner.append(bm.verts.new((0.65 * math.cos(a), 0.65 * math.sin(a), -1.0)))
        
    for i in range(segments):
        next_i = (i + 1) % segments
        f_rim = bm.faces.new((bot_outer[next_i], bot_outer[i], bot_inner[i], bot_inner[next_i]))
        f_rim.material_index = 0
        f_in = bm.faces.new((bot_inner[next_i], bot_inner[i], bot_center))
        f_in.material_index = 0

    # Create Recessed Top Cap
    top_outer = verts[-1]
    top_inner = []
    top_center = bm.verts.new((0, 0, 0.92)) # Recessed Z
    for i in range(segments):
        a = (i / segments) * 2 * math.pi
        top_inner.append(bm.verts.new((0.65 * math.cos(a), 0.65 * math.sin(a), 1.0)))
        
    for i in range(segments):
        next_i = (i + 1) % segments
        f_rim = bm.faces.new((top_outer[i], top_outer[next_i], top_inner[next_i], top_inner[i]))
        f_rim.material_index = 0
        f_in = bm.faces.new((top_inner[i], top_inner[next_i], top_center))
        f_in.material_index = 0

    # === Step 4: Generate Extruded Metal Bands ===
    def add_solid_band(z_b, z_t, r_inner_b, r_inner_t, thickness=0.03):
        r_out_b = r_inner_b + thickness
        r_out_t = r_inner_t + thickness
        
        v_in_b, v_in_t, v_out_b, v_out_t = [], [], [], []
        
        for i in range(segments):
            a = (i / segments) * 2 * math.pi
            c, s = math.cos(a), math.sin(a)
            v_in_b.append(bm.verts.new((r_inner_b * c, r_inner_b * s, z_b)))
            v_in_t.append(bm.verts.new((r_inner_t * c, r_inner_t * s, z_t)))
            v_out_b.append(bm.verts.new((r_out_b * c, r_out_b * s, z_b)))
            v_out_t.append(bm.verts.new((r_out_t * c, r_out_t * s, z_t)))
            
        for i in range(segments):
            next_i = (i + 1) % segments
            # Outer face
            f1 = bm.faces.new((v_out_b[i], v_out_b[next_i], v_out_t[next_i], v_out_t[i]))
            # Top rim
            f2 = bm.faces.new((v_out_t[i], v_out_t[next_i], v_in_t[next_i], v_in_t[i]))
            # Bottom rim
            f3 = bm.faces.new((v_in_b[i], v_in_b[next_i], v_out_b[next_i], v_out_b[i]))
            
            f1.material_index = f2.material_index = f3.material_index = 1
            f1.smooth = f2.smooth = f3.smooth = False

    # Add lower and upper iron bands
    add_solid_band(-0.65, -0.45, 0.86, 0.93)
    add_solid_band(0.45, 0.65, 0.93, 0.86)

    # === Step 5: Finalize Mesh & Transform ===
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} (Optimized Low-Poly Game Asset: {len(mesh.polygons)} polygons)"

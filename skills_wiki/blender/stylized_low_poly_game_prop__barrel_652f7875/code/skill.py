def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.20, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the wood in 0-1 range.
        **kwargs: Optional overrides (e.g., 'segments' to change poly count).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    segments = kwargs.get("segments", 10) # 10 sides gives a perfect chunky look

    # Create new mesh and object
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # --- 1. Construct the Wood Body ---
    # Define the bulge profile of the barrel
    z_levels = [-0.6, -0.3, 0.0, 0.3, 0.6]
    radii = [0.4, 0.48, 0.5, 0.48, 0.4]
    
    rings = []
    for z, r in zip(z_levels, radii):
        ring = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            v = bm.verts.new((r * math.cos(angle), r * math.sin(angle), z))
            ring.append(v)
        rings.append(ring)
        
    wood_faces = []
    
    # Side faces
    for i in range(len(rings) - 1):
        r1 = rings[i]
        r2 = rings[i+1]
        for j in range(segments):
            v1, v2 = r1[j], r1[(j+1)%segments]
            v3, v4 = r2[(j+1)%segments], r2[j]
            f = bm.faces.new((v1, v2, v3, v4))
            wood_faces.append(f)
            
    # Top Cap (inset)
    r_top = rings[-1]
    z_top = z_levels[-1]
    r_top_inner = radii[-1] - 0.05
    inner_top = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        v = bm.verts.new((r_top_inner * math.cos(angle), r_top_inner * math.sin(angle), z_top - 0.03))
        inner_top.append(v)
        
    for j in range(segments):
        v1, v2 = r_top[j], r_top[(j+1)%segments]
        v3, v4 = inner_top[(j+1)%segments], inner_top[j]
        f = bm.faces.new((v1, v2, v3, v4))
        wood_faces.append(f)
    f = bm.faces.new(inner_top)
    wood_faces.append(f)
    
    # Bottom Cap (inset)
    r_bot = rings[0]
    z_bot = z_levels[0]
    r_bot_inner = radii[0] - 0.05
    inner_bot = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        v = bm.verts.new((r_bot_inner * math.cos(angle), r_bot_inner * math.sin(angle), z_bot + 0.03))
        inner_bot.append(v)
        
    for j in range(segments):
        v1, v2 = r_bot[j], r_bot[(j+1)%segments]
        v3, v4 = inner_bot[(j+1)%segments], inner_bot[j]
        f = bm.faces.new((v1, v4, v3, v2))
        wood_faces.append(f)
    f = bm.faces.new(reversed(inner_bot))
    wood_faces.append(f)

    # --- 2. Construct the Metal Bands ---
    metal_faces = []
    band_z = [-0.3, 0.3]
    band_r = 0.495
    band_h = 0.08
    
    for bz in band_z:
        b_rings = []
        # Outer rings
        for z in [bz - band_h/2, bz + band_h/2]:
            ring = []
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                v = bm.verts.new((band_r * math.cos(angle), band_r * math.sin(angle), z))
                ring.append(v)
            b_rings.append(ring)
            
        # Inner rings
        inner_r = band_r - 0.04
        for z in [bz - band_h/2, bz + band_h/2]:
            ring = []
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                v = bm.verts.new((inner_r * math.cos(angle), inner_r * math.sin(angle), z))
                ring.append(v)
            b_rings.append(ring)
            
        for j in range(segments):
            # Outer face
            o1, o2 = b_rings[0][j], b_rings[0][(j+1)%segments]
            o3, o4 = b_rings[1][(j+1)%segments], b_rings[1][j]
            f = bm.faces.new((o1, o2, o3, o4))
            metal_faces.append(f)
            
            # Inner face
            i1, i2 = b_rings[2][j], b_rings[2][(j+1)%segments]
            i3, i4 = b_rings[3][(j+1)%segments], b_rings[3][j]
            f = bm.faces.new((i1, i4, i3, i2))
            metal_faces.append(f)
            
            # Bottom lip
            f = bm.faces.new((o1, i1, i2, o2))
            metal_faces.append(f)
            
            # Top lip
            f = bm.faces.new((o4, o3, i3, i4))
            metal_faces.append(f)

    # Standardize normals before assignment
    bmesh.ops.recalc_normals(bm, faces=bm.faces)

    # Assign material indices
    for f in wood_faces:
        f.material_index = 0
    for f in metal_faces:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()

    # Explicitly enforce flat shading for the stylized low-poly look
    for poly in mesh.polygons:
        poly.use_smooth = False

    # --- 3. Build Materials ---
    # Wood Material (Index 0)
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf_wood = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_wood:
        bsdf_wood.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_wood.inputs["Roughness"].default_value = 0.9

    # Metal Material (Index 1)
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_metal:
        bsdf_metal.inputs["Base Color"].default_value = (0.15, 0.15, 0.15, 1.0)
        bsdf_metal.inputs["Metallic"].default_value = 1.0
        bsdf_metal.inputs["Roughness"].default_value = 0.4

    obj.data.materials.append(mat_wood)
    obj.data.materials.append(mat_metal)

    # --- 4. Position & Finalize ---
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Low Poly Asset) at {location} with geometry ready for game-engine export."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    wood_color: tuple = (0.35, 0.15, 0.05),
    metal_color: tuple = (0.20, 0.20, 0.20),
    **kwargs,
) -> str:
    """
    Create a Low-Poly Stylized Game Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        wood_color: (R, G, B) base color for the wood.
        metal_color: (R, G, B) base color for the metal bands.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Materials Setup ===
    
    # 1. Wood Material
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf_wood = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_wood:
        bsdf_wood.inputs['Base Color'].default_value = (*wood_color, 1.0)
        bsdf_wood.inputs['Roughness'].default_value = 0.85
        if 'Specular' in bsdf_wood.inputs:
            bsdf_wood.inputs['Specular'].default_value = 0.1
        elif 'Specular IOR Level' in bsdf_wood.inputs:
            bsdf_wood.inputs['Specular IOR Level'].default_value = 0.1

    # 2. Metal Material
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_metal:
        bsdf_metal.inputs['Base Color'].default_value = (*metal_color, 1.0)
        bsdf_metal.inputs['Metallic'].default_value = 1.0
        bsdf_metal.inputs['Roughness'].default_value = 0.4

    # === Geometry Generation via BMesh ===
    bm = bmesh.new()
    segments = 12 # Low poly count for game asset

    # -- Part 1: Barrel Body --
    # Define the vertical profile (z_height, radius)
    profile = [
        (-1.0, 0.75),  # Bottom
        (-0.5, 0.95),  # Lower bulge
        (0.0, 1.00),   # Middle equator
        (0.5, 0.95),   # Upper bulge
        (1.0, 0.75)    # Top
    ]

    loops = []
    # Generate vertices in rings
    for z, r in profile:
        loop = []
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            v = bm.verts.new((x, y, z))
            loop.append(v)
        loops.append(loop)

    # Generate side faces for the body
    for i in range(len(profile) - 1):
        for j in range(segments):
            v1 = loops[i][j]
            v2 = loops[i][(j + 1) % segments]
            v3 = loops[i + 1][(j + 1) % segments]
            v4 = loops[i + 1][j]
            f = bm.faces.new((v1, v2, v3, v4))
            f.material_index = 0 # Wood
            f.smooth = False # Enforce low-poly flat shading

    # Top Cap (Inset and depressed)
    top_loop = loops[-1]
    top_inset = [bm.verts.new((v.co.x * 0.85, v.co.y * 0.85, v.co.z)) for v in top_loop]
    for j in range(segments):
        f = bm.faces.new((top_loop[j], top_loop[(j+1)%segments], top_inset[(j+1)%segments], top_inset[j]))
        f.material_index = 0
        f.smooth = False
    
    for v in top_inset: 
        v.co.z -= 0.1 # Push inset down
    f_top = bm.faces.new(top_inset)
    f_top.material_index = 0
    f_top.smooth = False

    # Bottom Cap (Inset and depressed upwards)
    bot_loop = loops[0]
    bot_inset = [bm.verts.new((v.co.x * 0.85, v.co.y * 0.85, v.co.z)) for v in bot_loop]
    for j in range(segments):
        # Reverse winding order for bottom faces so normals point out
        f = bm.faces.new((bot_loop[j], bot_inset[j], bot_inset[(j+1)%segments], bot_loop[(j+1)%segments]))
        f.material_index = 0
        f.smooth = False
        
    for v in bot_inset: 
        v.co.z += 0.1 # Push inset up into the barrel
    f_bot = bm.faces.new(reversed(bot_inset)) # Reverse to fix normal direction
    f_bot.material_index = 0
    f_bot.smooth = False

    # -- Part 2: Metal Bands --
    # Define bands: (z_center, thickness, radius_inner, radius_outer)
    bands = [
        (-0.6, 0.15, 0.88, 0.96),
        (0.6, 0.15, 0.88, 0.96)
    ]

    for z_c, th, r_in, r_out in bands:
        z_min = z_c - th / 2.0
        z_max = z_c + th / 2.0
        
        o_bot = [bm.verts.new((r_out * math.cos(i*2*math.pi/segments), r_out * math.sin(i*2*math.pi/segments), z_min)) for i in range(segments)]
        o_top = [bm.verts.new((r_out * math.cos(i*2*math.pi/segments), r_out * math.sin(i*2*math.pi/segments), z_max)) for i in range(segments)]
        i_bot = [bm.verts.new((r_in * math.cos(i*2*math.pi/segments), r_in * math.sin(i*2*math.pi/segments), z_min)) for i in range(segments)]
        i_top = [bm.verts.new((r_in * math.cos(i*2*math.pi/segments), r_in * math.sin(i*2*math.pi/segments), z_max)) for i in range(segments)]

        for i in range(segments):
            n_i = (i + 1) % segments
            # Outer face
            f1 = bm.faces.new((o_bot[i], o_bot[n_i], o_top[n_i], o_top[i]))
            # Top edge
            f2 = bm.faces.new((o_top[i], o_top[n_i], i_top[n_i], i_top[i]))
            # Bottom edge
            f3 = bm.faces.new((o_bot[i], i_bot[i], i_bot[n_i], o_bot[n_i]))
            
            for f in (f1, f2, f3):
                f.material_index = 1 # Metal
                f.smooth = False

    # Clean up and calculate normals
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # === Object Creation ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(object_name, mesh)
    
    # Add materials to object
    obj.data.materials.append(mat_wood)  # Index 0
    obj.data.materials.append(mat_metal) # Index 1

    # Link to scene
    scene.collection.objects.link(obj)

    # Position and scale
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    return f"Created '{object_name}' (Low-Poly Game Asset) at {location} with {len(mesh.polygons)} faces."

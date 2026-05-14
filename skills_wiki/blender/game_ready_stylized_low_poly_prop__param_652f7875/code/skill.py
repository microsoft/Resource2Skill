def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a Game-Ready Stylized Low-Poly Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the wood in 0-1 range.
        **kwargs: 
            metal_color: (R, G, B) for the metal bands.
            segments: Radial resolution (default 12 for low-poly).
            bulge: Multiplier for the middle thickness (default 1.25).

    Returns:
        Status string describing the generated asset.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Initialize Object and Mesh ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # === Step 2: Build Materials ===
    # Wood Material
    wood_mat = bpy.data.materials.new(name=f"{object_name}_Wood")
    wood_mat.use_nodes = True
    wood_bsdf = wood_mat.node_tree.nodes.get("Principled BSDF")
    if wood_bsdf:
        wood_bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        wood_bsdf.inputs['Roughness'].default_value = 0.8
        
    # Metal Material
    metal_color = kwargs.get("metal_color", (0.15, 0.15, 0.15))
    metal_mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    metal_mat.use_nodes = True
    metal_bsdf = metal_mat.node_tree.nodes.get("Principled BSDF")
    if metal_bsdf:
        metal_bsdf.inputs['Base Color'].default_value = (*metal_color, 1.0)
        metal_bsdf.inputs['Metallic'].default_value = 1.0
        metal_bsdf.inputs['Roughness'].default_value = 0.3

    mesh.materials.append(wood_mat)
    mesh.materials.append(metal_mat)

    # === Step 3: Procedural Geometry Generation (bmesh) ===
    bm = bmesh.new()
    
    radius = 0.5
    height = 1.2
    segments = kwargs.get("segments", 12)
    z_steps = 5  # 5 rows of faces creates exactly 2 bands separated by wood
    bulge_factor = kwargs.get("bulge", 1.25)
    
    verts = []
    # Generate vertices row by row
    for i in range(z_steps + 1):
        z = -height / 2 + (height / z_steps) * i
        
        # Calculate quadratic bulge profile (t goes from -1 to 1)
        t = (i / z_steps) * 2 - 1 
        current_radius = radius * (1 + (bulge_factor - 1) * (1 - t*t))
        
        layer = []
        for j in range(segments):
            angle = (j / segments) * 2 * math.pi
            x = current_radius * math.cos(angle)
            y = current_radius * math.sin(angle)
            layer.append(bm.verts.new((x, y, z)))
        verts.append(layer)
        
    wood_faces = []
    metal_faces = []
    
    # Generate side faces and assign material indices
    for i in range(z_steps):
        for j in range(segments):
            # Counter-clockwise winding order looking from outside
            v1 = verts[i][j]
            v2 = verts[i][(j+1)%segments]
            v3 = verts[i+1][(j+1)%segments]
            v4 = verts[i+1][j]
            face = bm.faces.new((v1, v2, v3, v4))
            
            # Row 1 and Row 3 become the metal bands
            if i == 1 or i == z_steps - 2:
                metal_faces.append(face)
                face.material_index = 1
            else:
                wood_faces.append(face)
                face.material_index = 0
                
    # Generate End Caps (N-Gons for maximum optimization)
    # Top Cap (Counter-Clockwise from top)
    top_cap = bm.faces.new([verts[-1][j] for j in range(segments)])
    top_cap.material_index = 0
    
    # Bottom Cap (Clockwise from top, which is CCW from bottom)
    bottom_cap = bm.faces.new([verts[0][segments - 1 - j] for j in range(segments)])
    bottom_cap.material_index = 0
    
    # Clean up and write to mesh
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    # Enforce flat shading
    for p in mesh.polygons:
        p.use_smooth = False
        
    # === Step 4: Position & Finalize ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created engine-ready '{object_name}' at {location} with {len(mesh.polygons)} faces."

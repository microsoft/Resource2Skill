def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.20, 0.08),
    **kwargs,
) -> str:
    """
    Create a Game-Ready Low-Poly Stylized Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the wood in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Procedural Geometry Definition ===
    segments = 12
    # Z-heights defining the barrel profile and the metal bands
    z_levels = [-1.0, -0.6, -0.4, 0.4, 0.6, 1.0]
    # Corresponding radii to create the outward bulge
    radii = [0.8, 0.95, 0.98, 0.98, 0.95, 0.8]

    verts = []
    faces = []
    face_materials = []  # 0 for wood, 1 for metal

    # Generate Vertices
    for z, r in zip(z_levels, radii):
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            verts.append((r * math.cos(angle), r * math.sin(angle), z))

    # Generate Faces
    # Bottom cap
    faces.append([i for i in range(segments)][::-1])  # Reversed to face outwards
    face_materials.append(0)

    # Side walls
    for level in range(len(z_levels) - 1):
        # Assign Metal (mat_idx 1) to specific bands (level 1 and 3)
        mat_idx = 1 if level in (1, 3) else 0  
        for i in range(segments):
            v1 = level * segments + i
            v2 = level * segments + (i + 1) % segments
            v3 = (level + 1) * segments + (i + 1) % segments
            v4 = (level + 1) * segments + i
            faces.append([v1, v2, v3, v4])
            face_materials.append(mat_idx)

    # Top cap
    top_start = (len(z_levels) - 1) * segments
    faces.append([top_start + i for i in range(segments)])
    face_materials.append(0)

    # === Step 2: Build Mesh & Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Ensure flat shading for stylized low-poly aesthetic
    for poly in obj.data.polygons:
        poly.use_smooth = False

    # === Step 3: Build & Assign Materials ===
    # Material 0: Wood
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf_w = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_w:
        bsdf_w.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_w.inputs["Roughness"].default_value = 0.9

    # Material 1: Metal Bands
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_m = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1.0)
        bsdf_m.inputs["Metallic"].default_value = 1.0
        bsdf_m.inputs["Roughness"].default_value = 0.4

    obj.data.materials.append(mat_wood)  # Index 0
    obj.data.materials.append(mat_metal) # Index 1

    # Map face materials based on the logic defined during generation
    for poly, mat_idx in zip(obj.data.polygons, face_materials):
        poly.material_index = mat_idx

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with {len(verts)} vertices and {len(faces)} faces (Optimized Game Asset)."

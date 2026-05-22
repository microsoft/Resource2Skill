def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.16, 0.05),
    **kwargs,
) -> str:
    """
    Create a Game-Ready Low Poly Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the wood.
        **kwargs: Additional overrides (metal_color, segments).

    Returns:
        Status string confirming creation and polygon count.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    from math import sin, cos, pi

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Mesh and Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Build Materials ===
    # Wood Material (Index 0)
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf_wood = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_wood:
        bsdf_wood.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_wood.inputs['Roughness'].default_value = 0.85
    mesh.materials.append(mat_wood)

    # Metal Material (Index 1)
    metal_color = kwargs.get("metal_color", (0.15, 0.15, 0.15))
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_metal:
        bsdf_metal.inputs['Base Color'].default_value = (*metal_color, 1.0)
        bsdf_metal.inputs['Metallic'].default_value = 1.0
        bsdf_metal.inputs['Roughness'].default_value = 0.4
    mesh.materials.append(mat_metal)

    # === Step 3: Generate Procedural BMesh Geometry ===
    bm = bmesh.new()
    segments = kwargs.get("segments", 12)

    # Define vertical profile rings: (z_height, radius)
    profile = [
        (1.2, 0.85),   # 0: Top cap edge
        (0.8, 1.05),   # 1: Metal band 1 top
        (0.6, 1.10),   # 2: Metal band 1 bottom
        (0.0, 1.15),   # 3: Equator (widest point)
        (-0.6, 1.10),  # 4: Metal band 2 top
        (-0.8, 1.05),  # 5: Metal band 2 bottom
        (-1.2, 0.85)   # 6: Bottom cap edge
    ]

    # Generate vertices layer by layer
    rings = []
    for z, r in profile:
        ring_verts = []
        for i in range(segments):
            angle = (i / segments) * 2 * pi
            x = cos(angle) * r
            y = sin(angle) * r
            v = bm.verts.new((x, y, z))
            ring_verts.append(v)
        rings.append(ring_verts)

    # Create side faces and assign materials based on vertical height
    for i in range(len(rings) - 1):
        ring1 = rings[i]
        ring2 = rings[i+1]

        # Assign Metal material (index 1) to specific ring intervals
        mat_idx = 1 if i in (1, 4) else 0

        for j in range(segments):
            v1 = ring1[j]
            v2 = ring1[(j+1) % segments]
            v3 = ring2[(j+1) % segments]
            v4 = ring2[j]

            f = bm.faces.new((v1, v2, v3, v4))
            f.material_index = mat_idx

    # Create top and bottom caps
    top_cap = bm.faces.new(rings[0][::-1]) # Reverse winding for correct upward normal
    top_cap.material_index = 0
    bottom_cap = bm.faces.new(rings[-1])   # Normal points downward
    bottom_cap.material_index = 0

    # Clean up and finalize mesh
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # Ensure low poly "flat shaded" aesthetic
    for poly in mesh.polygons:
        poly.use_smooth = False

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Low Poly Barrel) at {location} with {len(mesh.polygons)} game-ready faces."

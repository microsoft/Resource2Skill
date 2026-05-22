def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a game-ready, low-poly stylized barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the wood in 0-1 range.
        **kwargs: Optional 'segments' integer to control polygon count (default 12).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Build Materials ===
    wood_mat = bpy.data.materials.new(name=f"{object_name}_Wood")
    wood_mat.use_nodes = True
    if "Principled BSDF" in wood_mat.node_tree.nodes:
        bsdf = wood_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8
        bsdf.inputs["Metallic"].default_value = 0.0

    metal_mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    metal_mat.use_nodes = True
    if "Principled BSDF" in metal_mat.node_tree.nodes:
        bsdf = metal_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.15, 0.15, 0.15, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
        bsdf.inputs["Metallic"].default_value = 1.0

    # === Step 2: Initialize Object ===
    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    obj.data.materials.append(wood_mat)   # Material Index 0
    obj.data.materials.append(metal_mat)  # Material Index 1

    # === Step 3: Procedural BMesh Generation ===
    bm = bmesh.new()
    segments = kwargs.get("segments", 12)

    # Define the silhouette profile: (Z-Height, Radius)
    profile = [
        (-1.10, 0.85),  # 0: inner bottom cap
        (-1.20, 0.85),  # 1: bottom rim inner
        (-1.20, 0.95),  # 2: bottom rim outer
        (-0.70, 1.05),  # 3: lower wood body
        (-0.70, 1.08),  # 4: metal band 1 bottom edge
        (-0.40, 1.13),  # 5: metal band 1 face
        (-0.40, 1.10),  # 6: metal band 1 top edge
        (0.00,  1.15),  # 7: barrel equator
        (0.40,  1.10),  # 8: upper wood body
        (0.40,  1.13),  # 9: metal band 2 bottom edge
        (0.70,  1.08),  # 10: metal band 2 face
        (0.70,  1.05),  # 11: metal band 2 top edge
        (1.20,  0.95),  # 12: top rim outer
        (1.20,  0.85),  # 13: top rim inner
        (1.10,  0.85),  # 14: inner top cap
    ]

    # Material index for the faces connecting ring[i] to ring[i+1]
    segment_mats = [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0]

    rings = []
    # Generate vertices in circular rings
    for z, r in profile:
        ring_verts = []
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            ring_verts.append(bm.verts.new((x, y, z)))
        rings.append(ring_verts)

    # Connect rings to form quad faces
    for i in range(len(rings) - 1):
        ring1 = rings[i]
        ring2 = rings[i + 1]
        mat_idx = segment_mats[i]

        for j in range(segments):
            v1 = ring1[j]
            v2 = ring1[(j + 1) % segments]
            v3 = ring2[(j + 1) % segments]
            v4 = ring2[j]
            face = bm.faces.new((v1, v2, v3, v4))
            face.material_index = mat_idx

    # Create top and bottom caps
    bottom_cap = bm.faces.new(reversed(rings[0]))
    bottom_cap.material_index = 0
    top_cap = bm.faces.new(rings[-1])
    top_cap.material_index = 0

    # Write data back to mesh
    bm.to_mesh(mesh)
    bm.free()

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with {len(mesh.polygons)} polygons."

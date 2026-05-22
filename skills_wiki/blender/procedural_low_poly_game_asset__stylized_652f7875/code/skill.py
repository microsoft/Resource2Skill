def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.15, 0.05),  # Wood color
    **kwargs,
) -> str:
    """
    Create a game-ready, multi-material Low-Poly Barrel.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the wood.
        **kwargs: Optional overrides (segments, metal_color).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Parameters
    segments = kwargs.get("segments", 12)
    metal_color = kwargs.get("metal_color", (0.15, 0.15, 0.15))

    # === Step 1: Build Materials ===
    mat_wood = bpy.data.materials.new(name=f"{object_name}_Wood")
    mat_wood.use_nodes = True
    wood_bsdf = mat_wood.node_tree.nodes.get("Principled BSDF")
    wood_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
    wood_bsdf.inputs["Roughness"].default_value = 0.9
    wood_bsdf.inputs["Specular IOR Level"].default_value = 0.1

    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    metal_bsdf = mat_metal.node_tree.nodes.get("Principled BSDF")
    metal_bsdf.inputs["Base Color"].default_value = (*metal_color, 1.0)
    metal_bsdf.inputs["Metallic"].default_value = 1.0
    metal_bsdf.inputs["Roughness"].default_value = 0.45

    # === Step 2: Initialize Mesh ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    mesh.materials.append(mat_wood)   # Index 0
    mesh.materials.append(mat_metal)  # Index 1

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Helper: Create a ring of vertices. Z is shifted by +1.0 so the barrel origin is at the bottom (Z=0)
    def add_ring(z, r):
        return [
            bm.verts.new((
                r * math.cos(i * 2 * math.pi / segments),
                r * math.sin(i * 2 * math.pi / segments),
                z + 1.0
            )) for i in range(segments)
        ]

    # === Step 3: Define Structural Cross-Sections ===
    # Wood profile
    r0 = add_ring(0.95, 0.75)  # Top inner lid
    r1 = add_ring(1.0, 0.75)   # Top rim inner
    r2 = add_ring(1.0, 0.8)    # Top rim outer
    r3 = add_ring(0.6, 0.92)   # Above upper band
    r4 = add_ring(0.4, 0.96)   # Below upper band
    r5 = add_ring(0.0, 1.0)    # Equator (widest)
    r6 = add_ring(-0.4, 0.96)  # Above lower band
    r7 = add_ring(-0.6, 0.92)  # Below lower band
    r8 = add_ring(-1.0, 0.8)   # Bottom rim outer
    r9 = add_ring(-1.0, 0.75)  # Bottom rim inner
    r10 = add_ring(-0.95, 0.75)# Bottom inner lid

    # Center vertices for the lids
    v_top = bm.verts.new((0, 0, 0.95 + 1.0))
    v_bot = bm.verts.new((0, 0, -0.95 + 1.0))

    # Metal Band profiles (extruding out from the wood)
    band_ext = 0.04
    b1_top = add_ring(0.6, 0.92 + band_ext)
    b1_bot = add_ring(0.4, 0.96 + band_ext)
    b2_top = add_ring(-0.4, 0.96 + band_ext)
    b2_bot = add_ring(-0.6, 0.92 + band_ext)

    # === Step 4: Face Generation Helper ===
    def make_faces(ring1, ring2, mat_idx):
        for i in range(segments):
            v1 = ring1[i]
            v2 = ring1[(i+1) % segments]
            v3 = ring2[(i+1) % segments]
            v4 = ring2[i]
            try:
                f = bm.faces.new((v1, v2, v3, v4))
                f.material_index = mat_idx
                f.smooth = False  # Enforce flat low-poly shading
            except ValueError:
                pass # Face exists

    # === Step 5: Connect Faces ===
    # Wood Sections
    make_faces(r0, r1, 0)   # Top inside lip
    make_faces(r2, r1, 0)   # Top flat rim
    make_faces(r2, r3, 0)   # Slope to upper band
    make_faces(r4, r5, 0)   # Slope to equator
    make_faces(r5, r6, 0)   # Slope to lower band
    make_faces(r7, r8, 0)   # Slope to bottom rim
    make_faces(r9, r8, 0)   # Bottom flat rim
    make_faces(r10, r9, 0)  # Bottom inside lip

    # Lids (Triangles)
    for i in range(segments):
        f_top = bm.faces.new((v_top, r0[(i+1)%segments], r0[i]))
        f_top.material_index = 0
        f_top.smooth = False
        
        f_bot = bm.faces.new((v_bot, r10[i], r10[(i+1)%segments]))
        f_bot.material_index = 0
        f_bot.smooth = False

    # Metal Band 1 (Upper)
    make_faces(b1_top, r3, 1)      # Top ledge of band
    make_faces(b1_top, b1_bot, 1)  # Outer face of band
    make_faces(r4, b1_bot, 1)      # Bottom ledge of band

    # Metal Band 2 (Lower)
    make_faces(b2_top, r6, 1)      # Top ledge of band
    make_faces(b2_top, b2_bot, 1)  # Outer face of band
    make_faces(r7, b2_bot, 1)      # Bottom ledge of band

    # === Step 6: Finalize Mesh ===
    # Let Blender enforce strict outward-facing normals to fix any CCW/CW ordering issues
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.normal_update()
    
    bm.to_mesh(mesh)
    bm.free()

    # === Step 7: Transform & Placement ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created Game-Ready Low Poly Barrel '{object_name}' at {location} with {len(mesh.polygons)} polygons."

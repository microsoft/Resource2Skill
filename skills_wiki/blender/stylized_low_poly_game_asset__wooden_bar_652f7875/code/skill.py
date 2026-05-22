def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Wooden Barrel in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) wood color.
        **kwargs: Additional overrides (e.g., segments, metal_color).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    segments = kwargs.get('segments', 12)
    metal_color = kwargs.get('metal_color', (0.15, 0.15, 0.15))

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Barrel Proportions
    rings = 7
    height = 2.0
    radius_end = 0.75
    radius_mid = 1.0

    # === Step 1: Generate Wood Body ===
    verts = []
    for i in range(rings):
        z = (i / (rings - 1)) * height - (height / 2.0)
        t = z / (height / 2.0)
        
        # Parabolic curve to create the barrel bulge
        r = radius_mid - (radius_mid - radius_end) * (t * t)
        
        ring_verts = []
        for s in range(segments):
            angle = s * (2 * math.pi / segments)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            v = bm.verts.new((x, y, z))
            ring_verts.append(v)
        verts.append(ring_verts)

    body_faces = []
    
    # Side faces
    for i in range(rings - 1):
        for s in range(segments):
            s_next = (s + 1) % segments
            v1 = verts[i][s]
            v2 = verts[i][s_next]
            v3 = verts[i+1][s_next]
            v4 = verts[i+1][s]
            body_faces.append(bm.faces.new((v1, v2, v3, v4)))

    # Bottom cap with inset rim (to simulate thick planks)
    bottom_inset_verts = []
    for s in range(segments):
        v = verts[0][s]
        d = -Vector((v.co.x, v.co.y, 0)).normalized()
        v_inset = bm.verts.new(v.co + d * 0.1 + Vector((0, 0, 0.1)))
        bottom_inset_verts.append(v_inset)

    for s in range(segments):
        s_next = (s + 1) % segments
        body_faces.append(bm.faces.new((verts[0][s], verts[0][s_next], bottom_inset_verts[s_next], bottom_inset_verts[s])))
    body_faces.append(bm.faces.new(reversed(bottom_inset_verts)))

    # Top cap with inset rim
    top_inset_verts = []
    for s in range(segments):
        v = verts[-1][s]
        d = -Vector((v.co.x, v.co.y, 0)).normalized()
        v_inset = bm.verts.new(v.co + d * 0.1 + Vector((0, 0, -0.1)))
        top_inset_verts.append(v_inset)

    for s in range(segments):
        s_next = (s + 1) % segments
        body_faces.append(bm.faces.new((verts[-1][s_next], verts[-1][s], top_inset_verts[s], top_inset_verts[s_next])))
    body_faces.append(bm.faces.new(top_inset_verts))

    for f in body_faces:
        f.material_index = 0
        f.smooth = False  # Flat shading for low-poly look

    # === Step 2: Generate Metal Bands ===
    def make_band(z_center, band_h, r_out, r_in):
        z_top = z_center + band_h / 2.0
        z_bot = z_center - band_h / 2.0
        
        out_top = [bm.verts.new((r_out * math.cos(i*2*math.pi/segments), r_out * math.sin(i*2*math.pi/segments), z_top)) for i in range(segments)]
        out_bot = [bm.verts.new((r_out * math.cos(i*2*math.pi/segments), r_out * math.sin(i*2*math.pi/segments), z_bot)) for i in range(segments)]
        in_top = [bm.verts.new((r_in * math.cos(i*2*math.pi/segments), r_in * math.sin(i*2*math.pi/segments), z_top)) for i in range(segments)]
        in_bot = [bm.verts.new((r_in * math.cos(i*2*math.pi/segments), r_in * math.sin(i*2*math.pi/segments), z_bot)) for i in range(segments)]
        
        band_faces = []
        for s in range(segments):
            s_next = (s + 1) % segments
            band_faces.append(bm.faces.new((out_bot[s], out_bot[s_next], out_top[s_next], out_top[s]))) # Outer
            band_faces.append(bm.faces.new((in_bot[s_next], in_bot[s], in_top[s], in_top[s_next])))     # Inner
            band_faces.append(bm.faces.new((in_top[s], out_top[s], out_top[s_next], in_top[s_next])))   # Top
            band_faces.append(bm.faces.new((in_bot[s_next], out_bot[s_next], out_bot[s], in_bot[s])))   # Bottom
        
        for f in band_faces:
            f.material_index = 1
            f.smooth = False

    # Upper band
    z1 = 0.5
    t1 = z1 / (height / 2.0)
    r1 = radius_mid - (radius_mid - radius_end) * (t1 * t1)
    make_band(z1, 0.15, r1 + 0.04, r1 - 0.05)

    # Lower band
    z2 = -0.5
    t2 = z2 / (height / 2.0)
    r2 = radius_mid - (radius_mid - radius_end) * (t2 * t2)
    make_band(z2, 0.15, r2 + 0.04, r2 - 0.05)

    # Clean up normals and finalize mesh
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Build Materials ===
    wood_mat = bpy.data.materials.new(name=f"{object_name}_Wood")
    wood_mat.use_nodes = True
    wood_bsdf = wood_mat.node_tree.nodes.get("Principled BSDF")
    if wood_bsdf:
        wood_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        wood_bsdf.inputs["Roughness"].default_value = 0.9

    metal_mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    metal_mat.use_nodes = True
    metal_bsdf = metal_mat.node_tree.nodes.get("Principled BSDF")
    if metal_bsdf:
        metal_bsdf.inputs["Base Color"].default_value = (*metal_color, 1.0)
        metal_bsdf.inputs["Metallic"].default_value = 1.0
        metal_bsdf.inputs["Roughness"].default_value = 0.4

    obj.data.materials.append(wood_mat)
    obj.data.materials.append(metal_mat)

    # === Step 4: Modifiers ===
    # A subtle bevel catches lighting on low-poly edges and drastically improves the look
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.02
    bevel.segments = 1

    # === Step 5: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Low-Poly Barrel) at {location} with {segments} segments."

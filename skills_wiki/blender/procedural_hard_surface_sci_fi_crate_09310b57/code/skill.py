def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Crate",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a highly detailed procedural Sci-Fi Hard Surface Crate using a boolean-bevel workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space placement.
        scale: Uniform scale factor.
        material_color: (R, G, B) emissive accent color.

    Returns:
        Status string describing the operation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Main Body Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    # Give it a slightly squat, heavy proportion
    bmesh.ops.scale(bm, vec=(1.0, 1.0, 0.85), verts=bm.verts)

    # Assign Bevel Weight ONLY to vertical edges
    bw_layer = bm.edges.layers.bevel_weight.verify()
    for e in bm.edges:
        v1, v2 = e.verts
        if abs(v1.co.x - v2.co.x) < 0.001 and abs(v1.co.y - v2.co.y) < 0.001:
            e[bw_layer] = 1.0
        else:
            e[bw_layer] = 0.0

    bm.to_mesh(mesh)
    bm.free()

    # Enable smooth shading for hardened normals to work properly
    for p in mesh.polygons:
        p.use_smooth = True
    if hasattr(mesh, "use_auto_smooth"):
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = 0.8

    # === Step 2: Build Base Modifiers ===
    # 1. Round the vertical edges
    bev_vert = obj.modifiers.new("Bevel_Vertical", 'BEVEL')
    bev_vert.limit_method = 'WEIGHT'
    bev_vert.width = 0.3
    bev_vert.segments = 8

    # 2. Chamfer the top and bottom rims
    bev_chamf = obj.modifiers.new("Bevel_Chamfer", 'BEVEL')
    bev_chamf.limit_method = 'ANGLE'
    bev_chamf.angle_limit = 1.047  # ~60 degrees
    bev_chamf.width = 0.1
    bev_chamf.segments = 1

    # === Step 3: Create Materials ===
    mat_main = bpy.data.materials.new(object_name + "_Main")
    mat_main.use_nodes = True
    bsdf_main = mat_main.node_tree.nodes.get("Principled BSDF")
    bsdf_main.inputs['Base Color'].default_value = (0.15, 0.16, 0.18, 1.0)
    bsdf_main.inputs['Metallic'].default_value = 1.0
    bsdf_main.inputs['Roughness'].default_value = 0.4

    mat_accent = bpy.data.materials.new(object_name + "_Accent")
    mat_accent.use_nodes = True
    bsdf_acc = mat_accent.node_tree.nodes.get("Principled BSDF")
    bsdf_acc.inputs['Base Color'].default_value = material_color + (1.0,)
    if 'Emission Color' in bsdf_acc.inputs:
        bsdf_acc.inputs['Emission Color'].default_value = material_color + (1.0,)
    elif 'Emission' in bsdf_acc.inputs:
        bsdf_acc.inputs['Emission'].default_value = material_color + (1.0,)
    bsdf_acc.inputs['Emission Strength'].default_value = 10.0
    bsdf_acc.inputs['Metallic'].default_value = 0.5
    bsdf_acc.inputs['Roughness'].default_value = 0.3

    mat_dark = bpy.data.materials.new(object_name + "_Dark")
    mat_dark.use_nodes = True
    bsdf_dark = mat_dark.node_tree.nodes.get("Principled BSDF")
    bsdf_dark.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
    bsdf_dark.inputs['Metallic'].default_value = 0.8
    bsdf_dark.inputs['Roughness'].default_value = 0.6

    # Assign materials to slots so booleans can inherit them
    obj.data.materials.append(mat_main)
    obj.data.materials.append(mat_accent)
    obj.data.materials.append(mat_dark)

    # === Step 4: Cutter Factory ===
    cutters = []

    def create_mirrored_box(name, dim, offset, mat, mx=False, my=False):
        c_mesh = bpy.data.meshes.new(object_name + "_" + name)
        c_obj = bpy.data.objects.new(object_name + "_" + name, c_mesh)
        scene.collection.objects.link(c_obj)
        
        bm_c = bmesh.new()
        bmesh.ops.create_cube(bm_c, size=1.0)
        bmesh.ops.scale(bm_c, vec=dim, verts=bm_c.verts)
        bmesh.ops.translate(bm_c, vec=offset, verts=bm_c.verts)
        bm_c.to_mesh(c_mesh)
        bm_c.free()
        
        if mx or my:
            mir = c_obj.modifiers.new("Mirror", 'MIRROR')
            mir.use_axis[0] = mx
            mir.use_axis[1] = my
            mir.use_axis[2] = False
            
        c_obj.display_type = 'BOUNDS'
        c_obj.hide_render = True
        c_obj.hide_set(True)
        if mat:
            c_mesh.materials.append(mat)
        cutters.append(c_obj)
        return c_obj

    def create_mirrored_cyl(name, radius, depth, offset, mat, mx=False, my=False):
        c_mesh = bpy.data.meshes.new(object_name + "_" + name)
        c_obj = bpy.data.objects.new(object_name + "_" + name, c_mesh)
        scene.collection.objects.link(c_obj)
        
        bm_c = bmesh.new()
        bmesh.ops.create_cone(bm_c, cap_ends=True, segments=24, radius1=radius, radius2=radius, depth=depth)
        bmesh.ops.translate(bm_c, vec=offset, verts=bm_c.verts)
        bm_c.to_mesh(c_mesh)
        bm_c.free()
        
        if mx or my:
            mir = c_obj.modifiers.new("Mirror", 'MIRROR')
            mir.use_axis[0] = mx
            mir.use_axis[1] = my
        
        c_obj.display_type = 'BOUNDS'
        c_obj.hide_render = True
        c_obj.hide_set(True)
        if mat:
            c_mesh.materials.append(mat)
        cutters.append(c_obj)
        return c_obj

    # Build the mechanical details (Cutters)
    # 1. Top and Bottom large insets (rounded rectangles)
    c_top_in = create_mirrored_box("TopInset", (1.4, 1.4, 0.5), (0, 0, 0.85), mat_dark)
    bev_in_t = c_top_in.modifiers.new("Bevel", 'BEVEL')
    bev_in_t.width, bev_in_t.segments = 0.2, 8
    
    c_bot_in = create_mirrored_box("BotInset", (1.4, 1.4, 0.5), (0, 0, -0.85), mat_dark)
    bev_in_b = c_bot_in.modifiers.new("Bevel", 'BEVEL')
    bev_in_b.width, bev_in_b.segments = 0.2, 8

    # 2. Emissive Middle Slice
    create_mirrored_box("MidSlice", (2.5, 2.5, 0.05), (0, 0, 0.1), mat_accent)

    # 3. Outer edge notches
    create_mirrored_box("TopNotch", (0.5, 0.4, 0.2), (0, 1.0, 0.85), mat_dark, mx=False, my=True)
    create_mirrored_box("TopSmallNotch", (0.05, 0.5, 0.25), (0.15, 1.0, 0.85), mat_dark, mx=True, my=True)
    create_mirrored_box("SideGroove", (0.2, 0.1, 0.4), (1.0, 0.5, 0.0), mat_dark, mx=True, my=True)
    create_mirrored_box("SideHandle", (0.2, 0.4, 0.15), (1.0, 0.0, -0.4), mat_dark, mx=True, my=False)

    # 4. Circular Vents
    create_mirrored_cyl("Vent1", 0.06, 0.5, (0.55, 0.55, 0.85), mat_dark, True, True)
    create_mirrored_cyl("Vent2", 0.06, 0.5, (0.75, 0.55, 0.85), mat_dark, True, True)
    create_mirrored_cyl("Vent3", 0.06, 0.5, (0.55, 0.75, 0.85), mat_dark, True, True)

    # Apply all cutters to the main object
    for cut in cutters:
        bool_mod = obj.modifiers.new("Bool_" + cut.name.split("_")[-1], 'BOOLEAN')
        bool_mod.object = cut
        bool_mod.solver = 'EXACT'

    # Final Micro-Bevel for edge catch/highlights
    bev_final = obj.modifiers.new("Bevel_Final", 'BEVEL')
    bev_final.limit_method = 'ANGLE'
    bev_final.angle_limit = 0.6  # approx 34 degrees
    bev_final.width = 0.008
    bev_final.segments = 3
    bev_final.use_clamp_overlap = True
    bev_final.harden_normals = True

    # === Step 5: Positioning & Rigging ===
    empty_rig = bpy.data.objects.new(object_name + "_Rig", None)
    empty_rig.location = Vector(location)
    empty_rig.scale = (scale, scale, scale)
    scene.collection.objects.link(empty_rig)

    obj.parent = empty_rig
    for c in cutters:
        c.parent = empty_rig

    return f"Created Procedural Hard-Surface Crate '{object_name}' with 11 non-destructive boolean cutters at {location}."

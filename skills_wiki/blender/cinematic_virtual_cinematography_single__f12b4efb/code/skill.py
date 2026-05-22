def create_cinematic_studio(
    scene_name: str = "Scene",
    setup_name: str = "CinematicStudio",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    light_energy: float = 1500.0,
    light_color: tuple = (1.0, 0.95, 0.9),
    backdrop_color: tuple = (0.05, 0.05, 0.05),
    **kwargs
) -> str:
    """
    Create a cinematic single-source rim-lighting environment in the active Blender scene.
    Best used to dramatically light a subject placed at the provided `location`.

    Args:
        scene_name: Name of the target scene.
        setup_name: Prefix for created objects.
        location: (x, y, z) world-space position. Represents the center of the studio where a subject should stand.
        scale: Uniform scale factor for the studio size and light distance.
        light_energy: Power of the rim light.
        light_color: (R, G, B) color of the rim light.
        backdrop_color: (R, G, B) dark base color for the cyclorama backdrop.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Enforce Engine & World Settings
    scene.render.engine = 'CYCLES'  # Essential for the bounce-light fill effect
    
    if scene.world and scene.world.node_tree:
        bg_node = scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0, 0, 0, 1)  # Pure black
            bg_node.inputs[1].default_value = 0.0           # Nullify world ambient light

    base_loc = Vector(location)

    # 2. Procedural Cyclorama (Curved Backdrop)
    mesh = bpy.data.meshes.new(name=f"{setup_name}_Cyclorama_Mesh")
    backdrop_obj = bpy.data.objects.new(f"{setup_name}_Cyclorama", mesh)
    scene.collection.objects.link(backdrop_obj)

    bm = bmesh.new()
    
    # Dimensions
    w = 15.0 * scale
    d_front = -10.0 * scale
    d_back = 4.0 * scale
    h_top = 10.0 * scale
    corner_radius = 3.0 * scale

    # Create profile curve in YZ plane
    v1 = bm.verts.new((0, d_front, 0))
    v2 = bm.verts.new((0, d_back, 0))
    v3 = bm.verts.new((0, d_back, h_top))
    bm.edges.new((v1, v2))
    bm.edges.new((v2, v3))

    # Bevel the 90-degree corner vertex to create the smooth cyclorama sweep
    bmesh.ops.bevel(
        bm, 
        geom=[v2], 
        offset=corner_radius, 
        offset_type='OFFSET', 
        segments=32, 
        profile=0.5, 
        vertex_only=True
    )

    # Extrude along -X to create the surface (extruding -X ensures correct normal orientation)
    edges = list(bm.edges)
    extrude_res = bmesh.ops.extrude_edge_only(bm, edges=edges)
    extruded_verts = [v for v in extrude_res['geom'] if isinstance(v, bmesh.types.BMVert)]

    bmesh.ops.translate(bm, verts=extruded_verts, vec=(-w, 0, 0))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(w / 2, 0, 0))  # Center on X axis

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    for p in mesh.polygons:
        p.use_smooth = True

    # Backdrop Material (Dark, rough, non-reflective)
    mat = bpy.data.materials.new(name=f"{setup_name}_Backdrop_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*backdrop_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8
    backdrop_obj.data.materials.append(mat)
    backdrop_obj.location = base_loc

    # 3. Cinematic Area Light (The Core Skill)
    light_data = bpy.data.lights.new(name=f"{setup_name}_RimLight", type='AREA')
    light_data.energy = light_energy
    light_data.color = light_color
    light_data.size = 2.5 * scale
    light_data.shape = 'RECTANGLE'
    light_data.size_y = 1.0 * scale

    light_obj = bpy.data.objects.new(name=f"{setup_name}_RimLight", object_data=light_data)
    scene.collection.objects.link(light_obj)

    # Place light in the "Outside" zone: Behind and above the subject
    light_pos = base_loc + Vector((0, 1.5 * scale, 3.5 * scale))
    light_obj.location = light_pos

    # Target the light slightly above the origin (center of mass of a typical subject)
    target_pos = base_loc + Vector((0, 0, 1.0 * scale))
    direction = target_pos - light_pos
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # 4. Reference Camera (Placed in the "Inside" zone)
    cam_data = bpy.data.cameras.new(name=f"{setup_name}_Camera")
    cam_data.lens = 50 
    cam_obj = bpy.data.objects.new(name=f"{setup_name}_Camera", object_data=cam_data)
    scene.collection.objects.link(cam_obj)

    cam_pos = base_loc + Vector((0, -8.0 * scale, 1.5 * scale))
    cam_obj.location = cam_pos
    cam_direction = target_pos - cam_pos
    cam_obj.rotation_euler = cam_direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created Cinematic Studio '{setup_name}' at {location}. Enabled Cycles. Add a subject at {location} and view through {cam_obj.name} in Rendered mode to see the effect."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "ArchScaffold",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create an Architectural Scene Scaffold in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects and collections.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the walls.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scene.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Master Controller & Collections ===
    # Create an Empty to control the entire scaffold
    empty_data = bpy.data.objects.new(object_name, None)
    empty_data.empty_display_type = 'PLAIN_AXES'
    empty_data.empty_display_size = 2 * scale
    empty_data.location = Vector(location)
    scene.collection.objects.link(empty_data)

    # Establish architectural collections
    col_names = ["Arch_Meshes", "Arch_Lights", "Arch_Cameras"]
    collections = {}
    for name in col_names:
        prefixed_name = f"{object_name}_{name}"
        if prefixed_name not in bpy.data.collections:
            new_col = bpy.data.collections.new(prefixed_name)
            scene.collection.children.link(new_col)
        collections[name] = bpy.data.collections[prefixed_name]

    # === Step 2: Build Base Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9 # Matte wall paint

    # === Step 3: Procedural Geometry (Walls & Floor) ===
    thickness = 0.5 * scale
    height = 5.0 * scale
    length = 10.0 * scale

    # 3a. L-Shaped Walls
    wall_mesh = bpy.data.meshes.new(f"{object_name}_WallMesh")
    wall_obj = bpy.data.objects.new(f"{object_name}_Walls", wall_mesh)
    collections["Arch_Meshes"].objects.link(wall_obj)
    wall_obj.parent = empty_data
    
    bm_wall = bmesh.new()
    v1 = bm_wall.verts.new((0, 0, 0))
    v2 = bm_wall.verts.new((length, 0, 0))
    v3 = bm_wall.verts.new((length, thickness, 0))
    v4 = bm_wall.verts.new((thickness, thickness, 0))
    v5 = bm_wall.verts.new((thickness, length, 0))
    v6 = bm_wall.verts.new((0, length, 0))
    
    f_bottom = bm_wall.faces.new((v1, v2, v3, v4, v5, v6))
    res = bmesh.ops.extrude_face_region(bm_wall, geom=[f_bottom])
    extruded_verts = [elem for elem in res['geom'] if isinstance(elem, bmesh.types.BMVert)]
    bmesh.ops.translate(bm_wall, vec=Vector((0, 0, height)), verts=extruded_verts)
    
    bmesh.ops.recalc_face_normals(bm_wall, faces=bm_wall.faces)
    bm_wall.to_mesh(wall_mesh)
    bm_wall.free()
    wall_obj.data.materials.append(mat)

    # 3b. Floor
    floor_mesh = bpy.data.meshes.new(f"{object_name}_FloorMesh")
    floor_obj = bpy.data.objects.new(f"{object_name}_Floor", floor_mesh)
    collections["Arch_Meshes"].objects.link(floor_obj)
    floor_obj.parent = empty_data
    floor_obj.location = (length/2, length/2, 0)
    
    bm_floor = bmesh.new()
    s = length / 2
    fv1 = bm_floor.verts.new((-s, -s, 0))
    fv2 = bm_floor.verts.new((s, -s, 0))
    fv3 = bm_floor.verts.new((s, s, 0))
    fv4 = bm_floor.verts.new((-s, s, 0))
    bm_floor.faces.new((fv1, fv2, fv3, fv4))
    
    bm_floor.to_mesh(floor_mesh)
    bm_floor.free()
    floor_obj.data.materials.append(mat)

    # === Step 4: Architectural Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaData", type='AREA')
    light_data.energy = 500.0 * (scale ** 2)
    light_data.size = 5.0 * scale
    light_data.shape = 'SQUARE'
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    collections["Arch_Lights"].objects.link(light_obj)
    light_obj.parent = empty_data
    light_obj.location = (length/2, length/2, height - (0.5 * scale))

    # === Step 5: Camera Setup ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_CamData")
    cam_data.lens = 24.0 # Wide angle, standard for interiors
    
    cam_obj = bpy.data.objects.new(name=f"{object_name}_Camera", object_data=cam_data)
    collections["Arch_Cameras"].objects.link(cam_obj)
    cam_obj.parent = empty_data
    cam_obj.location = (length * 0.8, length * 0.8, height * 0.6)
    
    # Point camera at the corner
    target_pos = Vector((thickness, thickness, height * 0.4))
    direction = target_pos - Vector(cam_obj.location)
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # === Step 6: Render Settings ===
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'use_denoising'):
        scene.cycles.use_denoising = True
    scene.cycles.samples = 128

    return f"Created '{object_name}' Architectural Scaffold at {location} with organized collections, Area Light, and Wide-Angle Camera."

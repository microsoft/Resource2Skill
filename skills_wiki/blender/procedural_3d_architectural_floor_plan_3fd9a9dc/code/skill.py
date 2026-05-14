def create_object(
    scene_name: str = "Scene",
    object_name: str = "3DFloorPlan",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.9, 0.9),
    **kwargs,
) -> str:
    """
    Create a Procedural 3D Architectural Floor Plan in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created wall object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the walls in 0-1 range.
        **kwargs: 
            floor_color: (R, G, B) color for the floor.
            wall_height: Vertical height of the walls.
            wall_thickness: Thickness applied via Solidify.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Configurable parameters
    floor_color = kwargs.get("floor_color", (0.5, 0.35, 0.2))
    wall_height = kwargs.get("wall_height", 2.5)
    wall_thickness = kwargs.get("wall_thickness", 0.2)

    # Define the floor plan layout as a list of line segments (x1, y1, x2, y2)
    # Gaps in the lines represent doorways
    wall_segments = [
        # Exterior Bottom (with front door gap)
        (0, 0, 4.5, 0), (5.5, 0, 10, 0),
        # Exterior Right
        (10, 0, 10, 8),
        # Exterior Top
        (10, 8, 0, 8),
        # Exterior Left
        (0, 8, 0, 0),
        # Interior vertical wall separating left rooms from right hall
        (4, 0, 4, 3.5), (4, 4.5, 4, 8), 
        # Interior horizontal wall separating top left and bottom left rooms
        (0, 4, 1.5, 4), (2.5, 4, 4, 4), 
        # Interior small bathroom wall
        (7, 8, 7, 5), (7, 5, 8.5, 5), (9.5, 5, 10, 5)
    ]

    # === Step 1: Create Wall Geometry ===
    mesh_walls = bpy.data.meshes.new(object_name + "_Mesh")
    obj_walls = bpy.data.objects.new(object_name, mesh_walls)
    scene.collection.objects.link(obj_walls)

    bm = bmesh.new()
    for seg in wall_segments:
        x1, y1, x2, y2 = seg
        v1 = bm.verts.new((x1, y1, 0))
        v2 = bm.verts.new((x2, y2, 0))
        v3 = bm.verts.new((x2, y2, wall_height))
        v4 = bm.verts.new((x1, y1, wall_height))
        bm.faces.new((v1, v2, v3, v4))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh_walls)
    bm.free()

    # Apply Solidify for thickness
    mod_solidify = obj_walls.modifiers.new(name="Wall_Thickness", type='SOLIDIFY')
    mod_solidify.thickness = wall_thickness
    mod_solidify.offset = 0  # Center thickness to align corners better

    # === Step 2: Create Floor Geometry ===
    mesh_floor = bpy.data.meshes.new(object_name + "_Floor_Mesh")
    obj_floor = bpy.data.objects.new(object_name + "_Floor", mesh_floor)
    scene.collection.objects.link(obj_floor)

    bm_floor = bmesh.new()
    # Create a boundary floor that covers the 10x8 footprint
    v1 = bm_floor.verts.new((0, 0, 0))
    v2 = bm_floor.verts.new((10, 0, 0))
    v3 = bm_floor.verts.new((10, 8, 0))
    v4 = bm_floor.verts.new((0, 8, 0))
    bm_floor.faces.new((v1, v2, v3, v4))
    bm_floor.to_mesh(mesh_floor)
    bm_floor.free()

    # Parent floor to walls for easy transformation
    obj_floor.parent = obj_walls

    # === Step 3: Build Materials ===
    # Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall_Mat")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_wall.inputs['Roughness'].default_value = 0.8
    obj_walls.data.materials.append(mat_wall)

    # Floor Material
    mat_floor = bpy.data.materials.new(name=f"{object_name}_Floor_Mat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs['Base Color'].default_value = (*floor_color, 1.0)
        bsdf_floor.inputs['Roughness'].default_value = 0.3
    obj_floor.data.materials.append(mat_floor)

    # === Step 4: Position & Scale ===
    obj_walls.location = Vector(location)
    
    # We apply scale cautiously. Since Solidify thickness is affected by object scale,
    # we usually want to apply scale if we scale the object.
    obj_walls.scale = (scale, scale, scale)
    
    # Ensure view layer updates
    bpy.context.view_layer.update()

    return f"Created procedural 3D floor plan '{object_name}' (Walls + Floor) at {location} scaled by {scale}."

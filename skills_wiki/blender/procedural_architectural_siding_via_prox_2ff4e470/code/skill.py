def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSiding",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.85, 0.83),  # Off-white house paint
    **kwargs,
) -> str:
    """
    Create a procedural Board and Batten wall using Proxy-Volume Boolean intersections.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color of the wall.
        **kwargs: 
            wall_width (float): Total width of the wall.
            eave_height (float): Height of the wall at the edges.
            ridge_height (float): Peak height of the roof.
            batten_width (float): Width of vertical siding strips.
            batten_spacing (float): Distance between siding strips.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # --- Parameters ---
    width = kwargs.get('wall_width', 6.0)
    eave_height = kwargs.get('eave_height', 3.0)
    ridge_height = kwargs.get('ridge_height', 5.0)
    batten_width = kwargs.get('batten_width', 0.06)
    batten_depth = kwargs.get('batten_depth', 0.03)
    batten_spacing = kwargs.get('batten_spacing', 0.4)
    
    window_size = kwargs.get('window_size', (1.2, 1.0, 1.5))
    window_loc = kwargs.get('window_loc', (width / 2.0, 0.0, eave_height * 0.5))

    # --- Materials ---
    mat_wall = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_wall.inputs["Roughness"].default_value = 0.9

    mat_batten = bpy.data.materials.new(name=f"{object_name}_BattenMat")
    mat_batten.use_nodes = True
    bsdf_batten = mat_batten.node_tree.nodes.get("Principled BSDF")
    if bsdf_batten:
        # Slightly darker for the battens to enhance ambient occlusion visually
        darker_tint = (material_color[0]*0.95, material_color[1]*0.95, material_color[2]*0.95)
        bsdf_batten.inputs["Base Color"].default_value = (*darker_tint, 1.0)
        bsdf_batten.inputs["Roughness"].default_value = 0.8

    # --- Master Empty ---
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.empty_display_type = 'ARROWS'
    master_empty.empty_display_size = 2.0
    collection.objects.link(master_empty)

    # --- Step 1: Base Wall Geometry (Flat Gable Profile) ---
    bm_wall = bmesh.new()
    v1 = bm_wall.verts.new((0, 0, 0))
    v2 = bm_wall.verts.new((width, 0, 0))
    v3 = bm_wall.verts.new((width, 0, eave_height))
    v4 = bm_wall.verts.new((width / 2.0, 0, ridge_height))
    v5 = bm_wall.verts.new((0, 0, eave_height))
    bm_wall.faces.new((v1, v2, v3, v4, v5))
    
    mesh_wall = bpy.data.meshes.new(f"{object_name}_ProfileMesh")
    bm_wall.to_mesh(mesh_wall)
    bm_wall.free()

    # --- Step 2: The Visual Background Wall ---
    wall_obj = bpy.data.objects.new(f"{object_name}_BackgroundWall", mesh_wall)
    wall_obj.data.materials.append(mat_wall)
    wall_obj.parent = master_empty
    collection.objects.link(wall_obj)
    
    mod_wall_solidify = wall_obj.modifiers.new(name="Thickness", type='SOLIDIFY')
    mod_wall_solidify.thickness = 0.1
    mod_wall_solidify.offset = 1.0  # Extrude backwards (positive Y) so front stays at Y=0

    # --- Step 3: The Proxy Cutter Volume ---
    # This acts as the boundary bounding box that crops the tall battens to the roofline
    proxy_cutter_obj = bpy.data.objects.new(f"{object_name}_ProxyCutter", mesh_wall)
    proxy_cutter_obj.parent = master_empty
    collection.objects.link(proxy_cutter_obj)
    
    mod_proxy_solidify = proxy_cutter_obj.modifiers.new(name="IntersectionVolume", type='SOLIDIFY')
    mod_proxy_solidify.thickness = batten_depth * 10.0  # Make it extremely thick
    mod_proxy_solidify.offset = 0.0  # Center it over Y=0 so it fully encapsulates the battens
    
    proxy_cutter_obj.display_type = 'WIRE'
    proxy_cutter_obj.hide_render = True

    # --- Step 4: The Batten Array ---
    bm_batten = bmesh.new()
    bmesh.ops.create_cube(bm_batten, size=1.0)
    # Scale to dimensions. Height is made taller than the ridge so it spans the whole proxy volume
    total_batten_height = ridge_height + 1.0
    bmesh.ops.scale(bm_batten, vec=(batten_width, batten_depth, total_batten_height), verts=bm_batten.verts)
    # Translate so bottom is at Z=0, and the back face sits against the wall (Y=0)
    bmesh.ops.translate(bm_batten, vec=(batten_width/2, -batten_depth/2, total_batten_height/2), verts=bm_batten.verts)
    
    mesh_batten = bpy.data.meshes.new(f"{object_name}_BattenMesh")
    bm_batten.to_mesh(mesh_batten)
    bm_batten.free()
    
    batten_obj = bpy.data.objects.new(f"{object_name}_Battens", mesh_batten)
    batten_obj.data.materials.append(mat_batten)
    batten_obj.parent = master_empty
    collection.objects.link(batten_obj)

    # Batten Modifier 1: Array horizontally
    mod_array = batten_obj.modifiers.new(name="HorizontalArray", type='ARRAY')
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    mod_array.constant_offset_displace = (batten_spacing, 0, 0)
    mod_array.count = int(width / batten_spacing) + 1
    
    # Batten Modifier 2: Intersect with Proxy Volume (Cropping to Roofline)
    mod_bool_int = batten_obj.modifiers.new(name="CropToRoofline", type='BOOLEAN')
    mod_bool_int.operation = 'INTERSECT'
    mod_bool_int.object = proxy_cutter_obj
    mod_bool_int.solver = 'EXACT'

    # --- Step 5: Window Hole Cutter ---
    bm_win = bmesh.new()
    bmesh.ops.create_cube(bm_win, size=1.0)
    bmesh.ops.scale(bm_win, vec=window_size, verts=bm_win.verts)
    bmesh.ops.translate(bm_win, vec=window_loc, verts=bm_win.verts)
    
    mesh_win = bpy.data.meshes.new(f"{object_name}_WindowCutterMesh")
    bm_win.to_mesh(mesh_win)
    bm_win.free()
    
    win_cutter_obj = bpy.data.objects.new(f"{object_name}_WindowCutter", mesh_win)
    win_cutter_obj.parent = master_empty
    collection.objects.link(win_cutter_obj)
    
    win_cutter_obj.display_type = 'WIRE'
    win_cutter_obj.hide_render = True
    
    # Punch hole in the background wall
    mod_wall_diff = wall_obj.modifiers.new(name="CutWindow", type='BOOLEAN')
    mod_wall_diff.operation = 'DIFFERENCE'
    mod_wall_diff.object = win_cutter_obj
    mod_wall_diff.solver = 'EXACT'
    
    # Punch hole in the battens
    mod_batten_diff = batten_obj.modifiers.new(name="CutWindow", type='BOOLEAN')
    mod_batten_diff.operation = 'DIFFERENCE'
    mod_batten_diff.object = win_cutter_obj
    mod_batten_diff.solver = 'EXACT'

    # --- Finalize Transforms ---
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)

    return f"Created Procedural Siding System '{object_name}' at {location} (Includes Wall, Battens, Proxy Volume, and Window Cutter)"

def create_object(
    scene_name: str = "Scene",
    object_name: str = "LazyBuilding",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.15, 0.1),
    **kwargs,
) -> str:
    """
    Create a 2.5D Parallax Building Facade in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created building hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the exterior wall.
        **kwargs: 
            grid_columns (int): Number of windows horizontally (default: 3)
            grid_rows (int): Number of windows vertically (default: 4)
            interior_color (tuple): RGB color for the interior emission (default: warm light)

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Extract kwargs
    grid_columns = kwargs.get('grid_columns', 3)
    grid_rows = kwargs.get('grid_rows', 4)
    interior_color = kwargs.get('interior_color', (1.0, 0.7, 0.3))

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    collection = scene.collection

    # ==========================================
    # Step 1: Create Materials
    # ==========================================
    
    # 1A. Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall")
    mat_wall.use_nodes = True
    wall_bsdf = mat_wall.node_tree.nodes.get("Principled BSDF")
    if wall_bsdf:
        wall_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        wall_bsdf.inputs["Roughness"].default_value = 0.9

    # 1B. Glass Material (Mix of Glossy and Transparent)
    mat_glass = bpy.data.materials.new(name=f"{object_name}_Glass")
    mat_glass.use_nodes = True
    mat_glass.blend_method = 'HASHED'  # Crucial for EEVEE transparency
    mat_glass.shadow_method = 'NONE'
    
    nodes = mat_glass.node_tree.nodes
    links = mat_glass.node_tree.links
    nodes.clear()
    
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_glossy = nodes.new(type='ShaderNodeBsdfGlossy')
    node_transp = nodes.new(type='ShaderNodeBsdfTransparent')
    
    node_glossy.inputs["Roughness"].default_value = 0.05
    node_mix.inputs["Fac"].default_value = 0.15 # 15% Glossy, 85% Transparent
    
    links.new(node_transp.outputs[0], node_mix.inputs[1])
    links.new(node_glossy.outputs[0], node_mix.inputs[2])
    links.new(node_mix.outputs[0], node_out.inputs[0])

    # 1C. Interior Emission Material
    mat_interior = bpy.data.materials.new(name=f"{object_name}_Interior")
    mat_interior.use_nodes = True
    int_nodes = mat_interior.node_tree.nodes
    int_links = mat_interior.node_tree.links
    int_nodes.clear()
    
    int_out = int_nodes.new(type='ShaderNodeOutputMaterial')
    int_emit = int_nodes.new(type='ShaderNodeEmission')
    int_emit.inputs["Color"].default_value = (*interior_color, 1.0)
    int_emit.inputs["Strength"].default_value = 5.0
    int_links.new(int_emit.outputs[0], int_out.inputs[0])

    # ==========================================
    # Step 2: Build Facade Geometry
    # ==========================================
    mesh_facade = bpy.data.meshes.new(f"{object_name}_Facade_Mesh")
    obj_facade = bpy.data.objects.new(f"{object_name}_Facade", mesh_facade)
    
    # Assign materials (Index 0: Wall, Index 1: Glass)
    mesh_facade.materials.append(mat_wall)
    mesh_facade.materials.append(mat_glass)

    bm = bmesh.new()
    
    # Generate Grid Vertices centered at origin
    for y in range(grid_rows + 1):
        for x in range(grid_columns + 1):
            cx = x - (grid_columns / 2.0)
            cy = y - (grid_rows / 2.0)
            bm.verts.new((cx, cy, 0))
    
    bm.verts.ensure_lookup_table()
    
    # Generate Grid Faces
    window_faces = []
    for y in range(grid_rows):
        for x in range(grid_columns):
            v1 = bm.verts[y * (grid_columns + 1) + x]
            v2 = bm.verts[y * (grid_columns + 1) + x + 1]
            v3 = bm.verts[(y + 1) * (grid_columns + 1) + x + 1]
            v4 = bm.verts[(y + 1) * (grid_columns + 1) + x]
            f = bm.faces.new((v1, v2, v3, v4))
            window_faces.append(f)
            
    # Inset to create frames and recessed windows
    # depth=-0.1 pushes the inner face along -Z relative to normal
    bmesh.ops.inset_individual(bm, faces=window_faces, thickness=0.15, depth=-0.15)
    
    # Assign material indices
    for f in bm.faces:
        if f in window_faces:
            f.material_index = 1  # The shrunken original faces become Glass
        else:
            f.material_index = 0  # The newly generated frames become Wall
            
    bm.to_mesh(mesh_facade)
    bm.free()

    # Rotate upright (Z becomes -Y, so facade faces forward (-Y))
    obj_facade.rotation_euler = (math.radians(90), 0, 0)

    # ==========================================
    # Step 3: Build Interior Emissive Box
    # ==========================================
    mesh_box = bpy.data.meshes.new(f"{object_name}_Interior_Mesh")
    obj_box = bpy.data.objects.new(f"{object_name}_Interior", mesh_box)
    mesh_box.materials.append(mat_interior)
    
    bm_box = bmesh.new()
    bmesh.ops.create_cube(bm_box, size=1.0)
    
    # Scale cube to match the back of the facade
    bmesh.ops.scale(bm_box, vec=(grid_columns, grid_rows, 1.0), verts=bm_box.verts)
    # Translate behind the recessed windows (Local Z = -0.7)
    bmesh.ops.translate(bm_box, vec=(0, 0, -0.7), verts=bm_box.verts)
    
    bm_box.to_mesh(mesh_box)
    bm_box.free()
    
    # Rotate upright to match facade
    obj_box.rotation_euler = (math.radians(90), 0, 0)

    # ==========================================
    # Step 4: Finalize Hierarchy
    # ==========================================
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.empty_display_type = 'ARROWS'
    parent_empty.empty_display_size = 2.0
    
    collection.objects.link(parent_empty)
    collection.objects.link(obj_facade)
    collection.objects.link(obj_box)
    
    obj_facade.parent = parent_empty
    obj_box.parent = parent_empty
    
    # Apply global transforms to the parent Empty
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Lazy Building) at {location} with {grid_columns}x{grid_rows} windows."

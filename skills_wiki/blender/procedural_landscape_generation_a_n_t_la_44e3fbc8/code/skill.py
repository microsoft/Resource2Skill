def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralLandscape",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.25, 0.2),
    **kwargs,
) -> str:
    """
    Create a Procedural Landscape in the active Blender scene using A.N.T.Landscape.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created landscape object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the terrain.
        **kwargs: 
            subdivisions (int): Grid resolution (default: 128).
            seed (int): Random variation seed (default: 0).
            array_path (bool): If True, adds an array modifier to make a long path.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Enable A.N.T.Landscape Add-on ===
    # Check if loaded, if not, enable it
    loaded_default, loaded_state = addon_utils.check("ant_landscape")
    if not loaded_state:
        addon_utils.enable("ant_landscape")

    # === Step 2: Generate Landscape Geometry ===
    seed = kwargs.get("seed", 0)
    subdiv = kwargs.get("subdivisions", 128)
    
    # Deselect all objects to ensure we capture only the newly created landscape
    bpy.ops.object.select_all(action='DESELECT')
    
    # Call the landscape operator (wrapped in try-except to handle potential API signature differences)
    try:
        bpy.ops.mesh.landscape_add(
            subdivision_x=subdiv,
            subdivision_y=subdiv,
            mesh_size_x=2.0,
            mesh_size_y=2.0,
            random_seed=seed,
            noise_type='hetero_terrain' # Safe default, creates realistic rocky terrain
        )
    except TypeError:
        # Fallback if specific kwargs are rejected by the current Blender version
        bpy.ops.mesh.landscape_add()

    obj = bpy.context.active_object
    obj.name = object_name
    
    # === Step 3: Modifiers and Shading ===
    bpy.ops.object.shade_smooth()
    
    # Optional: Array modifier to create a continuous path/corridor as mentioned in the video
    if kwargs.get("array_path", False):
        array_mod = obj.modifiers.new(name="PathArray", type='ARRAY')
        array_mod.count = 4
        array_mod.use_relative_offset = True
        array_mod.relative_offset_displace = (0, 1, 0) # Extend along Y axis

    # === Step 4: Build Terrain Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.95
        bsdf.inputs["Specular IOR Level"].default_value = 0.05
        
    # Assign material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 5: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    return f"Created '{object_name}' (Procedural Landscape) at {location} with {subdiv}x{subdiv} subdivisions."

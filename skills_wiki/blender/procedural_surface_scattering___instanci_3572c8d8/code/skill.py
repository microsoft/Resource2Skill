def create_procedural_sugar_coating(
    scene_name: str = "Scene",
    base_object_name: str = "JellyCandy",
    crystal_object_name: str = "SugarCrystal",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    candy_color: tuple = (0.8, 0.02, 0.05, 1.0),
    density: float = 2500.0,
    crystal_scale_min: float = 0.01,
    crystal_scale_max: float = 0.04,
    **kwargs,
) -> str:
    """
    Create a jelly candy coated in procedural sugar crystals using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Name for the main candy object.
        crystal_object_name: Name for the instance crystal object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        candy_color: (R, G, B, A) base color for the jelly.
        density: Number of points to scatter on the faces.
        crystal_scale_min: Minimum scale multiplier for the sugar grains.
        crystal_scale_max: Maximum scale multiplier for the sugar grains.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create the base candy object (Torus) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.45, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = base_object_name
    base_obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    
    subsurf = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Create the sugar crystal instance object ===
    # Placed out of sight; it will only be used as referenced data
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0], location[1], location[2] - 10))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = crystal_object_name
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Setup Materials ===
    # 3a. Jelly Material
    candy_mat = bpy.data.materials.new(name=f"{base_object_name}_Mat")
    candy_mat.use_nodes = True
    bsdf_candy = candy_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        bsdf_candy.inputs["Base Color"].default_value = candy_color
        bsdf_candy.inputs["Roughness"].default_value = 0.15
        # Subsurface settings for gummy look (handles differences in Blender 3.x vs 4.x)
        if "Subsurface Weight" in bsdf_candy.inputs:
            bsdf_candy.inputs["Subsurface Weight"].default_value = 1.0
            bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.1, 0.1)
        elif "Subsurface" in bsdf_candy.inputs:
            bsdf_candy.inputs["Subsurface"].default_value = 1.0
            bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.1, 0.1)
            bsdf_candy.inputs["Subsurface Color"].default_value = candy_color
    base_obj.data.materials.append(candy_mat)

    # 3b. Sugar Material
    crystal_mat = bpy.data.materials.new(name=f"{crystal_object_name}_Mat")
    crystal_mat.use_nodes = True
    bsdf_crystal = crystal_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_crystal:
        bsdf_crystal.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_crystal.inputs["Roughness"].default_value = 0.25
        bsdf_crystal.inputs["IOR"].default_value = 1.55
        if "Transmission Weight" in bsdf_crystal.inputs:
            bsdf_crystal.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in bsdf_crystal.inputs:
            bsdf_crystal.inputs["Transmission"].default_value = 1.0
    crystal_obj.data.materials.append(crystal_mat)

    # === Step 4: Build the Geometry Nodes Tree ===
    node_group = bpy.data.node_groups.new(name="SugarCoating_GN", type="GeometryNodeTree")
    
    # Inputs & Outputs (Blender 4.0 vs 3.x compatibility)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.inputs.new('NodeSocketGeometry', "Geometry")
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    group_in = node_group.nodes.new("NodeGroupInput")
    group_out = node_group.nodes.new("NodeGroupOutput")

    # Core scattering nodes
    distribute = node_group.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute.inputs.get("Density").default_value = density
    
    instance = node_group.nodes.new("GeometryNodeInstanceOnPoints")
    join = node_group.nodes.new("GeometryNodeJoinGeometry")
    
    obj_info = node_group.nodes.new("GeometryNodeObjectInfo")
    obj_info.inputs.get("Object").default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'

    # Random Rotation (0 to math.tau radians on all axes)
    rand_rot = node_group.nodes.new("FunctionNodeRandomValue")
    rand_rot.data_type = 'FLOAT_VECTOR'
    for inp in rand_rot.inputs:
        if inp.name == 'Min' and 'VECTOR' in getattr(inp, 'type', 'VECTOR'):
            inp.default_value = (0.0, 0.0, 0.0)
        elif inp.name == 'Max' and 'VECTOR' in getattr(inp, 'type', 'VECTOR'):
            inp.default_value = (math.tau, math.tau, math.tau)

    # Random Scale (Min to Max Float)
    rand_scale = node_group.nodes.new("FunctionNodeRandomValue")
    rand_scale.data_type = 'FLOAT'
    for inp in rand_scale.inputs:
        if inp.name == 'Min' and 'FLOAT' in getattr(inp, 'type', 'FLOAT'):
            inp.default_value = crystal_scale_min
        elif inp.name == 'Max' and 'FLOAT' in getattr(inp, 'type', 'FLOAT'):
            inp.default_value = crystal_scale_max

    # Link the nodes
    links = node_group.links
    geom_in_socket = group_in.outputs.get("Geometry") or group_in.outputs[0]
    
    # Feed base mesh to Distribute and Join
    links.new(geom_in_socket, distribute.inputs[0])  # Mesh
    links.new(geom_in_socket, join.inputs[0])        # Geometry (multi-input)
    
    # Scatter flow
    links.new(distribute.outputs.get("Points") or distribute.outputs[0], instance.inputs.get("Points") or instance.inputs[0])
    links.new(obj_info.outputs.get("Geometry") or obj_info.outputs[3], instance.inputs.get("Instance") or instance.inputs[2])
    
    # Randomization links
    links.new(rand_rot.outputs[0], instance.inputs.get("Rotation") or instance.inputs[5])
    links.new(rand_scale.outputs[0], instance.inputs.get("Scale") or instance.inputs[6])
    
    # Output flow
    links.new(instance.outputs.get("Instances") or instance.outputs[0], join.inputs[0])
    links.new(join.outputs.get("Geometry") or join.outputs[0], group_out.inputs.get("Geometry") or group_out.inputs[0])

    # === Step 5: Apply Modifier ===
    gn_mod = base_obj.modifiers.new(name="Sugar_Coating_GN", type='NODES')
    gn_mod.node_group = node_group

    # Deselect crystal and ensure base object is selected
    crystal_obj.select_set(False)
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj

    return f"Created '{base_object_name}' with procedural sugar coating (Density: {density}) at {location}."

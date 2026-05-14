def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural Sugar-Coated Candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy candy.
        **kwargs: 
            crystal_density (float): Number of points for the scatter density. Default 5000.
            subdivision_level (int): Subsurf levels for the base. Default 2.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    crystal_density = kwargs.get('crystal_density', 5000.0)
    subdiv_level = kwargs.get('subdivision_level', 2)

    # === Step 1: Create Materials ===
    # Candy Material (Transmissive/Gummy)
    candy_mat = bpy.data.materials.new(name=f"{object_name}_Candy_Mat")
    candy_mat.use_nodes = True
    bsdf_candy = candy_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        # Handle RGB length correctly
        color_val = (*material_color, 1.0) if len(material_color) == 3 else material_color
        bsdf_candy.inputs['Base Color'].default_value = color_val
        bsdf_candy.inputs['Roughness'].default_value = 0.2
        # Cross-version compatibility for Transmission
        if 'Transmission Weight' in bsdf_candy.inputs:
            bsdf_candy.inputs['Transmission Weight'].default_value = 0.85
        elif 'Transmission' in bsdf_candy.inputs:
            bsdf_candy.inputs['Transmission'].default_value = 0.85
        bsdf_candy.inputs['IOR'].default_value = 1.45

    # Sugar Material (Glassy/White)
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_Sugar_Mat")
    sugar_mat.use_nodes = True
    bsdf_sugar = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_sugar:
        bsdf_sugar.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_sugar.inputs['Roughness'].default_value = 0.1
        if 'Transmission Weight' in bsdf_sugar.inputs:
            bsdf_sugar.inputs['Transmission Weight'].default_value = 0.95
        elif 'Transmission' in bsdf_sugar.inputs:
            bsdf_sugar.inputs['Transmission'].default_value = 0.95
        bsdf_sugar.inputs['IOR'].default_value = 1.55

    # === Step 2: Create the Sugar Crystal Instance Object ===
    bpy.ops.mesh.primitive_cube_add(size=0.02, location=location)
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal"
    crystal_obj.data.materials.append(sugar_mat)
    # Hide the source crystal from render and viewport
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Create the Base Candy Object ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, minor_radius=0.4, 
        major_segments=48, minor_segments=24, 
        location=location
    )
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.scale = (scale, scale, scale)
    base_obj.data.materials.append(candy_mat)
    
    # Smooth shading
    for poly in base_obj.data.polygons:
        poly.use_smooth = True

    # Subdivision modifier to smooth it out before scattering
    subsurf = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = subdiv_level
    subsurf.render_levels = subdiv_level

    # === Step 4: Build the Geometry Nodes Tree ===
    gn_mod = base_obj.modifiers.new(name="Sugar Scatter", type='NODES')
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_GN_Tree", type='GeometryNodeTree')
    gn_mod.node_group = node_tree

    # Create Group Input/Output sockets (Cross-version compatible)
    if hasattr(node_tree, "interface"):
        node_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.inputs.new('NodeSocketGeometry', "Geometry")
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_tree.nodes
    links = node_tree.links

    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')
    
    distribute_node = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute_node.inputs['Density'].default_value = crystal_density
    
    obj_info_node = nodes.new('GeometryNodeObjectInfo')
    obj_info_node.inputs['Object'].default_value = crystal_obj
    obj_info_node.transform_space = 'ORIGINAL'
    
    # Random Vector for Rotation (0 to math.tau radians on all axes)
    rand_rot_node = nodes.new('FunctionNodeRandomValue')
    rand_rot_node.data_type = 'FLOAT_VECTOR'
    rand_rot_node.inputs[0].default_value = (0.0, 0.0, 0.0) # Min
    rand_rot_node.inputs[1].default_value = (math.tau, math.tau, math.tau) # Max
    
    # Random Float for Scale
    rand_scale_node = nodes.new('FunctionNodeRandomValue')
    rand_scale_node.data_type = 'FLOAT'
    rand_scale_node.inputs[0].default_value = 0.5 # Min
    rand_scale_node.inputs[1].default_value = 1.5 # Max
    
    instance_node = nodes.new('GeometryNodeInstanceOnPoints')
    join_node = nodes.new('GeometryNodeJoinGeometry')

    # Link the nodes together
    # Original Mesh to Distribute and Join
    links.new(input_node.outputs[0], distribute_node.inputs['Mesh'])
    links.new(input_node.outputs[0], join_node.inputs['Geometry'])
    
    # Distribute -> Instance
    links.new(distribute_node.outputs['Points'], instance_node.inputs['Points'])
    
    # Object Info -> Instance Mesh
    links.new(obj_info_node.outputs['Geometry'], instance_node.inputs['Instance'])
    
    # Random Values -> Instance Transforms
    links.new(rand_rot_node.outputs[0], instance_node.inputs['Rotation'])
    links.new(rand_scale_node.outputs[0], instance_node.inputs['Scale'])
    
    # Instances -> Join
    links.new(instance_node.outputs['Instances'], join_node.inputs['Geometry'])
    
    # Join -> Output
    links.new(join_node.outputs['Geometry'], output_node.inputs[0])

    return f"Created '{object_name}' candy with procedurally scattered '{crystal_obj.name}' sugar crystals at {location}."

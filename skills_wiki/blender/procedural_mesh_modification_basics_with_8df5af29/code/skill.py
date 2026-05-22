def create_object(
    scene_name: str = "Scene",
    object_name: str = "GeoNodesObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    subdivision_level: int = 3,
    edge_crease: float = 0.0,
    translation: tuple = (0, 0, 0),
    rotation_euler: tuple = (0, 0, 0), # in degrees
    transform_scale: tuple = (1, 1, 1),
    use_cube_primitive_node: bool = False, # If True, Group Input is replaced by a Cube node
    **kwargs,
) -> str:
    """
    Create a mesh object with a Geometry Nodes modifier for procedural modification.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        subdivision_level: Level for the Subdivision Surface node.
        edge_crease: Edge Crease value for the Subdivision Surface node (0.0 to 1.0).
        translation: (X, Y, Z) translation for the Transform Geometry node.
        rotation_euler: (X, Y, Z) rotation in degrees for the Transform Geometry node.
        transform_scale: (X, Y, Z) scale for the Transform Geometry node.
        use_cube_primitive_node: If True, replaces Group Input with an internal Cube primitive.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'GeoNodesObject' at (0, 0, 0) with Geometry Nodes."
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a new mesh object (e.g., a cube)
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # --- Create Material ---
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*material_color, 1.0) # RGB + Alpha

    # --- Add Geometry Nodes Modifier ---
    gn_modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # Create a new Geometry Node tree if not already existing (unlikely given naming)
    node_tree_name = f"{object_name}_GeoNodes_Setup"
    if node_tree_name not in bpy.data.node_groups:
        node_tree = bpy.data.node_groups.new(name=node_tree_name, type='GeometryNodeTree')
    else:
        node_tree = bpy.data.node_groups[node_tree_name]
        # Clear existing nodes if we're creating a fresh setup
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

    gn_modifier.node_group = node_tree

    # --- Setup Geometry Nodes ---
    nodes = node_tree.nodes
    links = node_tree.links

    # Add Group Input and Group Output (default)
    group_input = nodes.new(type='NodeGroupInput')
    group_input.location = Vector((-800, 0))
    group_output = nodes.new(type='NodeGroupOutput')
    group_output.location = Vector((800, 0))

    # Optional: Replace Group Input with a Cube Primitive Node
    if use_cube_primitive_node:
        cube_node = nodes.new(type='GeometryNodeMeshCube')
        cube_node.location = Vector((-600, 0))
        links.new(cube_node.outputs['Mesh'], group_output.inputs['Geometry'])
        # Remove default link from Group Input to Group Output if replaced
        for link in links:
            if link.from_node == group_input and link.to_node == group_output:
                links.remove(link)
    else:
        # Default connection from Group Input
        # (This is already linked if modifier was added to an existing object)
        pass 
    
    # Add Transform Geometry Node
    transform_geom_node = nodes.new(type='GeometryNodeTransform')
    transform_geom_node.location = Vector((-400, 0))
    transform_geom_node.inputs['Translation'].default_value = Vector(translation)
    transform_geom_node.inputs['Rotation'].default_value = (
        math.radians(rotation_euler[0]),
        math.radians(rotation_euler[1]),
        math.radians(rotation_euler[2])
    )
    transform_geom_node.inputs['Scale'].default_value = Vector(transform_scale)

    # Add Subdivision Surface Node
    subdiv_node = nodes.new(type='GeometryNodeSubdivideMesh')
    subdiv_node.location = Vector((0, 0))
    subdiv_node.inputs['Level'].default_value = subdivision_level
    subdiv_node.inputs['Edge Crease'].default_value = edge_crease

    # Add Set Shade Smooth Node
    shade_smooth_node = nodes.new(type='GeometryNodeSetShadeSmooth')
    shade_smooth_node.location = Vector((400, 0))
    shade_smooth_node.inputs['Shade Smooth'].default_value = True

    # --- Connect Nodes ---
    if use_cube_primitive_node:
        links.new(cube_node.outputs['Mesh'], transform_geom_node.inputs['Geometry'])
    else:
        links.new(group_input.outputs['Geometry'], transform_geom_node.inputs['Geometry'])
    
    links.new(transform_geom_node.outputs['Geometry'], subdiv_node.inputs['Mesh'])
    links.new(subdiv_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])
    links.new(shade_smooth_node.outputs['Geometry'], group_output.inputs['Geometry'])

    return f"Created '{object_name}' at {location} with Geometry Nodes setup '{node_tree_name}'."


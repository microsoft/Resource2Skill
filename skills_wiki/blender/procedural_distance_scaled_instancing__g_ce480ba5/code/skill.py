def create_procedural_grid_instances(
    scene_name: str = "Scene",
    object_name: str = "DistanceScaledInstances",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    grid_size: float = 10.0,
    grid_subdivisions: int = 20,
    instance_mesh_type: str = 'CUBE', # Options: 'CUBE', 'UVSPHERE', 'ICOSPHERE'
    min_instance_scale: float = 0.05,
    max_instance_scale: float = 0.5,
    falloff_distance: float = 5.0, # Distance from center for full effect
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Creates a procedural grid of instances whose scale is determined by their distance
    from the object's origin using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created Geometry Nodes object.
        location: (x, y, z) world-space position for the main object.
        scale: Uniform scale factor for the main object.
        grid_size: Size of the initial grid (e.g., 10.0 for a 10x10m grid).
        grid_subdivisions: Number of subdivisions for the grid (e.g., 20 for 20x20 faces).
        instance_mesh_type: Type of mesh to instance ('CUBE', 'UVSPHERE', 'ICOSPHERE').
        min_instance_scale: Minimum scale for instances (at max distance).
        max_instance_scale: Maximum scale for instances (at min distance).
        falloff_distance: The distance from the center where the scaling effect fully applies.
        material_color: (R, G, B) base color in 0-1 range for the instances.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'DistanceScaledInstances' at (0, 0, 0) with Geometry Nodes."
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create a new object to host the Geometry Nodes modifier ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    gn_obj = bpy.context.active_object
    gn_obj.name = object_name
    gn_obj.scale = (scale, scale, scale)

    # --- 2. Add Geometry Nodes modifier ---
    gn_modifier = gn_obj.modifiers.new(name="GeometryNodes", type='NODES')

    # --- 3. Create a new Geometry Node tree ---
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    gn_modifier.node_group = node_tree

    # Clear default nodes (Group Input and Group Output are automatically added)
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # --- 4. Add Geometry Nodes ---
    group_input = node_tree.nodes.new(type='NodeGroupInput')
    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.is_active_output = True # Ensure this is the active output

    # Grid (base geometry)
    grid_node = node_tree.nodes.new(type='GeometryNodeMeshGrid')
    grid_node.location = Vector([-800, 0])
    grid_node.inputs['Size X'].default_value = grid_size
    grid_node.inputs['Size Y'].default_value = grid_size
    grid_node.inputs['Vertices X'].default_value = grid_subdivisions
    grid_node.inputs['Vertices Y'].default_value = grid_subdivisions

    # Mesh to Points
    mesh_to_points_node = node_tree.nodes.new(type='GeometryNodeMeshToPoints')
    mesh_to_points_node.location = Vector([-600, 0])
    mesh_to_points_node.inputs['Radius'].default_value = 0.0 # No visible points, just for instancing

    # Instance on Points
    instance_on_points_node = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
    instance_on_points_node.location = Vector([-200, 0])
    # Placeholder for instance mesh, will be connected below

    # Instance Mesh (Cube, UV Sphere, or Icosphere)
    instance_mesh_node = None
    if instance_mesh_type == 'CUBE':
        instance_mesh_node = node_tree.nodes.new(type='GeometryNodeMeshCube')
        instance_mesh_node.inputs['Size'].default_value = 1.0 # Base size for scaling
    elif instance_mesh_type == 'UVSPHERE':
        instance_mesh_node = node_tree.nodes.new(type='GeometryNodeMeshUVSphere')
        instance_mesh_node.inputs['Radius'].default_value = 0.5
    elif instance_mesh_type == 'ICOSPHERE':
        instance_mesh_node = node_tree.nodes.new(type='GeometryNodeMeshIcoSphere')
        instance_mesh_node.inputs['Radius'].default_value = 0.5
    else:
        print(f"Warning: Unknown instance_mesh_type '{instance_mesh_type}', defaulting to CUBE.")
        instance_mesh_node = node_tree.nodes.new(type='GeometryNodeMeshCube')
        instance_mesh_node.inputs['Size'].default_value = 1.0
    instance_mesh_node.location = Vector([-400, -200])

    # Position node (to get instance position)
    position_node = node_tree.nodes.new(type='GeometryNodeInputPosition')
    position_node.location = Vector([-600, -400])

    # Vector Math (for origin of distance calculation) - can be controlled by a group input later
    # For now, let's use the object's local origin (0,0,0) as the center for distance.
    # Note: If gn_obj is moved, the local origin stays, so the pattern moves with the object.
    # To make it world-space absolute, you'd need to convert object-space position to world-space.
    vector_zero = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_zero.operation = 'MULTIPLY' # Using multiply by 0 to get a zero vector easily
    vector_zero.inputs[0].default_value = (0.0, 0.0, 0.0) # Input doesn't matter, output is 0,0,0
    vector_zero.inputs[1].default_value = (0.0, 0.0, 0.0) # Input doesn't matter, output is 0,0,0
    vector_zero.location = Vector([-400, -400])


    # Distance node
    distance_node = node_tree.nodes.new(type='ShaderNodeVectorMath')
    distance_node.operation = 'DISTANCE'
    distance_node.location = Vector([-200, -400])

    # Map Range to control scale
    map_range_node = node_tree.nodes.new(type='ShaderNodeMapRange')
    map_range_node.location = Vector([0, -400])
    map_range_node.inputs['From Min'].default_value = 0.0
    map_range_node.inputs['From Max'].default_value = falloff_distance
    map_range_node.inputs['To Min'].default_value = max_instance_scale # Closer = larger
    map_range_node.inputs['To Max'].default_value = min_instance_scale # Further = smaller

    # Realize Instances (convert instances to actual mesh)
    realize_instances_node = node_tree.nodes.new(type='GeometryNodeRealizeInstances')
    realize_instances_node.location = Vector([200, 0])

    # Set Material
    set_material_node = node_tree.nodes.new(type='GeometryNodeSetMaterial')
    set_material_node.location = Vector([400, 0])

    # --- 5. Create and assign material ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.get(mat_name)
    if material is None:
        material = bpy.data.materials.new(name=mat_name)
        material.use_nodes = True
        bsdf_node = material.node_tree.nodes["Principled BSDF"]
        bsdf_node.inputs['Base Color'].default_value = (*material_color, 1.0)
    set_material_node.inputs['Material'].default_value = material

    # --- 6. Link nodes ---
    # Grid -> Mesh to Points
    node_tree.links.new(grid_node.outputs['Mesh'], mesh_to_points_node.inputs['Mesh'])

    # Mesh to Points -> Instance on Points
    node_tree.links.new(mesh_to_points_node.outputs['Points'], instance_on_points_node.inputs['Points'])

    # Instance Mesh -> Instance on Points (Instance input)
    node_tree.links.new(instance_mesh_node.outputs['Mesh'], instance_on_points_node.inputs['Instance'])

    # Position -> Distance (Vector 1)
    node_tree.links.new(position_node.outputs['Position'], distance_node.inputs[0])

    # Vector Zero -> Distance (Vector 2)
    node_tree.links.new(vector_zero.outputs['Vector'], distance_node.inputs[1])

    # Distance -> Map Range (Value)
    node_tree.links.new(distance_node.outputs['Value'], map_range_node.inputs['Value'])

    # Map Range -> Instance on Points (Scale)
    node_tree.links.new(map_range_node.outputs['Result'], instance_on_points_node.inputs['Scale'])

    # Instance on Points -> Realize Instances
    node_tree.links.new(instance_on_points_node.outputs['Instances'], realize_instances_node.inputs['Geometry'])

    # Realize Instances -> Set Material
    node_tree.links.new(realize_instances_node.outputs['Geometry'], set_material_node.inputs['Geometry'])

    # Set Material -> Group Output
    node_tree.links.new(set_material_node.outputs['Geometry'], group_output.inputs['Geometry'])

    # --- 7. Finalize ---
    bpy.context.view_layer.objects.active = gn_obj
    gn_obj.select_set(True)

    # Optional: Add parameters to the modifier UI for easy access
    # To add more parameters to the Group Input, you'd define them here.
    # Example: node_tree.inputs.new('NodeSocketFloat', 'Grid Size')
    # Then link group_input.outputs['Grid Size'] to grid_node.inputs['Size X'] etc.
    # For simplicity, we are setting node inputs directly for now.

    return f"Created procedural instancing object '{object_name}' at {location} with Geometry Nodes."


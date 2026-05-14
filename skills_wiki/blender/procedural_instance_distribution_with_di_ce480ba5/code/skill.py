def create_distance_scaled_instances(
    scene_name: str = "Scene",
    object_name: str = "DistanceScaledInstances",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    grid_size_x: float = 5.0,
    grid_size_y: float = 5.0,
    grid_vertices_x: int = 10,
    grid_vertices_y: int = 10,
    instance_rotation_z: float = 45.0, # Degrees
    instance_initial_scale: float = 0.2,
    distance_scale_factor: float = 0.5, # Multiplier for distance effect on scale
    min_instance_scale: float = 0.01,
    instance_object_name: str = "Suzanne",
    **kwargs,
) -> str:
    """
    Creates a procedural instance distribution using Geometry Nodes,
    where instance scale is based on distance from the origin.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the base object (1.0 = default size).
        grid_size_x: Size of the internal grid along X.
        grid_size_y: Size of the internal grid along Y.
        grid_vertices_x: Number of vertices in the internal grid along X.
        grid_vertices_y: Number of vertices in the internal grid along Y.
        instance_rotation_z: Rotation of each instance around its Z-axis in degrees.
        instance_initial_scale: Base scale of each instance before distance scaling.
        distance_scale_factor: Multiplier for the distance attribute when scaling instances.
        min_instance_scale: Minimum scale instances can have after distance calculation.
        instance_object_name: Name of the object to instance (e.g., "Suzanne", "Cube").
                              If not found, a new Suzanne will be created.
        **kwargs: Additional overrides (e.g., subdivision_level, roughness).

    Returns:
        Status string, e.g., "Created 'DistanceScaledInstances' at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Ensure Suzanne (or other instance object) exists ---
    instance_obj = bpy.data.objects.get(instance_object_name)
    if not instance_obj:
        if instance_object_name == "Suzanne":
            bpy.ops.mesh.primitive_monkey_add(
                size=1, enter_editmode=False, align='WORLD',
                location=(0, 0, 0), scale=(1, 1, 1)
            )
            instance_obj = bpy.context.active_object
        elif instance_object_name == "Cube":
            bpy.ops.mesh.primitive_cube_add(
                size=1, enter_editmode=False, align='WORLD',
                location=(0, 0, 0), scale=(1, 1, 1)
            )
            instance_obj = bpy.context.active_object
        else:
            # Fallback to a cube if specified object is not Suzanne/Cube and doesn't exist
            bpy.ops.mesh.primitive_cube_add(
                size=1, enter_editmode=False, align='WORLD',
                location=(0, 0, 0), scale=(1, 1, 1)
            )
            instance_obj = bpy.context.active_object
            instance_object_name = "Cube" # Update name
        instance_obj.name = instance_object_name
        instance_obj.hide_set(True) # Hide the original instance object

    # --- Create Base Object for Geometry Nodes Modifier ---
    bpy.ops.mesh.primitive_cube_add(
        size=0.1, enter_editmode=False, align='WORLD',
        location=location, scale=(scale, scale, scale)
    )
    main_obj = bpy.context.active_object
    main_obj.name = object_name

    # --- Create Geometry Node Tree ---
    node_tree_name = f"{object_name}_GeoNodesTree"
    node_tree = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_tree_name)

    # --- Add Geometry Nodes Modifier ---
    gn_modifier = main_obj.modifiers.new(name=f"{object_name}_GN", type='NODES')
    gn_modifier.node_group = node_tree

    # --- Setup Geometry Node Tree ---
    nodes = node_tree.nodes
    links = node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add Group Input and Output
    group_input = nodes.new(type='NodeGroupInput')
    group_input.location = (-800, 0)
    group_output = nodes.new(type='NodeGroupOutput')
    group_output.location = (1000, 0)

    # Mesh Primitive Grid
    grid_mesh = nodes.new(type='MESH_PRIMITIVE_GRID')
    grid_mesh.location = (-600, 0)
    grid_mesh.width = grid_size_x
    grid_mesh.height = grid_size_y
    grid_mesh.vertices_x = grid_vertices_x
    grid_mesh.vertices_y = grid_vertices_y
    links.new(grid_mesh.outputs['Mesh'], group_output.inputs['Geometry']) # Initial connect for visibility in case of errors

    # Mesh to Points
    mesh_to_points = nodes.new(type='GEOMETRY_NODES_MESH_TO_POINTS')
    mesh_to_points.location = (-300, 0)
    mesh_to_points.mode = 'FACES' # Distribute points on faces
    links.new(grid_mesh.outputs['Mesh'], mesh_to_points.inputs['Mesh'])

    # Object Info (for the instance object)
    object_info = nodes.new(type='GEOMETRY_NODES_OBJECT_INFO')
    object_info.location = (-300, -300)
    object_info.object = instance_obj # Link to our instance object
    object_info.as_instance = True # Treat as instance, not mesh data directly

    # Instance on Points
    instance_on_points = nodes.new(type='GEOMETRY_NODES_INSTANCE_ON_POINTS')
    instance_on_points.location = (0, 0)
    links.new(mesh_to_points.outputs['Points'], instance_on_points.inputs['Points'])
    links.new(object_info.outputs['Geometry'], instance_on_points.inputs['Instance'])

    # Rotate Instances
    rotate_instances = nodes.new(type='GEOMETRY_NODES_ROTATE_INSTANCES')
    rotate_instances.location = (200, 0)
    rotate_instances.rotation.z = math.radians(instance_rotation_z) # Set Z rotation
    links.new(instance_on_points.outputs['Instances'], rotate_instances.inputs['Instances'])

    # Initial Scale Instances
    scale_instances_initial = nodes.new(type='GEOMETRY_NODES_SCALE_INSTANCES')
    scale_instances_initial.location = (400, 0)
    scale_instances_initial.scale = (instance_initial_scale, instance_initial_scale, instance_initial_scale)
    links.new(rotate_instances.outputs['Instances'], scale_instances_initial.inputs['Instances'])

    # Position (to get instance position)
    position_node = nodes.new(type='GEOMETRY_NODES_INPUT_POSITION')
    position_node.location = (400, -300)

    # Vector Math (Distance)
    vector_math_distance = nodes.new(type='GEOMETRY_NODES_VECTOR_MATH')
    vector_math_distance.location = (600, -300)
    vector_math_distance.operation = 'DISTANCE'
    vector_math_distance.inputs[1].default_value = (0,0,0) # Distance from origin
    links.new(position_node.outputs['Position'], vector_math_distance.inputs[0])

    # Math (Multiply & Subtract for scaling based on distance)
    math_multiply = nodes.new(type='SHADER_NODE_MATH')
    math_multiply.location = (750, -300)
    math_multiply.operation = 'MULTIPLY'
    math_multiply.inputs[1].default_value = distance_scale_factor # Adjust sensitivity
    links.new(vector_math_distance.outputs['Value'], math_multiply.inputs[0])

    math_subtract = nodes.new(type='SHADER_NODE_MATH')
    math_subtract.location = (900, -300)
    math_subtract.operation = 'SUBTRACT'
    math_subtract.inputs[0].default_value = 1.0 # Base scale offset
    links.new(math_multiply.outputs['Value'], math_subtract.inputs[1])

    math_clamp = nodes.new(type='SHADER_NODE_MATH')
    math_clamp.location = (1050, -300)
    math_clamp.operation = 'MAXIMUM'
    math_clamp.inputs[1].default_value = min_instance_scale # Ensure minimum scale
    links.new(math_subtract.outputs['Value'], math_clamp.inputs[0])


    # Final Scale Instances (driven by distance)
    scale_instances_final = nodes.new(type='GEOMETRY_NODES_SCALE_INSTANCES')
    scale_instances_final.location = (600, 0)
    links.new(scale_instances_initial.outputs['Instances'], scale_instances_final.inputs['Instances'])
    links.new(math_clamp.outputs['Value'], scale_instances_final.inputs['Scale']) # Use distance value for scale

    # Realize Instances
    realize_instances = nodes.new(type='GEOMETRY_NODES_REALISE_INSTANCES')
    realize_instances.location = (800, 0)
    links.new(scale_instances_final.outputs['Instances'], realize_instances.inputs['Geometry'])

    # Connect to Group Output
    links.new(realize_instances.outputs['Geometry'], group_output.inputs['Geometry'])

    return f"Created '{object_name}' at {location} with Geometry Nodes setup."


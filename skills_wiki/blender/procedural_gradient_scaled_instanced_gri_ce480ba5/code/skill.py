def create_geometry_nodes_grid_instances(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGridInstances",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    grid_size_x: float = 10.0,
    grid_size_y: float = 10.0,
    grid_vertices_x: int = 20,
    grid_vertices_y: int = 20,
    instance_rotation_z: float = 45.0, # degrees
    instance_scale_uniform: float = 0.2,
    distance_map_from_max: float = 10.0, # Max distance to map from
    distance_map_to_min: float = 0.05,  # Min scale for instances
    distance_map_to_max: float = 1.0,   # Max scale for instances
    suzanne_density: float = 10.0,
    suzanne_random_scale_min: float = 0.05,
    suzanne_random_scale_max: float = 0.15,
    suzanne_random_rotation_max: float = 360.0, # degrees
    material_color: tuple = (0.8, 0.2, 0.1), # Not fully utilized in this geo-node heavy skill, but kept for consistency
    **kwargs,
) -> str:
    """
    Creates a procedural grid of instances using Geometry Nodes, as demonstrated in the tutorial.
    The instances' scale is based on their distance from the origin.
    Then, points are distributed on these instances, and Suzanne objects are instanced on those points with random scale and rotation.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the main object holding the Geometry Nodes modifier.
        location: (x, y, z) world-space position for the main object.
        scale: Uniform scale factor for the main object.
        grid_size_x: X dimension of the initial grid.
        grid_size_y: Y dimension of the initial grid.
        grid_vertices_x: Number of vertices in X direction for the grid.
        grid_vertices_y: Number of vertices in Y direction for the grid.
        instance_rotation_z: Z-axis rotation in degrees for the grid instances.
        instance_scale_uniform: Uniform scale for grid instances (before distance scaling).
        distance_map_from_max: The maximum distance value to map from for scaling instances.
        distance_map_to_min: The minimum scale value instances can have based on distance.
        distance_map_to_max: The maximum scale value instances can have based on distance.
        suzanne_density: Density of Suzanne instances on the faces of the grid instances.
        suzanne_random_scale_min: Minimum random scale for Suzanne instances.
        suzanne_random_scale_max: Maximum random scale for Suzanne instances.
        suzanne_random_rotation_max: Maximum random Z-axis rotation in degrees for Suzanne instances.
        material_color: (R, G, B) base color in 0-1 range (applied to helper objects, not directly to geo nodes).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'ProceduralGridInstances' at (0, 0, 0) with Geometry Nodes setup."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 0. Helper Objects for Instancing (Planes and Suzanne) ---
    # Create a Plane to instance on the grid points
    plane_name = f"{object_name}_InstancePlane"
    if plane_name not in bpy.data.objects:
        bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False, align='WORLD', location=(0,0,0))
        instance_plane = bpy.context.active_object
        instance_plane.name = plane_name
        instance_plane.hide_set(True)
        instance_plane.hide_render = True
        # Apply material to the helper object
        if instance_plane.data.materials:
            instance_plane.data.materials[0] = bpy.data.materials.new(name=f"{plane_name}_Mat")
        else:
            instance_plane.data.materials.append(bpy.data.materials.new(name=f"{plane_name}_Mat"))
        instance_plane.data.materials[0].diffuse_color = (*material_color, 1.0)
    else:
        instance_plane = bpy.data.objects[plane_name]
        if instance_plane.data.materials and instance_plane.data.materials[0]:
            instance_plane.data.materials[0].diffuse_color = (*material_color, 1.0)

    # Create a Suzanne to instance on distributed points
    suzanne_name = f"{object_name}_InstanceSuzanne"
    if suzanne_name not in bpy.data.objects:
        bpy.ops.mesh.primitive_monkey_add(size=1.0, enter_editmode=False, align='WORLD', location=(0,0,0))
        instance_suzanne = bpy.context.active_object
        instance_suzanne.name = suzanne_name
        instance_suzanne.hide_set(True)
        instance_suzanne.hide_render = True
        # Apply material to the helper object
        if instance_suzanne.data.materials:
            instance_suzanne.data.materials[0] = bpy.data.materials.new(name=f"{suzanne_name}_Mat")
        else:
            instance_suzanne.data.materials.append(bpy.data.materials.new(name=f"{suzanne_name}_Mat"))
        instance_suzanne.data.materials[0].diffuse_color = (*material_color, 1.0)
    else:
        instance_suzanne = bpy.data.objects[suzanne_name]
        if instance_suzanne.data.materials and instance_suzanne.data.materials[0]:
            instance_suzanne.data.materials[0].diffuse_color = (*material_color, 1.0)

    # --- 1. Create Base Object for Geometry Nodes ---
    # The tutorial uses a cube initially, which gets its geometry replaced by the GN output.
    bpy.ops.mesh.primitive_cube_add(size=2.0, enter_editmode=False, align='WORLD', location=(0,0,0))
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # --- 2. Add Geometry Nodes Modifier ---
    gn_modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # --- 3. Create Geometry Node Tree ---
    node_tree_name = f"{object_name}_NodeTree"
    if node_tree_name in bpy.data.node_groups:
        node_tree = bpy.data.node_groups[node_tree_name]
    else:
        node_tree = bpy.data.node_groups.new(name=node_tree_name, type='GeometryNodeTree')
        # Clear default nodes (Group Input, Group Output) if a new tree was created
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)
        node_tree.nodes.new(type='NodeGroupInput')
        node_tree.nodes.new(type='NodeGroupOutput')

    gn_modifier.node_group = node_tree
    
    # Get initial input and output nodes
    group_input = next((n for n in node_tree.nodes if n.type == 'GROUP_INPUT'), None)
    group_output = next((n for n in node_tree.nodes if n.type == 'GROUP_OUTPUT'), None)

    # Ensure links are clear before recreating
    node_tree.links.clear()

    # --- 4. Populate Node Tree ---

    # Nodes for the initial grid and points
    grid_node = node_tree.nodes.new(type='GeometryNodeMeshGrid')
    mesh_to_points_node = node_tree.nodes.new(type='GeometryNodeMeshToPoints')

    # Nodes for instancing planes
    object_info_plane_node = node_tree.nodes.new(type='GeometryNodeObjectInfo')
    instance_on_points_plane_node = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
    rotate_instances_node = node_tree.nodes.new(type='GeometryNodeRotateInstances')
    scale_instances_base_node = node_tree.nodes.new(type='GeometryNodeScaleInstances')

    # Nodes for distance-based scaling
    position_node = node_tree.nodes.new(type='GeometryNodeInputPosition')
    vector_math_distance_node = node_tree.nodes.new(type='ShaderNodeVectorMath')
    map_range_node = node_tree.nodes.new(type='ShaderNodeMapRange')
    scale_instances_distance_node = node_tree.nodes.new(type='GeometryNodeScaleInstances')
    
    # Nodes for final Suzanne instances
    realize_instances_node = node_tree.nodes.new(type='GeometryNodeRealizeInstances')
    distribute_points_node = node_tree.nodes.new(type='GeometryNodeDistributePointsOnFaces')
    object_info_suzanne_node = node_tree.nodes.new(type='GeometryNodeObjectInfo')
    instance_on_points_suzanne_node = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
    random_value_scale_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
    random_value_rotation_node = node_tree.nodes.new(type='FunctionNodeRandomValue')

    # --- 5. Configure Nodes ---

    # Grid settings
    grid_node.inputs['Size X'].default_value = grid_size_x
    grid_node.inputs['Size Y'].default_value = grid_size_y
    grid_node.inputs['Vertices X'].default_value = grid_vertices_x
    grid_node.inputs['Vertices Y'].default_value = grid_vertices_y

    # Mesh to Points (default 'Faces' in video example)
    mesh_to_points_node.inputs['Radius'].default_value = 0.05 # Smaller dots for internal representation

    # Object Info for the plane instance
    object_info_plane_node.inputs['Object'].set(instance_plane)
    object_info_plane_node.inputs['As Instance'].default_value = True

    # Rotate Instances
    rotate_instances_node.inputs['Rotation'].default_value.z = math.radians(instance_rotation_z)

    # Scale Instances (base scale)
    scale_instances_base_node.inputs['Scale'].default_value = (instance_scale_uniform, instance_scale_uniform, instance_scale_uniform)

    # Vector Math (Distance)
    vector_math_distance_node.operation = 'DISTANCE'
    vector_math_distance_node.inputs[1].default_value = (0.0, 0.0, 0.0) # Distance from origin

    # Map Range (for controlling how distance affects scale)
    map_range_node.inputs['From Min'].default_value = 0.0
    map_range_node.inputs['From Max'].default_value = distance_map_from_max
    map_range_node.inputs['To Min'].default_value = distance_map_to_min
    map_range_node.inputs['To Max'].default_value = distance_map_to_max
    
    # Distribute Points on Faces
    distribute_points_node.inputs['Density'].default_value = suzanne_density
    distribute_points_node.inputs['Seed'].default_value = kwargs.get('suzanne_seed', 0) # Example seed, can be randomized

    # Object Info for Suzanne instance
    object_info_suzanne_node.inputs['Object'].set(instance_suzanne)
    object_info_suzanne_node.inputs['As Instance'].default_value = True

    # Random Value for Suzanne scale
    random_value_scale_node.data_type = 'FLOAT'
    random_value_scale_node.inputs['Min'].default_value = suzanne_random_scale_min
    random_value_scale_node.inputs['Max'].default_value = suzanne_random_scale_max
    random_value_scale_node.inputs['Seed'].default_value = kwargs.get('suzanne_scale_seed', 1)

    # Random Value for Suzanne rotation
    random_value_rotation_node.data_type = 'VECTOR'
    random_value_rotation_node.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    random_value_rotation_node.inputs['Max'].default_value = (0.0, 0.0, math.radians(suzanne_random_rotation_max)) # Only Z-axis rotation
    random_value_rotation_node.inputs['Seed'].default_value = kwargs.get('suzanne_rotation_seed', 2)

    # --- 6. Link Nodes ---

    # Initial Grid setup
    node_tree.links.new(grid_node.outputs['Mesh'], mesh_to_points_node.inputs['Mesh'])

    # Instance planes on points
    node_tree.links.new(mesh_to_points_node.outputs['Points'], instance_on_points_plane_node.inputs['Points'])
    node_tree.links.new(object_info_plane_node.outputs['Geometry'], instance_on_points_plane_node.inputs['Instance'])

    # Rotate and Scale base instances
    node_tree.links.new(instance_on_points_plane_node.outputs['Instances'], rotate_instances_node.inputs['Instances'])
    node_tree.links.new(rotate_instances_node.outputs['Instances'], scale_instances_base_node.inputs['Instances'])

    # Distance-based scaling
    node_tree.links.new(position_node.outputs['Position'], vector_math_distance_node.inputs[0])
    node_tree.links.new(vector_math_distance_node.outputs['Value'], map_range_node.inputs['Value']) # Connect distance to map range
    node_tree.links.new(map_range_node.outputs['Result'], scale_instances_distance_node.inputs['Scale']) # Map Range output to scale
    node_tree.links.new(scale_instances_base_node.outputs['Instances'], scale_instances_distance_node.inputs['Instances']) # Original scaled instances go here

    # Realize instances and distribute points for Suzanne
    node_tree.links.new(scale_instances_distance_node.outputs['Instances'], realize_instances_node.inputs['Geometry'])
    node_tree.links.new(realize_instances_node.outputs['Geometry'], distribute_points_node.inputs['Mesh'])

    # Instance Suzanne on new points
    node_tree.links.new(distribute_points_node.outputs['Points'], instance_on_points_suzanne_node.inputs['Points'])
    node_tree.links.new(object_info_suzanne_node.outputs['Geometry'], instance_on_points_suzanne_node.inputs['Instance'])
    node_tree.links.new(random_value_scale_node.outputs['Value'], instance_on_points_suzanne_node.inputs['Scale'])
    node_tree.links.new(random_value_rotation_node.outputs['Value'], instance_on_points_suzanne_node.inputs['Rotation'])

    # Final output
    node_tree.links.new(instance_on_points_suzanne_node.outputs['Instances'], group_output.inputs['Geometry'])

    # Position nodes for better layout (optional but good practice)
    grid_node.location = Vector((-600, 0))
    mesh_to_points_node.location = Vector((-400, 0))
    object_info_plane_node.location = Vector((-400, -200))
    instance_on_points_plane_node.location = Vector((-200, 0))
    rotate_instances_node.location = Vector((0, 0))
    scale_instances_base_node.location = Vector((200, 0))
    position_node.location = Vector((200, -200))
    vector_math_distance_node.location = Vector((400, -200))
    map_range_node.location = Vector((600, -200))
    scale_instances_distance_node.location = Vector((600, 0))
    realize_instances_node.location = Vector((800, 0))
    distribute_points_node.location = Vector((1000, 0))
    object_info_suzanne_node.location = Vector((1000, -200))
    instance_on_points_suzanne_node.location = Vector((1200, 0))
    random_value_scale_node.location = Vector((1000, -300))
    random_value_rotation_node.location = Vector((1200, -300))
    group_output.location = Vector((1400, 0))

    return f"Created '{object_name}' at {location} with Geometry Nodes setup."


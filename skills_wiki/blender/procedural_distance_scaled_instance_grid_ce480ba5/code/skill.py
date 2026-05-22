def create_procedural_distance_scaled_grid(
    scene_name: str = "Scene",
    object_name: str = "DistanceScaledGrid",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_grid_size_x: float = 10.0,
    base_grid_size_y: float = 10.0,
    base_grid_vertices_x: int = 20,
    base_grid_vertices_y: int = 20,
    instance_grid_size: float = 0.8,
    instance_rotation_z_deg: float = 45.0, # in degrees
    distance_center: tuple = (0.0, 0.0, 0.0),
    scale_from_min_dist: float = 0.0, # Input for Map Range 'From Min'
    scale_from_max_dist: float = None, # Input for Map Range 'From Max', calculated if None
    scale_to_min_val: float = 0.05, # Input for Map Range 'To Min'
    scale_to_max_val: float = 0.2, # Input for Map Range 'To Max'
    apply_suzanne_distribution: bool = False,
    suzanne_density: float = 50.0,
    suzanne_scale_min: float = 0.1,
    suzanne_scale_max: float = 0.3,
    material_color: tuple = (0.8, 0.8, 0.8, 1.0), # RGBA
    **kwargs,
) -> str:
    """
    Creates a procedural grid of instances where each instance's scale is determined
    by its distance from a central point, using Geometry Nodes. Optionally
    distributes Suzanne monkeys on the generated geometry.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the main object (a cube with the GeoNodes modifier).
        location: (x, y, z) world-space position for the main object.
        scale: Uniform scale factor for the main object.
        base_grid_size_x: Size of the initial grid along X axis.
        base_grid_size_y: Size of the initial grid along Y axis.
        base_grid_vertices_x: Number of vertices along X axis for the initial grid.
        base_grid_vertices_y: Number of vertices along Y axis for the initial grid.
        instance_grid_size: Size of the individual grid instances.
        instance_rotation_z_deg: Z-axis rotation for each instance in degrees.
        distance_center: (x, y, z) world-space point for distance calculation.
        scale_from_min_dist: The minimum distance value to map from.
        scale_from_max_dist: The maximum distance value to map from. If None, it's calculated
                             based on base_grid_size_x/y and global scale.
        scale_to_min_val: The minimum scale value to map to.
        scale_to_max_val: The maximum scale value to map to.
        apply_suzanne_distribution: If True, distributes Suzanne monkeys on the
                                     realized instances.
        suzanne_density: Density of Suzanne monkeys per square meter.
        suzanne_scale_min: Minimum random scale for Suzanne instances.
        suzanne_scale_max: Maximum random scale for Suzanne instances.
        material_color: (R, G, B, A) base color for the instances in 0-1 range.
        **kwargs: Additional overrides (e.g., subdivision_level, roughness).

    Returns:
        Status string, e.g., "Created 'DistanceScaledGrid' at (0, 0, 0) with Geometry Nodes setup."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Calculate default scale_from_max_dist if not provided
    if scale_from_max_dist is None:
        max_dist_from_grid_center = math.sqrt( (base_grid_size_x/2)**2 + (base_grid_size_y/2)**2 )
        scale_from_max_dist = max_dist_from_grid_center * scale + Vector(distance_center).length

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a new empty object or reuse an existing one to apply GeoNodes
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        bpy.ops.mesh.primitive_cube_add(size=0.001, enter_editmode=False, align='WORLD', location=(0,0,0)) # Small initial cube
        obj = bpy.context.active_object
        obj.name = object_name
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Ensure the object has a Geometry Nodes modifier
    gn_modifier = None
    for mod in obj.modifiers:
        if mod.type == 'NODES':
            gn_modifier = mod
            break
    if gn_modifier is None:
        gn_modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # Create a new Geometry Node tree or get existing one
    node_tree_name = f"{object_name}_GeoNodes"
    node_tree = bpy.data.node_groups.get(node_tree_name)
    if node_tree is None:
        node_tree = bpy.data.node_groups.new(name=node_tree_name, type='GeometryNodeTree')
    else:
        # Clear existing nodes if tree already exists to ensure clean setup
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)
    
    gn_modifier.node_group = node_tree

    # Add Group Input and Group Output
    group_input = node_tree.nodes.new(type='NodeGroupInput')
    group_input.location = (-1000, 0)
    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1200, 0)

    # --- Define Node Group Inputs (exposed to modifier panel) ---
    # These calls safely add inputs only if they don't already exist.
    if 'Base Grid Size X' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Base Grid Size X')
    if 'Base Grid Size Y' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Base Grid Size Y')
    if 'Base Grid Vertices X' not in node_tree.inputs: node_tree.inputs.new('NodeSocketInt', 'Base Grid Vertices X')
    if 'Base Grid Vertices Y' not in node_tree.inputs: node_tree.inputs.new('NodeSocketInt', 'Base Grid Vertices Y')
    if 'Instance Grid Size' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Instance Grid Size')
    if 'Instance Rotation Z (deg)' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Instance Rotation Z (deg)')
    if 'Distance Center' not in node_tree.inputs: node_tree.inputs.new('NodeSocketVector', 'Distance Center')
    if 'Scale From Min Dist' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Scale From Min Dist')
    if 'Scale From Max Dist' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Scale From Max Dist')
    if 'Scale To Min Val' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Scale To Min Val')
    if 'Scale To Max Val' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Scale To Max Val')
    if 'Material' not in node_tree.inputs: node_tree.inputs.new('NodeSocketMaterial', 'Material')
    if apply_suzanne_distribution:
        if 'Suzanne Density' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Suzanne Density')
        if 'Suzanne Scale Min' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Suzanne Scale Min')
        if 'Suzanne Scale Max' not in node_tree.inputs: node_tree.inputs.new('NodeSocketFloat', 'Suzanne Scale Max')


    # === Node Setup ===

    # 1. Base Grid (Driver for points)
    grid_node = node_tree.nodes.new(type='GeometryNodeMeshGrid')
    grid_node.location = (-800, 200)
    node_tree.links.new(group_input.outputs['Base Grid Size X'], grid_node.inputs['Size X'])
    node_tree.links.new(group_input.outputs['Base Grid Size Y'], grid_node.inputs['Size Y'])
    node_tree.links.new(group_input.outputs['Base Grid Vertices X'], grid_node.inputs['Vertices X'])
    node_tree.links.new(group_input.outputs['Base Grid Vertices Y'], grid_node.inputs['Vertices Y'])

    # 2. Mesh to Points
    mesh_to_points = node_tree.nodes.new(type='GeometryNodeMeshToPoints')
    mesh_to_points.location = (-500, 200)
    mesh_to_points.inputs['Mode'].default_value = 'FACE' # As seen in tutorial
    node_tree.links.new(grid_node.outputs['Mesh'], mesh_to_points.inputs['Mesh'])

    # 3. Instance Grid (the actual instances)
    instance_mesh_grid = node_tree.nodes.new(type='GeometryNodeMeshGrid')
    instance_mesh_grid.location = (-500, -100)
    instance_mesh_grid.inputs['Vertices X'].default_value = 2 # Low res instances
    instance_mesh_grid.inputs['Vertices Y'].default_value = 2
    node_tree.links.new(group_input.outputs['Instance Grid Size'], instance_mesh_grid.inputs['Size X'])
    node_tree.links.new(group_input.outputs['Instance Grid Size'], instance_mesh_grid.inputs['Size Y'])

    # 4. Instance on Points
    instance_on_points = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
    instance_on_points.location = (-200, 200)
    node_tree.links.new(mesh_to_points.outputs['Points'], instance_on_points.inputs['Points'])
    node_tree.links.new(instance_mesh_grid.outputs['Mesh'], instance_on_points.inputs['Instance'])

    # 5. Rotate Instances
    rotate_instances = node_tree.nodes.new(type='GeometryNodeRotateInstances')
    rotate_instances.location = (0, 200)
    
    combine_rot_xyz = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_rot_xyz.location = (-200, -200)
    # Convert degrees to radians here for the default value, linking will override
    combine_rot_xyz.inputs['Z'].default_value = math.radians(instance_rotation_z_deg)
    node_tree.links.new(group_input.outputs['Instance Rotation Z (deg)'], combine_rot_xyz.inputs['Z'])
    node_tree.links.new(combine_rot_xyz.outputs['Vector'], rotate_instances.inputs['Rotation'])

    node_tree.links.new(instance_on_points.outputs['Instances'], rotate_instances.inputs['Instances'])

    # 6. Scale Instances (distance based)
    scale_instances = node_tree.nodes.new(type='GeometryNodeScaleInstances')
    scale_instances.location = (200, 200)

    # Position node
    position_node = node_tree.nodes.new(type='GeometryNodeInputPosition')
    position_node.location = (-200, -400)

    # Vector Math (Distance) node
    distance_node = node_tree.nodes.new(type='ShaderNodeVectorMath')
    distance_node.location = (0, -400)
    distance_node.operation = 'DISTANCE'
    node_tree.links.new(position_node.outputs['Position'], distance_node.inputs[0])
    node_tree.links.new(group_input.outputs['Distance Center'], distance_node.inputs[1])

    # Map Range node for scaling
    map_range_node = node_tree.nodes.new(type='ShaderNodeMapRange')
    map_range_node.location = (200, -400)
    node_tree.links.new(group_input.outputs['Scale From Min Dist'], map_range_node.inputs['From Min'])
    node_tree.links.new(group_input.outputs['Scale From Max Dist'], map_range_node.inputs['From Max'])
    node_tree.links.new(group_input.outputs['Scale To Min Val'], map_range_node.inputs['To Min'])
    node_tree.links.new(group_input.outputs['Scale To Max Val'], map_range_node.inputs['To Max'])
    node_tree.links.new(distance_node.outputs['Value'], map_range_node.inputs['Value'])
    node_tree.links.new(map_range_node.outputs['Result'], scale_instances.inputs['Scale'])

    node_tree.links.new(rotate_instances.outputs['Instances'], scale_instances.inputs['Instances'])

    # 7. Realize Instances
    realize_instances = node_tree.nodes.new(type='GeometryNodeRealizeInstances')
    realize_instances.location = (400, 200)
    node_tree.links.new(scale_instances.outputs['Instances'], realize_instances.inputs['Geometry'])

    current_output_geometry = realize_instances.outputs['Geometry']

    # 8. Set Material
    set_material_node = node_tree.nodes.new(type='GeometryNodeSetMaterial')
    set_material_node.location = (600, 200)
    node_tree.links.new(current_output_geometry, set_material_node.inputs['Geometry'])
    node_tree.links.new(group_input.outputs['Material'], set_material_node.inputs['Material'])
    current_output_geometry = set_material_node.outputs['Geometry']

    # --- Optional Suzanne Distribution ---
    if apply_suzanne_distribution:
        # Create Suzanne mesh if it doesn't exist
        suzanne_mesh_obj = bpy.data.objects.get("Suzanne_Mesh_Data")
        if suzanne_mesh_obj is None:
            bpy.ops.mesh.primitive_monkey_add(size=1.0, enter_editmode=False, align='WORLD', location=(10000, 10000, 10000)) # Create far away
            suzanne_mesh_obj = bpy.context.active_object
            suzanne_mesh_obj.name = "Suzanne_Mesh_Data"
            suzanne_mesh_obj.hide_set(True) # Hide Suzanne in viewport
            suzanne_mesh_obj.hide_render = True # Hide Suzanne in renders
            bpy.context.view_layer.objects.active = suzanne_mesh_obj
            bpy.ops.object.shade_smooth()
            subdiv_mod = suzanne_mesh_obj.modifiers.new(name="Subdivision", type='SUBSURF')
            subdiv_mod.levels = 2
            subdiv_mod.render_levels = 2
            bpy.context.view_layer.objects.active = None # Clear active object selection


        # Add Object Info node for Suzanne
        object_info_suzanne = node_tree.nodes.new(type='GeometryNodeInputObjectInfo')
        object_info_suzanne.location = (600, -200)
        object_info_suzanne.inputs['Object'].default_value = suzanne_mesh_obj
        object_info_suzanne.inputs['As Instance'].default_value = True

        # Distribute Points on Faces (for Suzanne)
        distribute_points_suzanne = node_tree.nodes.new(type='GeometryNodeDistributePointsOnFaces')
        distribute_points_suzanne.location = (800, 200)
        node_tree.links.new(group_input.outputs['Suzanne Density'], distribute_points_suzanne.inputs['Density'])
        node_tree.links.new(current_output_geometry, distribute_points_suzanne.inputs['Mesh'])
        
        # Instance on Points (for Suzanne)
        instance_on_points_suzanne = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
        instance_on_points_suzanne.location = (1000, 200)
        node_tree.links.new(distribute_points_suzanne.outputs['Points'], instance_on_points_suzanne.inputs['Points'])
        node_tree.links.new(object_info_suzanne.outputs['Geometry'], instance_on_points_suzanne.inputs['Instance'])

        # Random Value for Suzanne scale
        random_scale_suzanne = node_tree.nodes.new(type='FunctionNodeRandomValue')
        random_scale_suzanne.location = (800, -300)
        random_scale_suzanne.inputs['Type'].default_value = 'FLOAT'
        node_tree.links.new(group_input.outputs['Suzanne Scale Min'], random_scale_suzanne.inputs['Min'])
        node_tree.links.new(group_input.outputs['Suzanne Scale Max'], random_scale_suzanne.inputs['Max'])
        node_tree.links.new(random_scale_suzanne.outputs['Value'], instance_on_points_suzanne.inputs['Scale'])

        current_output_geometry = instance_on_points_suzanne.outputs['Instances']

    # Final Output
    node_tree.links.new(current_output_geometry, group_output.inputs['Geometry'])

    # --- Set Default values for modifier panel ---
    # These set the initial values visible in the modifier properties
    gn_modifier[group_input.outputs['Base Grid Size X'].identifier] = base_grid_size_x
    gn_modifier[group_input.outputs['Base Grid Size Y'].identifier] = base_grid_size_y
    gn_modifier[group_input.outputs['Base Grid Vertices X'].identifier] = base_grid_vertices_x
    gn_modifier[group_input.outputs['Base Grid Vertices Y'].identifier] = base_grid_vertices_y
    gn_modifier[group_input.outputs['Instance Grid Size'].identifier] = instance_grid_size
    gn_modifier[group_input.outputs['Instance Rotation Z (deg)'].identifier] = instance_rotation_z_deg
    gn_modifier[group_input.outputs['Distance Center'].identifier] = Vector(distance_center)
    gn_modifier[group_input.outputs['Scale From Min Dist'].identifier] = scale_from_min_dist
    gn_modifier[group_input.outputs['Scale From Max Dist'].identifier] = scale_from_max_dist
    gn_modifier[group_input.outputs['Scale To Min Val'].identifier] = scale_to_min_val
    gn_modifier[group_input.outputs['Scale To Max Val'].identifier] = scale_to_max_val

    # Create and assign material
    material_name = f"{object_name}_Instances_Material"
    material = bpy.data.materials.get(material_name)
    if material is None:
        material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = material_color
    else:
        # Update existing material color
        if material.use_nodes:
            bsdf = material.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = material_color

    gn_modifier[group_input.outputs['Material'].identifier] = material


    if apply_suzanne_distribution:
        gn_modifier[group_input.outputs['Suzanne Density'].identifier] = suzanne_density
        gn_modifier[group_input.outputs['Suzanne Scale Min'].identifier] = suzanne_scale_min
        gn_modifier[group_input.outputs['Suzanne Scale Max'].identifier] = suzanne_scale_max

    return f"Created '{object_name}' at {location} with Geometry Nodes setup."


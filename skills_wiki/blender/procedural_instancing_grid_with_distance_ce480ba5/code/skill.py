def create_procedural_instancing_grid(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGrid",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    grid_size: float = 10.0,
    grid_subdivisions: int = 20,
    instance_rotation_z: float = 45.0,
    instance_scale_multiplier: float = 0.2,
    distance_scale_min: float = 0.0,
    distance_scale_max: float = 1.0,
    suzanne_density: float = 10.0,
    suzanne_scale_min: float = 0.1,
    suzanne_scale_max: float = 0.3,
    **kwargs,
) -> str:
    """
    Creates a procedural grid of instances with distance-based scaling and
    distributes Suzanne monkeys on top, using Geometry Nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created main object (cube hosting geo nodes).
        location: (x, y, z) world-space position for the main object.
        scale: Uniform scale factor for the main object.
        grid_size: Size of the initial grid (both X and Y).
        grid_subdivisions: Number of vertices for the initial grid (X and Y).
        instance_rotation_z: Rotation in degrees for each instanced grid on Z-axis.
        instance_scale_multiplier: Base scale multiplier for the instanced grids.
        distance_scale_min: Minimum scale for instances based on distance from origin.
        distance_scale_max: Maximum scale for instances based on distance from origin.
        suzanne_density: Density of Suzanne distribution on the realized instances.
        suzanne_scale_min: Minimum random scale for distributed Suzannes.
        suzanne_scale_max: Maximum random scale for distributed Suzannes.
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created 'ProceduralGrid' at (0, 0, 0) with Geometry Nodes."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    # Material for the main grid instances
    grid_mat_name = f"{object_name}_GridMaterial"
    grid_mat = bpy.data.materials.get(grid_mat_name)
    if not grid_mat:
        grid_mat = bpy.data.materials.new(name=grid_mat_name)
        grid_mat.use_nodes = True
        bsdf = grid_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.7, 0.7, 0.7, 1) # Light grey
        bsdf.inputs["Roughness"].default_value = 0.7

    # Material for the Suzanne instances
    suzanne_mat_name = f"{object_name}_SuzanneMaterial"
    suzanne_mat = bpy.data.materials.get(suzanne_mat_name)
    if not suzanne_mat:
        suzanne_mat = bpy.data.materials.new(name=suzanne_mat_name)
        suzanne_mat.use_nodes = True
        bsdf = suzanne_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.4, 0.4, 0.4, 1) # Darker grey
        bsdf.inputs["Roughness"].default_value = 0.5

    # --- Base Object ---
    # Create a simple cube to host the Geometry Nodes modifier
    bpy.ops.mesh.primitive_cube_add(
        size=0.1,  # Small cube, its geometry will be replaced by the grid
        enter_editmode=False,
        align='WORLD',
        location=location,
        scale=(scale, scale, scale)
    )
    main_obj = bpy.context.active_object
    main_obj.name = object_name
    
    # --- Geometry Node Tree ---
    # Create a new geometry node tree
    gn_tree_name = f"{object_name}_GeoNodes"
    gn_tree = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')
    
    # Get initial Group Input and Group Output nodes
    node_input = gn_tree.nodes["Group Input"]
    node_output = gn_tree.nodes["Group Output"]
    
    # Remove default input geometry socket if present (we're generating geometry)
    if "Geometry" in node_input.outputs:
        gn_tree.outputs.remove(node_input.outputs["Geometry"])

    # Create Group Input for user parameters
    gn_tree.inputs.new('NodeSocketFloat', 'Grid Size')
    gn_tree.inputs['Grid Size'].default_value = grid_size
    gn_tree.inputs.new('NodeSocketInt', 'Grid Subdivisions')
    gn_tree.inputs['Grid Subdivisions'].default_value = grid_subdivisions
    gn_tree.inputs.new('NodeSocketFloat', 'Instance Rotation Z')
    gn_tree.inputs['Instance Rotation Z'].default_value = instance_rotation_z
    gn_tree.inputs.new('NodeSocketFloat', 'Instance Scale Multiplier')
    gn_tree.inputs['Instance Scale Multiplier'].default_value = instance_scale_multiplier
    gn_tree.inputs.new('NodeSocketFloat', 'Distance Scale Min')
    gn_tree.inputs['Distance Scale Min'].default_value = distance_scale_min
    gn_tree.inputs.new('NodeSocketFloat', 'Distance Scale Max')
    gn_tree.inputs['Distance Scale Max'].default_value = distance_scale_max
    gn_tree.inputs.new('NodeSocketFloat', 'Suzanne Density')
    gn_tree.inputs['Suzanne Density'].default_value = suzanne_density
    gn_tree.inputs.new('NodeSocketFloat', 'Suzanne Scale Min')
    gn_tree.inputs['Suzanne Scale Min'].default_value = suzanne_scale_min
    gn_tree.inputs.new('NodeSocketFloat', 'Suzanne Scale Max')
    gn_tree.inputs['Suzanne Scale Max'].default_value = suzanne_scale_max

    # --- Node Tree Construction ---
    # 1. Base Grid
    node_grid = gn_tree.nodes.new(type="GeometryNodeMeshGrid")
    gn_tree.links.new(node_input.outputs['Grid Size'], node_grid.inputs['Size X'])
    gn_tree.links.new(node_input.outputs['Grid Size'], node_grid.inputs['Size Y'])
    gn_tree.links.new(node_input.outputs['Grid Subdivisions'], node_grid.inputs['Vertices X'])
    gn_tree.links.new(node_input.outputs['Grid Subdivisions'], node_grid.inputs['Vertices Y'])
    node_grid.location = (0, 0)

    # 2. Mesh to Points (for instancing)
    node_mesh_to_points = gn_tree.nodes.new(type="GeometryNodeMeshToPoints")
    gn_tree.links.new(node_grid.outputs['Mesh'], node_mesh_to_points.inputs['Mesh'])
    node_mesh_to_points.location = (200, 0)

    # 3. Instance on Points (first layer - the grids themselves)
    node_instance_on_points_grid = gn_tree.nodes.new(type="GeometryNodeInstanceOnPoints")
    gn_tree.links.new(node_mesh_to_points.outputs['Points'], node_instance_on_points_grid.inputs['Points'])
    gn_tree.links.new(node_grid.outputs['Mesh'], node_instance_on_points_grid.inputs['Instance']) # Instance the grid itself
    node_instance_on_points_grid.location = (400, 0)

    # 4. Rotate Instances
    node_rotate_instances = gn_tree.nodes.new(type="GeometryNodeRotateInstances")
    gn_tree.links.new(node_instance_on_points_grid.outputs['Instances'], node_rotate_instances.inputs['Instances'])
    node_rotate_instances.inputs['Axis'].default_value = (0, 0, 1) # Rotate around Z
    node_radians = gn_tree.nodes.new(type="ShaderNodeMath") # Convert degrees to radians
    node_radians.operation = 'TO_RADIANS'
    gn_tree.links.new(node_input.outputs['Instance Rotation Z'], node_radians.inputs[0])
    gn_tree.links.new(node_radians.outputs[0], node_rotate_instances.inputs['Rotation'])
    node_rotate_instances.location = (600, 0)

    # 5. Scale Instances (distance-based)
    node_scale_instances = gn_tree.nodes.new(type="GeometryNodeScaleInstances")
    gn_tree.links.new(node_rotate_instances.outputs['Instances'], node_scale_instances.inputs['Instances'])
    node_scale_instances.location = (800, 0)

    # Calculate distance from origin
    node_position = gn_tree.nodes.new(type="GeometryNodeInputPosition")
    node_position.location = (600, -200)
    node_distance = gn_tree.nodes.new(type="ShaderNodeVectorMath")
    node_distance.operation = 'DISTANCE'
    node_distance.inputs[1].default_value = (0, 0, 0) # Distance from origin
    gn_tree.links.new(node_position.outputs['Position'], node_distance.inputs[0])
    node_distance.location = (800, -200)

    # Map Range for scaling
    node_map_range = gn_tree.nodes.new(type="ShaderNodeMapRange")
    node_map_range.inputs['From Max'].default_value = grid_size * math.sqrt(2) / 2 # Max distance from center to corner
    gn_tree.links.new(node_distance.outputs['Value'], node_map_range.inputs['Value'])
    gn_tree.links.new(node_input.outputs['Distance Scale Min'], node_map_range.inputs['To Min'])
    gn_tree.links.new(node_input.outputs['Distance Scale Max'], node_map_range.inputs['To Max'])
    node_map_range.location = (1000, -200)

    # Multiply by base scale
    node_vector_math_scale = gn_tree.nodes.new(type="ShaderNodeVectorMath")
    node_vector_math_scale.operation = 'MULTIPLY'
    gn_tree.links.new(node_map_range.outputs['Result'], node_vector_math_scale.inputs[0])
    gn_tree.links.new(node_input.outputs['Instance Scale Multiplier'], node_vector_math_scale.inputs[1])
    gn_tree.links.new(node_vector_math_scale.outputs['Vector'], node_scale_instances.inputs['Scale'])
    node_vector_math_scale.location = (1200, -200)
    
    # 6. Realize Instances (convert instances to actual geometry)
    node_realize_instances = gn_tree.nodes.new(type="GeometryNodeRealizeInstances")
    gn_tree.links.new(node_scale_instances.outputs['Instances'], node_realize_instances.inputs['Geometry'])
    node_realize_instances.location = (1000, 0)

    # Set Material for the realized instances
    node_set_material_grid = gn_tree.nodes.new(type="GeometryNodeSetMaterial")
    gn_tree.links.new(node_realize_instances.outputs['Geometry'], node_set_material_grid.inputs['Geometry'])
    node_set_material_grid.inputs['Material'].default_value = grid_mat
    node_set_material_grid.location = (1200, 0)

    # 7. Distribute Points on Faces (for Suzanne)
    node_distribute_points = gn_tree.nodes.new(type="GeometryNodeDistributePointsOnFaces")
    gn_tree.links.new(node_set_material_grid.outputs['Geometry'], node_distribute_points.inputs['Mesh'])
    gn_tree.links.new(node_input.outputs['Suzanne Density'], node_distribute_points.inputs['Density'])
    node_distribute_points.location = (1400, 0)

    # 8. Instance on Points (second layer - Suzanne)
    node_instance_on_points_suzanne = gn_tree.nodes.new(type="GeometryNodeInstanceOnPoints")
    gn_tree.links.new(node_distribute_points.outputs['Points'], node_instance_on_points_suzanne.inputs['Points'])
    
    # Create Suzanne mesh object temporarily to get its geometry
    bpy.ops.mesh.primitive_monkey_add(size=1.0, enter_editmode=False, location=(10000, 10000, 10000)) # Far away
    suzanne_mesh_obj = bpy.context.active_object
    suzanne_mesh_obj.name = f"{object_name}_SuzanneGeometry"
    suzanne_mesh_obj.hide_set(True)
    suzanne_mesh_obj.hide_render = True
    
    # Use Object Info node to reference Suzanne's mesh
    node_obj_info_suzanne = gn_tree.nodes.new(type='GeometryNodeObjectInfo')
    node_obj_info_suzanne.inputs['Object'].default_value = suzanne_mesh_obj
    node_obj_info_suzanne.inputs['As Instance'].default_value = True # Take as instance to avoid geometry conversion
    gn_tree.links.new(node_obj_info_suzanne.outputs['Geometry'], node_instance_on_points_suzanne.inputs['Instance'])
    node_obj_info_suzanne.location = (1400, -200)

    # Random Scale for Suzanne
    node_random_scale_suzanne = gn_tree.nodes.new(type="GeometryNodeRandomValue")
    node_random_scale_suzanne.data_type = 'FLOAT'
    gn_tree.links.new(node_input.outputs['Suzanne Scale Min'], node_random_scale_suzanne.inputs['Min'])
    gn_tree.links.new(node_input.outputs['Suzanne Scale Max'], node_random_scale_suzanne.inputs['Max'])
    gn_tree.links.new(node_random_scale_suzanne.outputs['Value'], node_instance_on_points_suzanne.inputs['Scale'])
    node_random_scale_suzanne.location = (1600, -200)

    # Set Material for Suzanne instances
    node_set_material_suzanne = gn_tree.nodes.new(type="GeometryNodeSetMaterial")
    gn_tree.links.new(node_instance_on_points_suzanne.outputs['Instances'], node_set_material_suzanne.inputs['Geometry'])
    node_set_material_suzanne.inputs['Material'].default_value = suzanne_mat
    node_set_material_suzanne.location = (1800, 0)

    # 9. Join Geometry
    node_join_geometry = gn_tree.nodes.new(type="GeometryNodeJoinGeometry")
    gn_tree.links.new(node_set_material_grid.outputs['Geometry'], node_join_geometry.inputs['Geometry'])
    gn_tree.links.new(node_set_material_suzanne.outputs['Geometry'], node_join_geometry.inputs['Geometry'])
    node_join_geometry.location = (2000, 0)
    
    # Connect to Group Output
    gn_tree.links.new(node_join_geometry.outputs['Geometry'], node_output.inputs['Geometry'])

    # --- Apply Geometry Nodes Modifier ---
    mod = main_obj.modifiers.new(name="GeometryNodes", type='NODES')
    mod.node_group = gn_tree

    # Link custom parameters to modifier inputs
    mod["Input_1"] = grid_size
    mod["Input_2"] = grid_subdivisions
    mod["Input_3"] = instance_rotation_z
    mod["Input_4"] = instance_scale_multiplier
    mod["Input_5"] = distance_scale_min
    mod["Input_6"] = distance_scale_max
    mod["Input_7"] = suzanne_density
    mod["Input_8"] = suzanne_scale_min
    mod["Input_9"] = suzanne_scale_max

    # Ensure the Suzanne helper object is cleaned up or hidden
    suzanne_mesh_obj.parent = main_obj # Parent it to the main object
    suzanne_mesh_obj.hide_render = True
    suzanne_mesh_obj.hide_viewport = True
    suzanne_mesh_obj.display_type = 'WIRE' # Less obtrusive in viewport

    return f"Created '{object_name}' at {location} with Geometry Nodes."


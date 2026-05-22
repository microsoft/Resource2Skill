def create_procedural_tiling_and_scatter(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGen",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    grid_size: float = 10.0,
    grid_vertices: int = 20,
    tile_scale: float = 0.2,
    suzanne_density: float = 10.0,
    suzanne_random_scale_min: float = 0.1,
    suzanne_random_scale_max: float = 0.5,
    material_color_tiles: tuple = (0.8, 0.2, 0.1),
    material_color_suzannes: tuple = (0.1, 0.5, 0.8),
    **kwargs,
) -> str:
    """
    Creates a procedural tiling pattern with instanced grids and scattered Suzanne monkeys
    using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created main object (host for GeoNodes).
        location: (x, y, z) world-space position for the main object.
        scale: Uniform scale factor for the main object.
        grid_size: Size of the main procedural grid.
        grid_vertices: Number of vertices for the main grid.
        tile_scale: Uniform scale for the individual grid tiles.
        suzanne_density: Number of Suzanne instances per square meter on the tiles.
        suzanne_random_scale_min: Minimum random scale for Suzanne instances.
        suzanne_random_scale_max: Maximum random scale for Suzanne instances.
        material_color_tiles: (R, G, B) base color for the grid tiles.
        material_color_suzannes: (R, G, B) base color for the Suzanne instances.
        **kwargs: Additional overrides (e.g., subdivision_level).

    Returns:
        Status string, e.g., "Created 'ProceduralGen' at (0, 0, 0) with Geometry Nodes"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Create a host object for the Geometry Nodes modifier ---
    bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False, align='WORLD', location=location)
    host_obj = bpy.context.active_object
    host_obj.name = object_name
    host_obj.scale = (scale, scale, scale)

    # --- Create Suzanne object for instancing later ---
    bpy.ops.mesh.primitive_monkey_add(size=1.0, enter_editmode=False, align='WORLD', location=(1000, 1000, 1000)) # Place far away
    suzanne_obj = bpy.context.active_object
    suzanne_obj.name = "Suzanne_Instance_Source"
    suzanne_obj.hide_set(True) # Hide the source object

    # --- Create Material for Tiles ---
    tile_mat = bpy.data.materials.new(name="Tile_Material")
    tile_mat.use_nodes = True
    bsdf_node_tiles = tile_mat.node_tree.nodes["Principled BSDF"]
    bsdf_node_tiles.inputs["Base Color"].default_value = (*material_color_tiles, 1.0) # RGBA

    # --- Create Material for Suzannes ---
    suzanne_mat = bpy.data.materials.new(name="Suzanne_Material")
    suzanne_mat.use_nodes = True
    bsdf_node_suzannes = suzanne_mat.node_tree.nodes["Principled BSDF"]
    bsdf_node_suzannes.inputs["Base Color"].default_value = (*material_color_suzannes, 1.0) # RGBA

    # --- Create Geometry Node Tree ---
    if "Procedural_Tiling_NodeTree" not in bpy.data.node_groups:
        node_tree = bpy.data.node_groups.new(name="Procedural_Tiling_NodeTree", type='GeometryNodeTree')
    else:
        node_tree = bpy.data.node_groups["Procedural_Tiling_NodeTree"]
        # Clear existing nodes for a clean start if already exists
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

    # Add Group Input/Output if not present or cleared
    group_input = node_tree.nodes.new('NodeGroupInput')
    group_output = node_tree.nodes.new('NodeGroupOutput')
    group_input.location = (-1000, 0)
    group_output.location = (1000, 0)

    # Remove default geometry input from Group Input
    if 'Geometry' in group_input.outputs:
        node_tree.outputs.remove(group_input.outputs['Geometry'])

    # --- Add Geometry Nodes to the tree ---

    # Base Grid (acts as the main surface)
    grid_node = node_tree.nodes.new('GeometryNodeMeshGrid')
    grid_node.location = (-800, 200)
    grid_node.inputs['Size X'].default_value = grid_size
    grid_node.inputs['Size Y'].default_value = grid_size
    grid_node.inputs['Vertices X'].default_value = grid_vertices
    grid_node.inputs['Vertices Y'].default_value = grid_vertices

    # --- Tiling Pattern Branch ---
    # Convert grid faces to points for instancing
    mesh_to_points_node = node_tree.nodes.new('GeometryNodeMeshToPoints')
    mesh_to_points_node.location = (-600, 200)
    mesh_to_points_node.inputs['Domain'].default_value = 'FACE' # Instance on faces
    node_tree.links.new(grid_node.outputs['Mesh'], mesh_to_points_node.inputs['Mesh'])

    # Instance a smaller grid as tiles
    tile_grid_node = node_tree.nodes.new('GeometryNodeMeshGrid')
    tile_grid_node.location = (-400, 400)
    tile_grid_node.inputs['Size X'].default_value = 1.0
    tile_grid_node.inputs['Size Y'].default_value = 1.0
    tile_grid_node.inputs['Vertices X'].default_value = 2 # Low res for tiles
    tile_grid_node.inputs['Vertices Y'].default_value = 2

    instance_on_points_tiles = node_tree.nodes.new('GeometryNodeInstanceOnPoints')
    instance_on_points_tiles.location = (-400, 200)
    node_tree.links.new(mesh_to_points_node.outputs['Points'], instance_on_points_tiles.inputs['Points'])
    node_tree.links.new(tile_grid_node.outputs['Mesh'], instance_on_points_tiles.inputs['Instance'])

    # Rotate instances
    rotate_instances = node_tree.nodes.new('GeometryNodeRotateInstances')
    rotate_instances.location = (-200, 200)
    rotate_instances.inputs['Rotation'].default_value = (0, 0, math.radians(45)) # 45 degrees around Z
    node_tree.links.new(instance_on_points_tiles.outputs['Instances'], rotate_instances.inputs['Instances'])

    # Scale instances (uniform base scale)
    scale_instances_base = node_tree.nodes.new('GeometryNodeScaleInstances')
    scale_instances_base.location = (0, 200)
    scale_instances_base.inputs['Scale'].default_value = (tile_scale, tile_scale, tile_scale)
    node_tree.links.new(rotate_instances.outputs['Instances'], scale_instances_base.inputs['Instances'])

    # Scale instances based on distance from origin
    position_node = node_tree.nodes.new('GeometryNodeInputPosition')
    position_node.location = (0, -100)

    distance_node = node_tree.nodes.new('ShaderNodeVectorMath')
    distance_node.location = (200, -100)
    distance_node.operation = 'DISTANCE'
    distance_node.inputs[1].default_value = (0, 0, 0) # Distance from origin
    node_tree.links.new(position_node.outputs['Position'], distance_node.inputs[0])

    map_range_node = node_tree.nodes.new('ShaderNodeMapRange')
    map_range_node.location = (400, -100)
    map_range_node.inputs['From Min'].default_value = 0.0
    map_range_node.inputs['From Max'].default_value = grid_size * 0.7 # Approximate max distance
    map_range_node.inputs['To Min'].default_value = 0.5 # Minimum scale for furthest
    map_range_node.inputs['To Max'].default_value = 1.5 # Maximum scale for closest
    node_tree.links.new(distance_node.outputs['Value'], map_range_node.inputs['Value'])

    scale_instances_distance = node_tree.nodes.new('GeometryNodeScaleInstances')
    scale_instances_distance.location = (200, 200)
    scale_instances_distance.inputs['Scale'].default_value = (1, 1, 1) # This is overwritten by factor
    node_tree.links.new(scale_instances_base.outputs['Instances'], scale_instances_distance.inputs['Instances'])
    node_tree.links.new(map_range_node.outputs['Result'], scale_instances_distance.inputs['Scale'].outputs[0]) # Scale X, Y, Z by result

    # Realize instances to make them actual geometry for next scatter
    realize_instances_tiles = node_tree.nodes.new('GeometryNodeRealizeInstances')
    realize_instances_tiles.location = (400, 200)
    node_tree.links.new(scale_instances_distance.outputs['Instances'], realize_instances_tiles.inputs['Geometry'])

    # Set Material for tiles
    set_material_tiles = node_tree.nodes.new('GeometryNodeSetMaterial')
    set_material_tiles.location = (600, 200)
    set_material_tiles.inputs['Material'].default_value = tile_mat
    node_tree.links.new(realize_instances_tiles.outputs['Geometry'], set_material_tiles.inputs['Geometry'])

    # --- Suzanne Scatter Branch ---
    # Distribute points on the realized tiles
    distribute_points_on_faces = node_tree.nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute_points_on_faces.location = (600, -200)
    distribute_points_on_faces.inputs['Density'].default_value = suzanne_density
    node_tree.links.new(realize_instances_tiles.outputs['Geometry'], distribute_points_on_faces.inputs['Mesh'])

    # Object Info for Suzanne
    suzanne_object_info = node_tree.nodes.new('GeometryNodeInputObjectInfo')
    suzanne_object_info.location = (600, -400)
    suzanne_object_info.inputs['Object'].default_value = suzanne_obj
    suzanne_object_info.inputs['As Instance'].default_value = True

    # Instance Suzanne on points
    instance_on_points_suzanne = node_tree.nodes.new('GeometryNodeInstanceOnPoints')
    instance_on_points_suzanne.location = (800, -200)
    node_tree.links.new(distribute_points_on_faces.outputs['Points'], instance_on_points_suzanne.inputs['Points'])
    node_tree.links.new(suzanne_object_info.outputs['Geometry'], instance_on_points_suzanne.inputs['Instance'])

    # Random Scale for Suzanne instances
    random_value_scale_suzanne = node_tree.nodes.new('GeometryNodeRandomValue')
    random_value_scale_suzanne.location = (800, -400)
    random_value_scale_suzanne.inputs['Type'].default_value = 'VECTOR'
    random_value_scale_suzanne.inputs['Min'].default_value = (suzanne_random_scale_min, suzanne_random_scale_min, suzanne_random_scale_min)
    random_value_scale_suzanne.inputs['Max'].default_value = (suzanne_random_scale_max, suzanne_random_scale_max, suzanne_random_scale_max)
    node_tree.links.new(random_value_scale_suzanne.outputs['Value'], instance_on_points_suzanne.inputs['Scale'])

    # Set Material for Suzannes
    set_material_suzannes = node_tree.nodes.new('GeometryNodeSetMaterial')
    set_material_suzannes.location = (1000, -200)
    set_material_suzannes.inputs['Material'].default_value = suzanne_mat
    node_tree.links.new(instance_on_points_suzanne.outputs['Instances'], set_material_suzannes.inputs['Geometry'])

    # --- Join Geometries ---
    join_geometry = node_tree.nodes.new('GeometryNodeJoinGeometry')
    join_geometry.location = (800, 0)
    node_tree.links.new(set_material_tiles.outputs['Geometry'], join_geometry.inputs['Geometry'])
    node_tree.links.new(set_material_suzannes.outputs['Geometry'], join_geometry.inputs['Geometry'])


    # --- Output ---
    node_tree.links.new(join_geometry.outputs['Geometry'], group_output.inputs['Geometry'])

    # --- Apply Geometry Nodes modifier to the host object ---
    gn_modifier = host_obj.modifiers.new(name="GeometryNodes", type='NODES')
    gn_modifier.node_group = node_tree

    # --- Clean up Suzanne source object ---
    bpy.data.objects.remove(suzanne_obj)


    return f"Created '{object_name}' at {location} with Geometry Nodes for procedural tiling and scattering."


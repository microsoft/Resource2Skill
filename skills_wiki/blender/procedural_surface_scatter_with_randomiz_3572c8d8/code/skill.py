def create_procedural_surface_scatter(
    scene_name: str = "Scene",
    object_name: str = "SugarCoatedObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_mesh_color: tuple = (0.8, 0.1, 0.2, 1.0), # RGBA
    crystal_color: tuple = (1.0, 1.0, 1.0, 1.0), # RGBA
    density: float = 100.0,
    min_crystal_scale: float = 0.11,
    max_crystal_scale: float = 0.39,
    seed: int = 0,
    **kwargs,
) -> str:
    """
    Creates a procedural surface scatter effect using Geometry Nodes,
    simulating sugar crystals on a base mesh.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created base object with the Geometry Nodes modifier.
        location: (x, y, z) world-space position for the base object.
        scale: Uniform scale factor for the base object.
        base_mesh_color: (R, G, B, A) base color for the primary mesh in 0-1 range.
        crystal_color: (R, G, B, A) base color for the scattered instances in 0-1 range.
        density: Number of points to distribute per square meter (approx).
        min_crystal_scale: Minimum uniform scale for individual sugar crystals.
        max_crystal_scale: Maximum uniform scale for individual sugar crystals.
        seed: Random seed for point distribution and instance randomization.
        **kwargs: Additional overrides (e.g., base_mesh_type, crystal_mesh_type).

    Returns:
        Status string, e.g., "Created 'SugarCoatedObject' at (0, 0, 0) with 2 objects."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 0. Helper Functions / Data ---
    # Ensure math.tau is available for full rotation (2 * PI)
    if not hasattr(math, 'tau'):
        math.tau = 2 * math.pi

    # --- 1. Create Base Mesh (e.g., a Cube for the candy) ---
    bpy.ops.mesh.primitive_cube_add(
        size=2,
        enter_editmode=False,
        align='WORLD',
        location=location,
        scale=(scale, scale, scale)
    )
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.location = Vector(location)
    base_obj.scale = (scale, scale, scale)

    # --- 2. Create Instance Mesh (e.g., a small Cube for sugar crystal) ---
    crystal_name = f"{object_name}_sugar_crystal"
    bpy.ops.mesh.primitive_cube_add(
        size=1, # Default size, will be scaled by GN
        enter_editmode=False,
        align='WORLD',
        location=(1000, 1000, 1000) # Far away to be out of view
    )
    crystal_obj = bpy.context.active_object
    crystal_obj.name = crystal_name
    
    # Apply default scale for proper instancing
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Hide crystal object from viewport and renders
    crystal_obj.hide_set(True)
    crystal_obj.hide_render = True

    # --- 3. Create Materials ---
    base_mat = bpy.data.materials.new(name=f"{object_name}_BaseMat")
    base_mat.use_nodes = True
    bsdf = base_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = base_mesh_color
    # Optional: add some subsurface scattering for candy look
    bsdf.inputs["Subsurface"].default_value = 0.1
    bsdf.inputs["Subsurface Color"].default_value = base_mesh_color
    base_obj.data.materials.append(base_mat)

    crystal_mat = bpy.data.materials.new(name=f"{crystal_name}_Mat")
    crystal_mat.use_nodes = True
    bsdf_crystal = crystal_mat.node_tree.nodes["Principled BSDF"]
    bsdf_crystal.inputs["Base Color"].default_value = crystal_color
    bsdf_crystal.inputs["Roughness"].default_value = 0.8
    # Add some translucency for sugar
    bsdf_crystal.inputs["Subsurface"].default_value = 0.2
    bsdf_crystal.inputs["Subsurface Color"].default_value = (0.9, 0.9, 0.9, 1.0)
    crystal_obj.data.materials.append(crystal_mat)


    # --- 4. Add Geometry Nodes Modifier to Base Object ---
    geo_nodes_modifier = base_obj.modifiers.new(name="GeometryNodes", type='NODES')
    
    # Create a new Geometry Node group
    node_tree_name = f"{object_name}_ScatterNodes"
    geo_nodes_modifier.node_group = bpy.data.node_groups.new(name=node_tree_name, type='GeometryNodeTree')
    
    node_tree = geo_nodes_modifier.node_group
    nodes = node_tree.nodes
    links = node_tree.links

    # Clear existing default nodes (Group Input and Group Output are recreated below)
    for node in nodes:
        nodes.remove(node)

    # --- 5. Build Geometry Node Tree ---
    # Group Input
    group_input = nodes.new(type='NodeGroupInput')
    group_input.location = (-800, 0)
    # Add geometry input to the node group for the base mesh
    node_tree.inputs.new('NodeSocketGeometry', 'Geometry')
    group_input.outputs[0].name = 'Geometry'


    # Distribute Points on Faces
    distribute_points = nodes.new(type='GEOMETRY_NODES_DISTRIBUTE_POINTS_ON_FACES')
    distribute_points.location = (-400, 200)
    distribute_points.inputs['Density'].default_value = density
    distribute_points.inputs['Seed'].default_value = seed

    # Object Info (for the sugar crystal)
    object_info = nodes.new(type='GEOMETRY_NODES_OBJECT_INFO')
    object_info.location = (-400, -200)
    object_info.inputs['Object'].set(crystal_obj)
    object_info.inputs['As Instance'].default_value = True # Ensure it's treated as instance

    # Random Value (for Rotation)
    random_rot = nodes.new(type='GEOMETRY_NODES_RANDOM_VALUE')
    random_rot.location = (-100, 100)
    random_rot.data_type = 'FLOAT_VECTOR' # Use Vector for XYZ rotation
    random_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    random_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau) # Full 360 degree rotation
    random_rot.inputs['Seed'].default_value = seed # Use same seed for consistency

    # Random Value (for Scale)
    random_scale = nodes.new(type='GEOMETRY_NODES_RANDOM_VALUE')
    random_scale.location = (-100, -50)
    random_scale.data_type = 'FLOAT' # Use Float for uniform scaling
    random_scale.inputs['Min'].default_value = min_crystal_scale
    random_scale.inputs['Max'].default_value = max_crystal_scale
    random_scale.inputs['Seed'].default_value = seed + 1 # Different seed for scale randomization

    # Instance on Points
    instance_on_points = nodes.new(type='GEOMETRY_NODES_INSTANCE_ON_POINTS')
    instance_on_points.location = (100, 100)

    # Join Geometry (to combine base mesh and instances)
    join_geometry = nodes.new(type='GEOMETRY_NODES_JOIN_GEOMETRY')
    join_geometry.location = (400, 0)

    # Group Output
    group_output = nodes.new(type='NodeGroupOutput')
    group_output.location = (600, 0)
    node_tree.outputs.new('NodeSocketGeometry', 'Geometry')


    # --- 6. Connect Nodes ---
    # Input to Distribute Points
    links.new(group_input.outputs['Geometry'], distribute_points.inputs['Mesh'])
    
    # Distribute Points to Instance on Points
    links.new(distribute_points.outputs['Points'], instance_on_points.inputs['Points'])
    
    # Object Info to Instance on Points
    links.new(object_info.outputs['Geometry'], instance_on_points.inputs['Instance'])
    
    # Random Rotation to Instance on Points
    links.new(random_rot.outputs['Value'], instance_on_points.inputs['Rotation'])

    # Random Scale to Instance on Points
    links.new(random_scale.outputs['Value'], instance_on_points.inputs['Scale'])

    # Instance on Points to Join Geometry
    links.new(instance_on_points.outputs['Instances'], join_geometry.inputs['Geometry'])
    
    # Original Geometry to Join Geometry
    links.new(group_input.outputs['Geometry'], join_geometry.inputs['Geometry'])

    # Join Geometry to Group Output
    links.new(join_geometry.outputs['Geometry'], group_output.inputs['Geometry'])

    return f"Created '{object_name}' with procedural sugar scatter at {location}"


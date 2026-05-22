def create_procedural_sugar_coating(
    scene_name: str = "Scene",
    base_object_name: str = "SugarCandy",
    sugar_crystal_name: str = "SugarCrystal",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    candy_color: tuple = (0.8, 0.1, 0.1), # Red
    sugar_color: tuple = (0.9, 0.9, 0.9), # White
    point_density: float = 200.0,
    min_sugar_scale: float = 0.1,
    max_sugar_scale: float = 0.3,
) -> str:
    """
    Creates a procedural sugar-coated object using Geometry Nodes.
    The base object is a Torus, coated with small scattered cubes.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Name for the base candy object.
        sugar_crystal_name: Name for the hidden sugar crystal instance object.
        location: (x, y, z) world-space position for the candy.
        scale: Uniform scale factor for the candy.
        candy_color: (R, G, B) base color for the candy.
        sugar_color: (R, G, B) base color for the sugar crystals.
        point_density: Number of sugar crystals per square meter.
        min_sugar_scale: Minimum scale for individual sugar crystals.
        max_sugar_scale: Maximum scale for individual sugar crystals.

    Returns:
        Status string, e.g., "Created 'SugarCandy' at (0, 0, 0) with sugar coating"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Sugar Crystal Instance Object (hidden) ---
    # Ensure no object is active or selected initially to avoid issues
    bpy.ops.object.select_all(action='DESELECT')
    
    # Create cube for sugar crystal
    bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(0,0,0))
    sugar_crystal_obj = bpy.context.object
    sugar_crystal_obj.name = sugar_crystal_name
    
    # Apply scale to the sugar crystal instance for correct scaling in Geometry Nodes
    # It's important to select and activate the object before applying transform
    bpy.ops.object.select_all(action='DESELECT')
    sugar_crystal_obj.select_set(True)
    bpy.context.view_layer.objects.active = sugar_crystal_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Hide original instance from render and viewport
    sugar_crystal_obj.hide_render = True
    sugar_crystal_obj.hide_set(True)

    # Create sugar material
    sugar_mat = bpy.data.materials.new(name=f"{sugar_crystal_name}Material")
    sugar_mat.use_nodes = True
    if bsdf := sugar_mat.node_tree.nodes.get("Principled BSDF"):
        bsdf.inputs["Base Color"].default_value = (*sugar_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
        bsdf.inputs["IOR"].default_value = 1.35
        bsdf.inputs["Transmission"].default_value = 0.1
    if not sugar_crystal_obj.data.materials:
        sugar_crystal_obj.data.materials.append(sugar_mat)
    else:
        sugar_crystal_obj.data.materials[0] = sugar_mat


    # --- 2. Create Base Candy Object (Torus) ---
    bpy.ops.object.select_all(action='DESELECT') # Deselect before creating new object
    bpy.ops.mesh.primitive_torus_add(
        align='WORLD',
        major_radius=0.8,
        minor_radius=0.3,
        major_segments=48,
        minor_segments=24
    )
    base_obj = bpy.context.object
    base_obj.name = base_object_name

    # Apply subdivision surface for smoothness
    subdiv = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 3
    bpy.ops.object.shade_smooth()

    # Create candy material
    candy_mat = bpy.data.materials.new(name=f"{base_object_name}Material")
    candy_mat.use_nodes = True
    if bsdf := candy_mat.node_tree.nodes.get("Principled BSDF"):
        bsdf.inputs["Base Color"].default_value = (*candy_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3
        bsdf.inputs["Subsurface"].default_value = 0.2
        bsdf.inputs["Subsurface Color"].default_value = (*candy_color, 1.0)
    if not base_obj.data.materials:
        base_obj.data.materials.append(candy_mat)
    else:
        base_obj.data.materials[0] = candy_mat


    # --- 3. Setup Geometry Nodes ---
    # Create a new Geometry Node tree or get existing one
    gn_tree_name = f"{base_object_name}_SugarNodes"
    gn_tree = bpy.data.node_groups.get(gn_tree_name)
    if not gn_tree:
        gn_tree = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')
    
    gn_modifier = base_obj.modifiers.new(name="GeometryNodes", type='NODES')
    gn_modifier.node_group = gn_tree

    nodes = gn_tree.nodes
    links = gn_tree.links

    # Clear default nodes if they exist (for new tree, it's just input/output)
    for node in nodes:
        nodes.remove(node)

    # Group Input and Output
    group_input = nodes.new(type='NodeGroupInput')
    group_input.location = (-800, 0)
    group_output = nodes.new(type='NodeGroupOutput')
    group_output.location = (800, 0)

    # Distribute Points on Faces
    distribute_points = nodes.new(type='GEOMETRY_NODE_DISTRIBUTE_POINTS_ON_FACES')
    distribute_points.location = (-400, 200)
    distribute_points.inputs["Density"].default_value = point_density
    distribute_points.inputs["Seed"].default_value = 0 # Can be randomized by user later

    # Instance on Points
    instance_on_points = nodes.new(type='GEOMETRY_NODE_INSTANCE_ON_POINTS')
    instance_on_points.location = (0, 0)

    # Random Value for Rotation
    random_rot = nodes.new(type='FunctionNodeRandomValue')
    random_rot.location = (-200, -200)
    random_rot.data_type = 'FLOAT_VECTOR' # Use vector for X, Y, Z rotation
    random_rot.inputs[1].default_value = (0.0, 0.0, 0.0) # Min rotation
    random_rot.inputs[2].default_value = (math.tau, math.tau, math.tau) # Max rotation (2*pi for full 360)

    # Random Value for Scale
    random_scale = nodes.new(type='FunctionNodeRandomValue')
    random_scale.location = (-200, -400)
    random_scale.data_type = 'FLOAT' # Use float for uniform scale
    random_scale.inputs[1].default_value = min_sugar_scale # Min scale (e.g., 0.110 in video)
    random_scale.inputs[2].default_value = max_sugar_scale # Max scale (e.g., 0.390 in video)

    # Object Info for sugar crystal
    object_info_crystal = nodes.new(type='GEOMETRY_NODE_OBJECT_INFO')
    object_info_crystal.location = (-200, -600)
    object_info_crystal.inputs["Object"].default_value = sugar_crystal_obj
    object_info_crystal.inputs["As Instance"].default_value = True

    # Join Geometry
    join_geometry = nodes.new(type='GEOMETRY_NODE_JOIN_GEOMETRY')
    join_geometry.location = (400, 0)


    # --- 4. Link Nodes ---
    # Original geometry to Join Geometry
    links.new(group_input.outputs["Geometry"], join_geometry.inputs[0]) # First input socket

    # Distribute Points on Faces
    links.new(group_input.outputs["Geometry"], distribute_points.inputs["Mesh"])

    # Instance on Points
    links.new(distribute_points.outputs["Points"], instance_on_points.inputs["Points"])
    links.new(object_info_crystal.outputs["Geometry"], instance_on_points.inputs["Instance"])

    # Random Rotation
    links.new(random_rot.outputs["Value"], instance_on_points.inputs["Rotation"])

    # Random Scale
    links.new(random_scale.outputs["Value"], instance_on_points.inputs["Scale"])

    # Instances to Join Geometry
    links.new(instance_on_points.outputs["Instances"], join_geometry.inputs[1]) # Second input socket

    # Join Geometry to Group Output
    links.new(join_geometry.outputs["Geometry"], group_output.inputs["Geometry"])


    # --- 5. Position & Scale ---
    base_obj.location = Vector(location)
    base_obj.scale = (scale, scale, scale)

    return f"Created '{base_object_name}' at {location} with procedural sugar coating."


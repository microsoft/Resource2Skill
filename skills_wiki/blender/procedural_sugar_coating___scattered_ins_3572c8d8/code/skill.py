def create_sugar_coated_object(
    scene_name: str = "Scene",
    base_object_name: str = "SugarCandyBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_material_color: tuple = (0.8, 0.1, 0.2, 1.0), # RGBA
    sugar_material_color: tuple = (1.0, 1.0, 1.0, 1.0), # RGBA
    density: float = 2000,
    sugar_min_scale: float = 0.1,
    sugar_max_scale: float = 0.3,
    sugar_rotation_strength: float = 6.28319, # math.tau for 360 degrees
    subdivision_level: int = 2,
    candy_transmission: float = 0.7,
    candy_roughness: float = 0.2,
    sugar_roughness: float = 0.3,
    sugar_emission: float = 0.05,
    sugar_bevel_amount: float = 0.005,
    sugar_bevel_segments: int = 2,
    hide_crystal_instance: bool = True,
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated object using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Name for the main candy base object.
        location: (x, y, z) world-space position for the base object.
        scale: Uniform scale factor for the base object.
        base_material_color: (R, G, B, A) base color for the candy in 0-1 range.
        sugar_material_color: (R, G, B, A) base color for the sugar crystals.
        density: Number of sugar crystals to scatter (points per square meter).
        sugar_min_scale: Minimum scale for individual sugar crystals.
        sugar_max_scale: Maximum scale for individual sugar crystals.
        sugar_rotation_strength: Max rotation in radians (math.tau for 360 degrees).
        subdivision_level: Subdivision levels for the base candy mesh.
        candy_transmission: Transmission value for the candy material.
        candy_roughness: Roughness value for the candy material.
        sugar_roughness: Roughness value for the sugar crystal material.
        sugar_emission: Emission strength for the sugar crystal material.
        sugar_bevel_amount: Bevel amount for the sugar crystals.
        sugar_bevel_segments: Bevel segments for the sugar crystals.
        hide_crystal_instance: If True, hides the original sugar crystal object.
        **kwargs: Additional overrides for future parameters.

    Returns:
        Status string, e.g., "Created 'SugarCandyBase' with sugar coating."
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Candy Mesh (e.g., a simple cube for demonstration) ---
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD',
                                    location=location, scale=(scale, scale, scale))
    base_obj = bpy.context.object
    base_obj.name = base_object_name

    # Add Subdivision Surface Modifier to base object for smoother shape
    subdiv_mod = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_level
    subdiv_mod.render_levels = subdivision_level
    bpy.ops.object.shade_smooth() # Smooth shading

    # --- 2. Create Sugar Crystal Instance Mesh ---
    sugar_crystal_name = f"{base_object_name}_SugarCrystalInstance"
    bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD',
                                    location=(100, 100, 100)) # Place far away
    sugar_crystal_obj = bpy.context.object
    sugar_crystal_obj.name = sugar_crystal_name

    # Apply scale for correct instancing
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Add Bevel Modifier to sugar crystal
    bevel_mod = sugar_crystal_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.width = sugar_bevel_amount
    bevel_mod.segments = sugar_bevel_segments
    bpy.ops.object.shade_smooth()

    if hide_crystal_instance:
        sugar_crystal_obj.hide_set(True)
        sugar_crystal_obj.hide_render = True

    # --- 3. Create Materials ---
    # Base Candy Material
    candy_mat = bpy.data.materials.new(name=f"{base_object_name}_CandyMat")
    candy_mat.use_nodes = True
    principled_bsdf = candy_mat.node_tree.nodes["Principled BSDF"]
    principled_bsdf.inputs["Base Color"].default_value = base_material_color
    principled_bsdf.inputs["Transmission"].default_value = candy_transmission
    principled_bsdf.inputs["Roughness"].default_value = candy_roughness
    principled_bsdf.inputs["IOR"].default_value = 1.3
    base_obj.data.materials.append(candy_mat)

    # Sugar Crystal Material
    sugar_mat = bpy.data.materials.new(name=f"{sugar_crystal_name}_SugarMat")
    sugar_mat.use_nodes = True
    principled_bsdf = sugar_mat.node_tree.nodes["Principled BSDF"]
    principled_bsdf.inputs["Base Color"].default_value = sugar_material_color
    principled_bsdf.inputs["Roughness"].default_value = sugar_roughness
    principled_bsdf.inputs["Metallic"].default_value = 0.1 # Slight metallic for sparkle
    principled_bsdf.inputs["Emission Strength"].default_value = sugar_emission
    sugar_crystal_obj.data.materials.append(sugar_mat)

    # --- 4. Setup Geometry Nodes ---
    gn_tree_name = f"{base_object_name}_SugarCoatingGN"
    gn_mod_name = "SugarCoating"

    # Create a new Geometry Node tree
    if gn_tree_name in bpy.data.node_groups:
        gn_tree = bpy.data.node_groups[gn_tree_name]
    else:
        gn_tree = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')

    # Clear existing nodes for a clean start if reusing a name, except Group Input/Output
    for node in gn_tree.nodes:
        if node.type not in {'GROUP_INPUT', 'GROUP_OUTPUT'}:
            gn_tree.nodes.remove(node)

    # Get Group Input and Output nodes
    node_input = gn_tree.nodes.get('Group Input') or gn_tree.nodes.new(type='NodeGroupInput')
    node_output = gn_tree.nodes.get('Group Output') or gn_tree.nodes.new(type='NodeGroupOutput')

    # Add Nodes
    node_distribute_points = gn_tree.nodes.new(type='GEOMETRY_NODES_DISTRIBUTE_POINTS_ON_FACES')
    node_instance_on_points = gn_tree.nodes.new(type='GEOMETRY_NODES_INSTANCE_ON_POINTS')
    node_object_info = gn_tree.nodes.new(type='GEOMETRY_NODES_OBJECT_INFO')
    node_random_rot = gn_tree.nodes.new(type='GEOMETRY_NODES_RANDOM_VALUE')
    node_random_scale = gn_tree.nodes.new(type='GEOMETRY_NODES_RANDOM_VALUE')
    node_join_geometry = gn_tree.nodes.new(type='GEOMETRY_NODES_JOIN_GEOMETRY')

    # Set Node Properties
    node_distribute_points.distribute_method = 'POISSON_DISK'
    node_distribute_points.inputs['Density Max'].default_value = density

    node_object_info.inputs['Object'].default_value = sugar_crystal_obj
    node_object_info.outputs['Geometry'].attribute_domain = 'POINT' # Important for instancing
    node_object_info.inputs['As Instance'].default_value = True
    node_object_info.inputs['Relative'].default_value = True

    node_random_rot.data_type = 'FLOAT_VECTOR'
    node_random_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    node_random_rot.inputs['Max'].default_value = (sugar_rotation_strength, sugar_rotation_strength, sugar_rotation_strength) # math.tau

    node_random_scale.data_type = 'FLOAT'
    node_random_scale.inputs['Min'].default_value = sugar_min_scale
    node_random_scale.inputs['Max'].default_value = sugar_max_scale

    # Arrange Nodes
    node_input.location = Vector((-800, 0))
    node_distribute_points.location = Vector((-400, 0))
    node_object_info.location = Vector((-400, -300))
    node_random_rot.location = Vector((-200, 200))
    node_random_scale.location = Vector((-200, -200))
    node_instance_on_points.location = Vector((0, 0))
    node_join_geometry.location = Vector((200, 0))
    node_output.location = Vector((400, 0))


    # Link Nodes
    gn_tree.links.new(node_input.outputs['Geometry'], node_distribute_points.inputs['Mesh'])
    gn_tree.links.new(node_distribute_points.outputs['Points'], node_instance_on_points.inputs['Points'])
    gn_tree.links.new(node_object_info.outputs['Geometry'], node_instance_on_points.inputs['Instance'])
    gn_tree.links.new(node_random_rot.outputs['Value'], node_instance_on_points.inputs['Rotation'])
    gn_tree.links.new(node_random_scale.outputs['Value'], node_instance_on_points.inputs['Scale'])

    gn_tree.links.new(node_input.outputs['Geometry'], node_join_geometry.inputs['Geometry'])
    gn_tree.links.new(node_instance_on_points.outputs['Instances'], node_join_geometry.inputs['Geometry_1'])
    gn_tree.links.new(node_join_geometry.outputs['Geometry'], node_output.inputs['Geometry'])


    # Add Geometry Nodes modifier to the base object
    gn_modifier = base_obj.modifiers.new(name=gn_mod_name, type='NODES')
    gn_modifier.node_group = gn_tree

    return f"Created '{base_object_name}' at {location} with sugar coating."


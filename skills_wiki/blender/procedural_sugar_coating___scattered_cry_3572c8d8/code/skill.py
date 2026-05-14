def create_procedural_sugar_coating(
    scene_name: str = "Scene",
    base_object_name: str = "SugarCandy",
    crystal_object_name: str = "SugarCrystal",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    candy_color: tuple = (0.8, 0.05, 0.05, 1.0), # RGBA
    crystal_color: tuple = (0.9, 0.9, 0.9, 1.0), # RGBA
    subdivision_levels: int = 2,
    density: float = 100.0,
    min_crystal_scale: float = 0.1,
    max_crystal_scale: float = 0.5,
    min_rotation_radians: float = 0.0,
    max_rotation_radians: float = 6.28319, # math.tau for 360 degrees
    crystal_roughness: float = 0.2,
    candy_transmission: float = 0.5,
    hide_crystal_source: bool = True,
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes in Blender.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Name for the main candy object.
        crystal_object_name: Name for the sugar crystal source object.
        location: (x, y, z) world-space position for the candy.
        scale: Uniform scale factor for the candy.
        candy_color: (R, G, B, A) base color for the candy body.
        crystal_color: (R, G, B, A) base color for the sugar crystals.
        subdivision_levels: Subdivision levels for the base candy.
        density: Density of sugar crystals on the candy surface.
        min_crystal_scale: Minimum uniform scale for individual crystals.
        max_crystal_scale: Maximum uniform scale for individual crystals.
        min_rotation_radians: Minimum rotation in radians (0 to math.tau).
        max_rotation_radians: Maximum rotation in radians (0 to math.tau).
        crystal_roughness: Roughness for the sugar crystal material.
        candy_transmission: Transmission for the candy material.
        hide_crystal_source: If True, hide the original crystal object.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'SugarCandy' with 'SugarCrystal' instances."
    """
    import bpy
    import mathutils
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Candy Mesh ---
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    candy_obj = bpy.context.object
    candy_obj.name = base_object_name

    # Apply Subdivision Surface Modifier for rounded shape
    subdiv_mod = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels

    # --- 2. Create Sugar Crystal Instance Mesh ---
    bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    crystal_source_obj = bpy.context.object
    crystal_source_obj.name = crystal_object_name

    # Apply scale to the instance source object
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    if hide_crystal_source:
        crystal_source_obj.hide_set(True)
        crystal_source_obj.hide_render = True

    # --- 3. Create Geometry Nodes Setup ---
    # Create a new Geometry Node tree
    geonode_tree = bpy.data.node_groups.new(name=f"{base_object_name}_GeometryNodes", type='GeometryNodeTree')

    # Add Geometry Nodes modifier to the candy_obj
    geonode_mod = candy_obj.modifiers.new(name="GeometryNodes", type='NODES')
    geonode_mod.node_group = geonode_tree

    # Clear default nodes from new group
    for node in geonode_tree.nodes:
        geonode_tree.nodes.remove(node)

    # Add Group Input and Group Output nodes
    node_input = geonode_tree.nodes.new(type='NodeGroupInput')
    node_input.location = (-800, 0)
    node_output = geonode_tree.nodes.new(type='NodeGroupOutput')
    node_output.location = (800, 0)

    # Add Distribute Points on Faces node
    node_distribute_points = geonode_tree.nodes.new(type='GeometryNode_PointsDistribute')
    node_distribute_points.location = (-400, 200)
    node_distribute_points.inputs['Density'].default_value = density
    # Random Seed can be exposed or randomized too if needed, but for now fixed
    # node_distribute_points.inputs['Seed'].default_value = 0 # Can be kwargs

    # Add Object Info node for sugar crystal
    node_obj_info = geonode_tree.nodes.new(type='GeometryNodeObjectInfo')
    node_obj_info.location = (-600, -200)
    node_obj_info.inputs['Object'].default_value = crystal_source_obj
    node_obj_info.inputs['As Instance'].default_value = True

    # Add Instance on Points node
    node_instance_on_points = geonode_tree.nodes.new(type='GeometryNode_PointsInstance')
    node_instance_on_points.location = (0, 0)

    # Add Random Value node for rotation (Vector)
    node_random_rot = geonode_tree.nodes.new(type='FunctionNodeRandomValue')
    node_random_rot.location = (-200, -400)
    node_random_rot.data_type = 'FLOAT_VECTOR'
    node_random_rot.inputs['Min'].default_value = (min_rotation_radians, min_rotation_radians, min_rotation_radians)
    node_random_rot.inputs['Max'].default_value = (max_rotation_radians, max_rotation_radians, max_rotation_radians)

    # Add Random Value node for scale (Float)
    node_random_scale = geonode_tree.nodes.new(type='FunctionNodeRandomValue')
    node_random_scale.location = (-200, -600)
    node_random_scale.data_type = 'FLOAT'
    node_random_scale.inputs['Min'].default_value = min_crystal_scale
    node_random_scale.inputs['Max'].default_value = max_crystal_scale

    # Add Join Geometry node to combine base mesh and instances
    node_join_geometry = geonode_tree.nodes.new(type='GeometryNodeJoinGeometry')
    node_join_geometry.location = (400, 0)

    # Link nodes
    geonode_tree.links.new(node_input.outputs['Geometry'], node_distribute_points.inputs['Mesh'])
    geonode_tree.links.new(node_obj_info.outputs['Geometry'], node_instance_on_points.inputs['Instance'])
    geonode_tree.links.new(node_distribute_points.outputs['Points'], node_instance_on_points.inputs['Points'])
    geonode_tree.links.new(node_random_rot.outputs['Value'], node_instance_on_points.inputs['Rotation'])
    geonode_tree.links.new(node_random_scale.outputs['Value'], node_instance_on_points.inputs['Scale'])
    
    geonode_tree.links.new(node_input.outputs['Geometry'], node_join_geometry.inputs[0]) # Original mesh
    geonode_tree.links.new(node_instance_on_points.outputs['Instances'], node_join_geometry.inputs[1]) # Instanced geometry
    geonode_tree.links.new(node_join_geometry.outputs['Geometry'], node_output.inputs['Geometry'])

    # --- 4. Create and Assign Materials ---
    # Candy Material
    candy_mat = bpy.data.materials.new(name=f"{base_object_name}_Mat")
    candy_mat.use_nodes = True
    bsdf_node = candy_mat.node_tree.nodes.get('Principled BSDF')
    if bsdf_node:
        bsdf_node.inputs['Base Color'].default_value = candy_color
        bsdf_node.inputs['Transmission'].default_value = candy_transmission
        bsdf_node.inputs['Roughness'].default_value = 0.3 # Default roughness
    candy_obj.data.materials.append(candy_mat)

    # Crystal Material
    crystal_mat = bpy.data.materials.new(name=f"{crystal_object_name}_Mat")
    crystal_mat.use_nodes = True
    bsdf_node = crystal_mat.node_tree.nodes.get('Principled BSDF')
    if bsdf_node:
        bsdf_node.inputs['Base Color'].default_value = crystal_color
        bsdf_node.inputs['Roughness'].default_value = crystal_roughness
        bsdf_node.inputs['Metallic'].default_value = 0.0 # Clear, not metallic
    crystal_source_obj.data.materials.append(crystal_mat)


    # --- 5. Position and Scale ---
    candy_obj.location = mathutils.Vector(location)
    candy_obj.scale = (scale, scale, scale)

    # --- 6. Finalize ---
    bpy.context.view_layer.objects.active = candy_obj
    bpy.ops.object.select_all(action='DESELECT')
    candy_obj.select_set(True)

    return f"Created '{base_object_name}' with '{crystal_object_name}' instances at {location}."

# Example Usage (uncomment to run in Blender's Python console)
# result = create_procedural_sugar_coating(
#     location=(0, 0, 0),
#     scale=1.5,
#     candy_color=(0.9, 0.1, 0.1, 1.0),
#     crystal_color=(0.98, 0.98, 0.98, 1.0),
#     subdivision_levels=3,
#     density=2500.0,
#     min_crystal_scale=0.08,
#     max_crystal_scale=0.18,
#     min_rotation_radians=0.0,
#     max_rotation_radians=math.tau, # 2 * PI for full randomization
#     crystal_roughness=0.1,
#     candy_transmission=0.7
# )
# print(result)

def create_procedural_sugar_scatter(
    scene_name: str = "Scene",
    base_object_name: str = "SugarCube",
    sugar_crystal_name: str = "SugarCrystal",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_material_color: tuple = (0.7, 0.7, 0.7),
    sugar_material_color: tuple = (1.0, 1.0, 1.0),
    sugar_roughness: float = 0.2,
    sugar_transmission: float = 0.7,
    density_factor: float = 50.0,
    crystal_min_scale: float = 0.1,
    crystal_max_scale: float = 0.3,
    crystal_seed: int = 0,
    subdivision_levels: int = 2,
    **kwargs,
) -> str:
    """
    Creates a base mesh (cube) with procedurally scattered 'sugar crystals'
    using Geometry Nodes, with random rotation and scale.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Name for the base object (e.g., "SugarCube").
        sugar_crystal_name: Name for the instanced sugar crystal object.
        location: (x, y, z) world-space position for the base object.
        scale: Uniform scale factor for the base object.
        base_material_color: (R, G, B) base color for the base object in 0-1 range.
        sugar_material_color: (R, G, B) base color for sugar crystals in 0-1 range.
        sugar_roughness: Roughness value for the sugar crystals material.
        sugar_transmission: Transmission value for the sugar crystals material.
        density_factor: Density of scattered points on the base mesh.
        crystal_min_scale: Minimum uniform scale for individual sugar crystals.
        crystal_max_scale: Maximum uniform scale for individual sugar crystals.
        crystal_seed: Seed for randomizing crystal placement and properties.
        subdivision_levels: Levels of subdivision for the base cube.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'SugarCube' with scattered crystals at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Create / Get Sugar Crystal Object (for instancing) ---
    sugar_crystal_obj = bpy.data.objects.get(sugar_crystal_name)
    if sugar_crystal_obj:
        # Update existing crystal object
        if sugar_crystal_obj.type == 'MESH':
            # Optionally clear existing mesh data if needed for fresh start
            # sugar_crystal_obj.data.clear_geometry()
            pass # Keep existing mesh for now
        else:
            bpy.data.objects.remove(sugar_crystal_obj, do_unlink=True)
            sugar_crystal_obj = None # Recreate if not mesh

    if not sugar_crystal_obj:
        bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(0,0,0))
        sugar_crystal_obj = bpy.context.active_object
        sugar_crystal_obj.name = sugar_crystal_name
        
    # Apply initial scale (important for Geometry Nodes instancing)
    sugar_crystal_obj.scale = (0.1, 0.1, 0.1) # Small initial size
    bpy.context.view_layer.objects.active = sugar_crystal_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Hide the sugar crystal object from viewport and render
    sugar_crystal_obj.hide_set(True)
    sugar_crystal_obj.hide_render = True

    # Assign sugar crystal material
    sugar_mat = bpy.data.materials.get(f"{sugar_crystal_name}_Material")
    if not sugar_mat:
        sugar_mat = bpy.data.materials.new(name=f"{sugar_crystal_name}_Material")
        sugar_mat.use_nodes = True
        bsdf_node = sugar_mat.node_tree.nodes["Principled BSDF"]
        bsdf_node.inputs["Base Color"].default_value = (*sugar_material_color, 1.0)
        bsdf_node.inputs["Roughness"].default_value = sugar_roughness
        bsdf_node.inputs["Transmission"].default_value = sugar_transmission
    if sugar_crystal_obj.data.materials:
        sugar_crystal_obj.data.materials[0] = sugar_mat
    else:
        sugar_crystal_obj.data.materials.append(sugar_mat)

    # --- Create Base Object (Cube) ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, enter_editmode=False, align='WORLD', location=location)
    base_obj = bpy.context.active_object
    base_obj.name = base_object_name
    base_obj.scale = (scale, scale, scale)
    
    # Assign base material
    base_mat = bpy.data.materials.get(f"{base_object_name}_Material")
    if not base_mat:
        base_mat = bpy.data.materials.new(name=f"{base_object_name}_Material")
        base_mat.use_nodes = True
        bsdf_node_base = base_mat.node_tree.nodes["Principled BSDF"]
        bsdf_node_base.inputs["Base Color"].default_value = (*base_material_color, 1.0)
    if base_obj.data.materials:
        base_obj.data.materials[0] = base_mat
    else:
        base_obj.data.materials.append(base_mat)

    # Add Subdivision Surface Modifier
    if subdivision_levels > 0:
        subdiv_mod = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv_mod.levels = subdivision_levels
        subdiv_mod.render_levels = subdivision_levels
        bpy.ops.object.shade_smooth()


    # --- Setup Geometry Nodes ---
    gn_modifier = base_obj.modifiers.new(name="GeometryNodes", type='NODES')
    gn_tree_name = f"{base_object_name}_SugarScatter_GN"
    node_group = bpy.data.node_groups.get(gn_tree_name)
    if not node_group:
        node_group = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')
    gn_modifier.node_group = node_group

    # Clear existing nodes for a fresh setup
    for node in node_group.nodes:
        node_group.nodes.remove(node)

    # Add Group Input and Group Output
    group_input = node_group.nodes.new(type='NodeGroupInput')
    group_input.location = (-800, 0)
    group_output = node_group.nodes.new(type='NodeGroupOutput')
    group_output.location = (800, 0)

    # Add Distribute Points on Faces
    distribute_points = node_group.nodes.new(type='GeometryNode_PointsDistribute')
    distribute_points.location = (-400, 200)
    distribute_points.inputs['Density'].default_value = density_factor
    distribute_points.inputs['Seed'].default_value = crystal_seed

    # Add Object Info for the Sugar Crystal
    obj_info_crystal = node_group.nodes.new(type='GeometryNodeObjectInfo')
    obj_info_crystal.location = (-400, -300)
    obj_info_crystal.inputs['Object'].default_value = sugar_crystal_obj
    obj_info_crystal.inputs['As Instance'].default_value = True # Essential for instancing

    # Add Instance on Points
    instance_on_points = node_group.nodes.new(type='GeometryNodeInstanceOnPoints')
    instance_on_points.location = (0, 0)

    # Add Random Value (Vector) for Rotation
    random_rot_val = node_group.nodes.new(type='FunctionNodeRandomValue')
    random_rot_val.location = (-200, -100)
    random_rot_val.data_type = 'FLOAT_VECTOR'
    random_rot_val.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    random_rot_val.inputs['Max'].default_value = (math.tau, math.tau, math.tau) # Full 360 deg rotation
    random_rot_val.inputs['Seed'].default_value = crystal_seed # Use shared seed

    # Add Random Value (Float) for Scale
    random_scale_val = node_group.nodes.new(type='FunctionNodeRandomValue')
    random_scale_val.location = (-200, -200)
    random_scale_val.data_type = 'FLOAT'
    random_scale_val.inputs['Min'].default_value = crystal_min_scale
    random_scale_val.inputs['Max'].default_value = crystal_max_scale
    random_scale_val.inputs['Seed'].default_value = crystal_seed # Use shared seed

    # Add Join Geometry
    join_geometry = node_group.nodes.new(type='GeometryNodeJoinGeometry')
    join_geometry.location = (400, 0)

    # --- Create Node Links ---
    # Base geometry to distribute points
    node_group.links.new(group_input.outputs['Geometry'], distribute_points.inputs['Mesh'])

    # Distribute points to instance on points
    node_group.links.new(distribute_points.outputs['Points'], instance_on_points.inputs['Points'])

    # Sugar crystal object to instance on points
    node_group.links.new(obj_info_crystal.outputs['Geometry'], instance_on_points.inputs['Instance'])

    # Random rotation to instance on points
    node_group.links.new(random_rot_val.outputs['Value'], instance_on_points.inputs['Rotation'])

    # Random scale to instance on points
    node_group.links.new(random_scale_val.outputs['Value'], instance_on_points.inputs['Scale'])
    
    # Instance on points to Join Geometry
    node_group.links.new(instance_on_points.outputs['Instances'], join_geometry.inputs['Geometry'])
    
    # Original Base Geometry to Join Geometry (so the original cube is visible)
    node_group.links.new(group_input.outputs['Geometry'], join_geometry.inputs['Geometry'])

    # Join Geometry to Group Output
    node_group.links.new(join_geometry.outputs['Geometry'], group_output.inputs['Geometry'])
    
    # Set the sugar crystal's material for instancing (Blender 3.2+ setup)
    set_material_node = node_group.nodes.new(type='GeometryNodeSetMaterial')
    set_material_node.location = (200, -100)
    set_material_node.inputs[1].default_value = sugar_mat
    node_group.links.new(instance_on_points.outputs['Instances'], set_material_node.inputs['Geometry'])
    node_group.links.new(set_material_node.outputs['Geometry'], join_geometry.inputs['Geometry'])


    return f"Created '{base_object_name}' with '{sugar_crystal_name}' instances at {location}"


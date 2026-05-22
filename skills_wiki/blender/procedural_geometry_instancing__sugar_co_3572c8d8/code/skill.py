def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the candy.
        **kwargs: 
            density (float): Density of the scattered sugar (default: 3000.0)

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    density = kwargs.get("density", 3000.0)

    # === Step 1: Create Materials ===
    
    # 1a. Candy Material (Gummy)
    mat_candy = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    mat_candy.use_nodes = True
    bsdf_candy = mat_candy.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        bsdf_candy.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_candy.inputs['Roughness'].default_value = 0.3

    # 1b. Sugar Material (Glassy/Refractive)
    mat_sugar = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    mat_sugar.use_nodes = True
    bsdf_sugar = mat_sugar.node_tree.nodes.get("Principled BSDF")
    if bsdf_sugar:
        bsdf_sugar.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_sugar.inputs['Roughness'].default_value = 0.1
        # Use Transmission for a glassy look (handling API differences gracefully)
        if 'Transmission Weight' in bsdf_sugar.inputs: # Blender 4.0+
            bsdf_sugar.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_sugar.inputs: # Blender 3.x
            bsdf_sugar.inputs['Transmission'].default_value = 1.0

    # === Step 2: Create Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -10))  # Hide it below the scene
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_CrystalInstance"
    crystal_obj.data.materials.append(mat_sugar)
    # Hide the source instance from viewport and render
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Create Base Mesh (Candy Torus) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=48, 
        minor_segments=24,
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    candy_obj.scale = (scale, scale, scale)
    candy_obj.data.materials.append(mat_candy)
    bpy.ops.object.shade_smooth()

    # === Step 4: Setup Geometry Nodes ===
    # Create a new node group
    gn_group = bpy.data.node_groups.new(name=f"{object_name}_SugarCoating", type="GeometryNodeTree")
    
    # Handle Input/Output creation across Blender versions (3.x vs 4.0+)
    if hasattr(gn_group, "interface"): # Blender 4.0+
        gn_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type="NodeSocketGeometry")
        gn_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type="NodeSocketGeometry")
    else: # Blender 3.x
        gn_group.inputs.new("NodeSocketGeometry", "Geometry")
        gn_group.outputs.new("NodeSocketGeometry", "Geometry")

    # Clear default nodes if any, then create fresh ones
    gn_group.nodes.clear()

    node_in = gn_group.nodes.new("NodeGroupInput")
    node_in.location = (-400, 0)
    
    node_out = gn_group.nodes.new("NodeGroupOutput")
    node_out.location = (600, 0)

    node_distribute = gn_group.nodes.new("GeometryNodeDistributePointsOnFaces")
    node_distribute.location = (-150, 100)
    node_distribute.inputs['Density'].default_value = density

    node_instance = gn_group.nodes.new("GeometryNodeInstanceOnPoints")
    node_instance.location = (150, 100)

    node_join = gn_group.nodes.new("GeometryNodeJoinGeometry")
    node_join.location = (400, 0)

    node_obj_info = gn_group.nodes.new("GeometryNodeObjectInfo")
    node_obj_info.location = (-150, -100)
    node_obj_info.inputs['Object'].default_value = crystal_obj

    # Random Rotation (0 to Tau for full 360 randomization)
    node_rand_rot = gn_group.nodes.new("FunctionNodeRandomValue")
    node_rand_rot.location = (-150, -300)
    node_rand_rot.data_type = 'FLOAT_VECTOR'
    node_rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    # Random Scale (so crystals vary in size)
    node_rand_scale = gn_group.nodes.new("FunctionNodeRandomValue")
    node_rand_scale.location = (-150, -500)
    node_rand_scale.data_type = 'FLOAT'
    node_rand_scale.inputs['Min'].default_value = 0.02
    node_rand_scale.inputs['Max'].default_value = 0.06

    # Link nodes
    links = gn_group.links
    
    # Original mesh to Join
    links.new(node_in.outputs[0], node_join.inputs[0])
    # Original mesh to Distribute
    links.new(node_in.outputs[0], node_distribute.inputs[0])
    
    # Distribute -> Instance
    links.new(node_distribute.outputs['Points'], node_instance.inputs['Points'])
    # Object Info -> Instance
    # In newer Blender versions, Object Info output is 'Geometry', in older it might be 'Geometry' or 'Instance'
    geom_out_socket = node_obj_info.outputs.get('Geometry') or node_obj_info.outputs.get('Instance')
    links.new(geom_out_socket, node_instance.inputs['Instance'])
    
    # Randoms -> Instance
    links.new(node_rand_rot.outputs['Value'], node_instance.inputs['Rotation'])
    links.new(node_rand_scale.outputs[0], node_instance.inputs['Scale'])
    
    # Instance -> Join -> Output
    links.new(node_instance.outputs['Instances'], node_join.inputs[0])
    links.new(node_join.outputs['Geometry'], node_out.inputs[0])

    # === Step 5: Assign Modifier ===
    gn_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    gn_mod.node_group = gn_group

    return f"Created '{object_name}' (Candy Base) at {location} with {density} procedurally generated sugar crystals."

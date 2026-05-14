def create_proximity_growth_system(
    scene_name: str = "Scene",
    object_name: str = "ProximityGrowth",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.1),
    base_size: float = 10.0,
    density: float = 500.0,
    falloff: float = 3.0,
    **kwargs,
) -> str:
    """
    Create a Procedural Proximity Growth System in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the base scatter grid.
        location: (x, y, z) world-space position of the grid.
        scale: Uniform scale factor for the instances and layout.
        material_color: (R, G, B) base color of the scattered instances.
        base_size: Dimensions of the generated ground plane.
        density: Distribution density for the instances.
        falloff: Radius of the proximity effect (growth radius).
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Materials ===
    grass_mat = bpy.data.materials.new(name=f"{object_name}_InstMat")
    grass_mat.use_nodes = True
    bsdf_grass = grass_mat.node_tree.nodes.get('Principled BSDF')
    if bsdf_grass:
        if 'Base Color' in bsdf_grass.inputs:
            bsdf_grass.inputs['Base Color'].default_value = (*material_color, 1.0)
        if 'Roughness' in bsdf_grass.inputs:
            bsdf_grass.inputs['Roughness'].default_value = 0.8

    ground_mat = bpy.data.materials.new(name=f"{object_name}_GroundMat")
    ground_mat.use_nodes = True
    bsdf_ground = ground_mat.node_tree.nodes.get('Principled BSDF')
    if bsdf_ground:
        if 'Base Color' in bsdf_ground.inputs:
            bsdf_ground.inputs['Base Color'].default_value = (0.05, 0.04, 0.03, 1.0)

    # === Step 2: Instance Object (Grass Blade / Object) ===
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.05*scale, depth=0.4*scale, location=location)
    inst_obj = bpy.context.active_object
    inst_obj.name = f"{object_name}_Instance"
    
    # Shift origin to the bottom of the geometry so it scales upward from the ground
    me = inst_obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    for v in bm.verts:
        v.co.z += 0.2 * scale
    bm.to_mesh(me)
    bm.free()
    
    inst_obj.data.materials.append(grass_mat)
    inst_obj.hide_viewport = True
    inst_obj.hide_render = True

    # === Step 3: Proximity Effector Object ===
    effector_loc = (location[0], location[1], location[2] + falloff * 0.8)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=falloff * scale, location=effector_loc)
    prox_obj = bpy.context.active_object
    prox_obj.name = f"{object_name}_Effector"
    prox_obj.display_type = 'BOUNDS'
    prox_obj.hide_render = True

    # === Step 4: Base Object & Geometry Nodes Setup ===
    bpy.ops.mesh.primitive_plane_add(size=base_size*scale, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    
    mod = base_obj.modifiers.new(name="Proximity Growth", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_GNTree", type='GeometryNodeTree')
    mod.node_group = tree
    tree.nodes.clear()

    # Dynamic output socket creation (supports both 3.x and 4.x APIs)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='OUT', socket_type='NodeSocketGeometry')
    else:
        tree.outputs.new('NodeSocketGeometry', "Geometry")
        
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (800, 0)
    
    # Grid generation
    grid_node = tree.nodes.new('GeometryNodeMeshGrid')
    grid_node.location = (-600, 0)
    grid_node.inputs['Size X'].default_value = base_size * scale
    grid_node.inputs['Size Y'].default_value = base_size * scale
    grid_node.inputs['Vertices X'].default_value = int(base_size * 4)
    grid_node.inputs['Vertices Y'].default_value = int(base_size * 4)
    
    set_mat_grid = tree.nodes.new('GeometryNodeSetMaterial')
    set_mat_grid.location = (-400, -50)
    set_mat_grid.inputs['Material'].default_value = ground_mat

    dist_node = tree.nodes.new('GeometryNodeDistributePointsOnFaces')
    dist_node.location = (-200, 0)
    dist_node.inputs['Density'].default_value = density
    
    inst_node = tree.nodes.new('GeometryNodeInstanceOnPoints')
    inst_node.location = (400, 0)
    
    join_node = tree.nodes.new('GeometryNodeJoinGeometry')
    join_node.location = (600, 0)
    
    # Instance targeting
    obj_info_inst = tree.nodes.new('GeometryNodeObjectInfo')
    obj_info_inst.location = (200, -200)
    obj_info_inst.inputs['Object'].default_value = inst_obj
    
    # Proximity targeting
    obj_info_prox = tree.nodes.new('GeometryNodeObjectInfo')
    obj_info_prox.location = (-600, 300)
    obj_info_prox.inputs['Object'].default_value = prox_obj
    obj_info_prox.transform_space = 'RELATIVE' # Crucial for moving the effector
    
    prox_node = tree.nodes.new('GeometryNodeProximity')
    prox_node.location = (-400, 300)
    
    # Math: Re-map distance (0 -> 1, Falloff -> 0)
    map_math = tree.nodes.new('ShaderNodeMath')
    map_math.operation = 'MULTIPLY_ADD'
    map_math.use_clamp = True
    map_math.inputs[1].default_value = -1.0 / (falloff * scale) # Multiplier
    map_math.inputs[2].default_value = 1.0                      # Addend
    map_math.location = (-200, 300)
    
    # Math: Add scale variation
    rand_scale = tree.nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.3
    rand_scale.inputs['Max'].default_value = 1.0
    rand_scale.location = (-200, 100)
    
    mult_math = tree.nodes.new('ShaderNodeMath')
    mult_math.operation = 'MULTIPLY'
    mult_math.location = (0, 200)
    
    comb_scale = tree.nodes.new('ShaderNodeCombineXYZ')
    comb_scale.location = (200, 50)
    
    # Rotation variation
    rand_rot = tree.nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT'
    rand_rot.inputs['Min'].default_value = 0.0
    rand_rot.inputs['Max'].default_value = math.pi * 2
    rand_rot.location = (0, -300)
    
    comb_rot = tree.nodes.new('ShaderNodeCombineXYZ')
    comb_rot.location = (200, -350)

    # === Step 5: Tree Linking ===
    links = tree.links
    
    # Base geo flow
    links.new(grid_node.outputs['Mesh'], set_mat_grid.inputs['Geometry'])
    links.new(set_mat_grid.outputs['Geometry'], dist_node.inputs['Mesh'])
    links.new(dist_node.outputs['Points'], inst_node.inputs['Points'])
    links.new(obj_info_inst.outputs['Geometry'], inst_node.inputs['Instance'])
    
    links.new(set_mat_grid.outputs['Geometry'], join_node.inputs['Geometry'])
    links.new(inst_node.outputs['Instances'], join_node.inputs['Geometry'])
    links.new(join_node.outputs['Geometry'], out_node.inputs['Geometry'])
    
    # Proximity calculation flow
    links.new(obj_info_prox.outputs['Geometry'], prox_node.inputs['Target'])
    links.new(prox_node.outputs['Distance'], map_math.inputs[0])
    
    # Scale calculation flow
    links.new(map_math.outputs['Value'], mult_math.inputs[0])
    links.new(rand_scale.outputs['Value'], mult_math.inputs[1])
    
    links.new(mult_math.outputs['Value'], comb_scale.inputs['X'])
    links.new(mult_math.outputs['Value'], comb_scale.inputs['Y'])
    links.new(mult_math.outputs['Value'], comb_scale.inputs['Z'])
    links.new(comb_scale.outputs['Vector'], inst_node.inputs['Scale'])
    
    # Rotation flow
    links.new(rand_rot.outputs['Value'], comb_rot.inputs['Z'])
    links.new(comb_rot.outputs['Vector'], inst_node.inputs['Rotation'])

    # Deselect all and select base
    bpy.ops.object.select_all(action='DESELECT')
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj

    return f"Created proximity growth system '{object_name}' with effector '{prox_obj.name}' at {location}."

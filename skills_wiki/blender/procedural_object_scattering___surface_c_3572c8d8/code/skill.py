def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCoatedGummy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create Procedural Object Scattering & Surface Coating in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy object.
        **kwargs: Overrides like 'density' for the scattering.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create the Instance Object (Sugar Crystal) ---
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(location[0], location[1], location[2] - 10))
    sugar_obj = bpy.context.active_object
    sugar_obj.name = f"{object_name}_SugarParticle"
    # Hide the source instance so only the scattered ones are visible
    sugar_obj.hide_set(True)
    sugar_obj.hide_render = True

    # --- 2. Create the Base Object (Gummy Torus) ---
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.45, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Add Subdivision Surface for a smoother distribution surface
    subsurf = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # --- 3. Setup Materials ---
    # Gummy Material
    gummy_mat = bpy.data.materials.new(name=f"{object_name}_GummyMat")
    gummy_mat.use_nodes = True
    gummy_bsdf = gummy_mat.node_tree.nodes.get("Principled BSDF")
    if gummy_bsdf:
        gummy_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        gummy_bsdf.inputs["Roughness"].default_value = 0.25
        # Handle cross-version transmission names (4.0 uses Transmission Weight)
        if gummy_bsdf.inputs.get("Transmission Weight"):
            gummy_bsdf.inputs["Transmission Weight"].default_value = 0.85
        elif gummy_bsdf.inputs.get("Transmission"):
            gummy_bsdf.inputs["Transmission"].default_value = 0.85
    base_obj.data.materials.append(gummy_mat)

    # Sugar Material
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    sugar_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if sugar_bsdf:
        sugar_bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)
        sugar_bsdf.inputs["Roughness"].default_value = 0.1
        if sugar_bsdf.inputs.get("Transmission Weight"):
            sugar_bsdf.inputs["Transmission Weight"].default_value = 0.95
        elif sugar_bsdf.inputs.get("Transmission"):
            sugar_bsdf.inputs["Transmission"].default_value = 0.95
    sugar_obj.data.materials.append(sugar_mat)

    # --- 4. Setup Geometry Nodes ---
    gn_mod = base_obj.modifiers.new(name="SugarCoating", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_GNTree", type='GeometryNodeTree')
    gn_mod.node_group = node_group

    # Initialize interface inputs/outputs (Cross-version support for 3.x and 4.x)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.inputs.new('NodeSocketGeometry', 'Geometry')
        node_group.outputs.new('NodeSocketGeometry', 'Geometry')

    nodes = node_group.nodes
    links = node_group.links

    # Create nodes
    in_node = nodes.new('NodeGroupInput')
    in_node.location = (-600, 0)
    
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (400, 0)

    distribute_node = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute_node.location = (-300, 150)
    distribute_node.inputs['Density'].default_value = kwargs.get('density', 3000.0)

    instance_node = nodes.new('GeometryNodeInstanceOnPoints')
    instance_node.location = (0, 150)

    obj_info_node = nodes.new('GeometryNodeObjectInfo')
    obj_info_node.location = (-300, -100)
    obj_info_node.inputs['Object'].default_value = sugar_obj
    obj_info_node.inputs['As Instance'].default_value = True

    # Random Rotation (Tau = 2*Pi for full 360 rotation on all axes)
    random_rot_node = nodes.new('FunctionNodeRandomValue')
    random_rot_node.location = (-300, -300)
    random_rot_node.data_type = 'FLOAT_VECTOR'
    for inp in random_rot_node.inputs:
        if inp.name == 'Min' and inp.type == 'VECTOR':
            inp.default_value = (0.0, 0.0, 0.0)
        elif inp.name == 'Max' and inp.type == 'VECTOR':
            inp.default_value = (math.pi * 2, math.pi * 2, math.pi * 2)

    # Random Scale
    random_scale_node = nodes.new('FunctionNodeRandomValue')
    random_scale_node.location = (-300, -500)
    random_scale_node.data_type = 'FLOAT'
    for inp in random_scale_node.inputs:
        if inp.name == 'Min' and inp.type == 'VALUE':
            inp.default_value = 0.02
        elif inp.name == 'Max' and inp.type == 'VALUE':
            inp.default_value = 0.06

    join_node = nodes.new('GeometryNodeJoinGeometry')
    join_node.location = (200, 0)

    # Link nodes
    links.new(in_node.outputs[0], distribute_node.inputs['Mesh'])
    links.new(distribute_node.outputs['Points'], instance_node.inputs['Points'])
    links.new(obj_info_node.outputs['Geometry'], instance_node.inputs['Instance'])
    links.new(random_rot_node.outputs['Value'], instance_node.inputs['Rotation'])
    links.new(random_scale_node.outputs['Value'], instance_node.inputs['Scale'])
    
    # Join original mesh with scattered points
    links.new(in_node.outputs[0], join_node.inputs[0])
    links.new(instance_node.outputs['Instances'], join_node.inputs[0])
    
    links.new(join_node.outputs[0], out_node.inputs[0])

    # --- 5. Apply Position and Scale ---
    base_obj.location = Vector(location)
    base_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with Geometry Nodes scattering."

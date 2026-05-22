def create_geometry_nodes_scatter(
    scene_name: str = "Scene",
    object_name: str = "SugaryDonut",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs
) -> str:
    """
    Create a procedural Geometry Nodes scattering system in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the main base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the underlying mesh.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create the Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=location)
    crystal = bpy.context.active_object
    crystal.name = f"{object_name}_Crystal_Instance"
    # Scale to make it slightly rectangular/irregular
    crystal.scale = (0.5, 0.8, 0.5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Hide the source instance from viewport and render
    crystal.hide_viewport = True
    crystal.hide_render = True
    
    # Crystal Material (Transmissive/Glass)
    mat_crystal = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    mat_crystal.use_nodes = True
    bsdf_c = mat_crystal.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        # Handle Blender 4.0+ vs older API for Transmission
        if 'Transmission Weight' in bsdf_c.inputs:
            bsdf_c.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_c.inputs:
            bsdf_c.inputs['Transmission'].default_value = 1.0
        bsdf_c.inputs['Roughness'].default_value = 0.2
        bsdf_c.inputs['IOR'].default_value = 1.55
    crystal.data.materials.append(mat_crystal)

    # === Step 2: Create the Base Object (Donut/Torus) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.4, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    bpy.ops.object.shade_smooth()
    base_obj.scale = (scale, scale, scale)
    
    # Base Material (Candy)
    mat_base = bpy.data.materials.new(name=f"{object_name}_BaseMat")
    mat_base.use_nodes = True
    bsdf_b = mat_base.node_tree.nodes.get("Principled BSDF")
    if bsdf_b:
        bsdf_b.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_b.inputs['Roughness'].default_value = 0.3
    base_obj.data.materials.append(mat_base)

    # === Step 3: Setup Geometry Nodes Modifier ===
    mod = base_obj.modifiers.new(name="Scatter_System", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_ScatterTree", type='GeometryNodeTree')
    mod.node_group = node_group

    # Interface API compatibility (Blender 4.0+ vs Older)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.inputs.new('NodeSocketGeometry', "Geometry")
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # === Step 4: Build Node Tree ===
    group_in = nodes.new('NodeGroupInput')
    group_in.location = (-600, 0)

    group_out = nodes.new('NodeGroupOutput')
    group_out.location = (600, 0)

    # Point Distribution
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-300, 150)
    distribute.inputs['Density'].default_value = 1500.0

    # Instancing
    instance_on_points = nodes.new('GeometryNodeInstanceOnPoints')
    instance_on_points.location = (0, 150)

    # Reference the external object
    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-300, -50)
    obj_info.inputs['Object'].default_value = crystal
    obj_info.transform_space = 'RELATIVE'

    # Combine original and scattered geometry
    join_geo = nodes.new('GeometryNodeJoinGeometry')
    join_geo.location = (300, 0)

    # Randomness for Rotation (0 to math.tau radians on all axes)
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.location = (-300, -250)
    rand_rot.data_type = 'FLOAT_VECTOR'
    for inp in rand_rot.inputs:
        if inp.name == 'Min' and inp.type == 'VECTOR':
            inp.default_value = (0.0, 0.0, 0.0)
        elif inp.name == 'Max' and inp.type == 'VECTOR':
            inp.default_value = (math.tau, math.tau, math.tau)

    # Randomness for Scale (0.2x to 0.8x)
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.location = (-300, -450)
    rand_scale.data_type = 'FLOAT'
    for inp in rand_scale.inputs:
        if inp.name == 'Min' and inp.type == 'VALUE':
            inp.default_value = 0.2
        elif inp.name == 'Max' and inp.type == 'VALUE':
            inp.default_value = 0.8

    # Extract dynamic outputs defensively (API version agnostic)
    rot_out = next((out for out in rand_rot.outputs if out.type == 'VECTOR'), rand_rot.outputs[0])
    scale_out = next((out for out in rand_scale.outputs if out.type == 'VALUE'), rand_scale.outputs[0])

    # === Step 5: Wire the Nodes ===
    links.new(group_in.outputs[0], distribute.inputs['Mesh'])
    links.new(distribute.outputs['Points'], instance_on_points.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], instance_on_points.inputs['Instance'])
    
    links.new(rot_out, instance_on_points.inputs['Rotation'])
    links.new(scale_out, instance_on_points.inputs['Scale'])

    # Join nodes (utilizing multi-input socket of Join Geometry)
    links.new(group_in.outputs[0], join_geo.inputs[0])
    links.new(instance_on_points.outputs[0], join_geo.inputs[0])
    
    # Final Output
    links.new(join_geo.outputs[0], group_out.inputs[0])

    return f"Created Geometry Nodes scatter system '{object_name}' at {location} with {crystal.name} instances."

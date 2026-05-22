def create_object(
    scene_name: str = "Scene",
    object_name: str = "AbstractLoopCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.45, 0.80),
    **kwargs,
) -> str:
    """
    Create an animated, looping abstract cube matrix using Geometry Nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cubes.
        **kwargs: 
            loop_frames (int): Number of frames for a perfect loop (default: 250)
            noise_speed (float): How far the noise evolves over the loop (default: 5.0)

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    loop_frames = kwargs.get("loop_frames", 250)
    noise_speed = kwargs.get("noise_speed", 5.0)

    # === Step 1: Create Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4

    # === Step 2: Create Instance Cube (The small repeating block) ===
    bpy.ops.mesh.primitive_cube_add(size=0.22)
    inst_obj = bpy.context.active_object
    inst_obj.name = f"{object_name}_InstanceBlock"
    inst_obj.data.materials.append(mat)
    
    # Add Bevel for highlights
    bevel = inst_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.width = 0.01
    bpy.ops.object.shade_smooth()
    
    # Hide instance source
    inst_obj.hide_viewport = True
    inst_obj.hide_render = True

    # === Step 3: Create Inner Core Cube (Blocks light in the center) ===
    bpy.ops.mesh.primitive_cube_add(size=1.85)
    inner_cube = bpy.context.active_object
    inner_cube.name = f"{object_name}_InnerCore"
    inner_cube.data.materials.append(mat)
    bpy.ops.object.shade_flat()

    # === Step 4: Create Main GeoNodes Host ===
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    main_obj = bpy.context.active_object
    main_obj.name = f"{object_name}_Matrix"
    
    # === Step 5: Build Geometry Nodes Tree ===
    gn_mod = main_obj.modifiers.new(name="GeoNodes", type='NODES')
    gn_tree = bpy.data.node_groups.new(name=f"{object_name}_Tree", type='GeometryNodeTree')
    gn_mod.node_group = gn_tree

    # Handle I/O sockets based on Blender version
    if bpy.app.version >= (4, 0, 0):
        gn_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.outputs.new('NodeSocketGeometry', 'Geometry')

    nodes = gn_tree.nodes
    links = gn_tree.links

    # Create nodes
    out_node = nodes.new('NodeGroupOutput')
    
    grid_node = nodes.new('GeometryNodeMeshCube')
    grid_node.inputs['Size'].default_value = (2.2, 2.2, 2.2)
    grid_node.inputs['Vertices X'].default_value = 10
    grid_node.inputs['Vertices Y'].default_value = 10
    grid_node.inputs['Vertices Z'].default_value = 10

    info_node = nodes.new('GeometryNodeObjectInfo')
    info_node.inputs['Object'].default_value = inst_obj

    inst_node = nodes.new('GeometryNodeInstanceOnPoints')

    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.noise_dimensions = '4D'
    noise1.inputs['Scale'].default_value = 1.5
    noise1.inputs['Detail'].default_value = 0.0

    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.noise_dimensions = '4D'
    noise2.inputs['Scale'].default_value = 1.5
    noise2.inputs['Detail'].default_value = 0.0

    mix_node = nodes.new('ShaderNodeMix')
    mix_node.data_type = 'RGBA'
    
    # Safely find correct inputs for Mix node (API varies slightly across 3.4+)
    mix_fac_input = mix_node.inputs[0]
    mix_A_input = next(inp for inp in mix_node.inputs if inp.name == 'A' and inp.type == 'RGBA')
    mix_B_input = next(inp for inp in mix_node.inputs if inp.name == 'B' and inp.type == 'RGBA')

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    # Link nodes
    links.new(grid_node.outputs['Mesh'], inst_node.inputs['Points'])
    links.new(info_node.outputs['Geometry'], inst_node.inputs['Instance'])
    links.new(noise1.outputs['Color'], mix_A_input)
    links.new(noise2.outputs['Color'], mix_B_input)
    links.new(mix_node.outputs[2], ramp.inputs['Fac']) # Output 2 is usually the Result Color
    links.new(ramp.outputs['Color'], inst_node.inputs['Scale'])
    links.new(inst_node.outputs['Instances'], out_node.inputs['Geometry'])

    # === Step 6: Setup Procedural Animation Drivers for Looping ===
    
    # 1. Mix Factor Driver: 0 -> 1 over the loop length
    drv_fac = mix_fac_input.driver_add('default_value').driver
    drv_fac.type = 'SCRIPTED'
    drv_fac.expression = f"(frame % {loop_frames}) / {loop_frames}"

    # 2. Noise 1 'W' Driver: 0 -> noise_speed
    drv_w1 = noise1.inputs['W'].driver_add('default_value').driver
    drv_w1.type = 'SCRIPTED'
    drv_w1.expression = f"((frame % {loop_frames}) / {loop_frames}) * {noise_speed}"

    # 3. Noise 2 'W' Driver: -noise_speed -> 0
    drv_w2 = noise2.inputs['W'].driver_add('default_value').driver
    drv_w2.type = 'SCRIPTED'
    drv_w2.expression = f"(((frame % {loop_frames}) / {loop_frames}) * {noise_speed}) - {noise_speed}"

    # === Step 7: Hierarchy, Positioning, and Cleanup ===
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    parent_empty = bpy.context.active_object
    parent_empty.name = object_name
    
    # Parent elements to empty
    main_obj.parent = parent_empty
    inner_cube.parent = parent_empty
    inst_obj.parent = parent_empty
    
    # Reset local transforms
    main_obj.location = (0, 0, 0)
    inner_cube.location = (0, 0, 0)

    # Apply global positioning & slightly rotate for visual interest
    parent_empty.location = location
    parent_empty.scale = (scale, scale, scale)
    parent_empty.rotation_euler = (0.5, 0.5, 0.5)

    return f"Created procedural looping matrix '{object_name}' at {location} configured for a {loop_frames}-frame loop."

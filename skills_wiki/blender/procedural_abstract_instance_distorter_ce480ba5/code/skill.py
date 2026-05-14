def create_object(
    scene_name: str = "Scene",
    object_name: str = "AbstractInstanceGrid",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Procedural Abstract Instance Distorter using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the instances.
        **kwargs: Additional parameters.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create the Source Instance (Suzanne) ===
    target_name = f"{object_name}_SourceTarget"
    
    # Check if target already exists to prevent duplicate clutter
    if target_name in bpy.data.objects:
        suzanne = bpy.data.objects[target_name]
    else:
        current_active = bpy.context.active_object
        
        # Add primitive monkey
        bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0))
        suzanne = bpy.context.active_object
        suzanne.name = target_name
        suzanne.hide_viewport = True # Hide the source object
        suzanne.hide_render = True
        
        # Create and assign material
        mat = bpy.data.materials.new(name=f"{object_name}_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.3
            bsdf.inputs["Metallic"].default_value = 0.0
        suzanne.data.materials.append(mat)
        
        # Restore previously active object
        if current_active:
            bpy.context.view_layer.objects.active = current_active

    # === Step 2: Create the Host Object for Geometry Nodes ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 3: Build the Geometry Nodes Tree ===
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    modifier.node_group = node_group

    nodes = node_group.nodes
    links = node_group.links

    # Clear default nodes
    for n in nodes:
        nodes.remove(n)

    # Create Group Output (Compatible with Blender 3.x and 4.0+)
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (800, 0)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    # Nodes: Generation & Conversion
    grid_node = nodes.new('GeometryNodeMeshGrid')
    grid_node.location = (-600, 0)
    grid_node.inputs['Size X'].default_value = 10.0
    grid_node.inputs['Size Y'].default_value = 10.0
    grid_node.inputs['Vertices X'].default_value = 15
    grid_node.inputs['Vertices Y'].default_value = 15

    m2p_node = nodes.new('GeometryNodeMeshToPoints')
    m2p_node.location = (-400, 0)
    m2p_node.mode = 'FACES' # Convert the center of each face to a point

    # Nodes: Instancing
    iop_node = nodes.new('GeometryNodeInstanceOnPoints')
    iop_node.location = (-200, 0)

    info_node = nodes.new('GeometryNodeObjectInfo')
    info_node.location = (-400, -200)
    info_node.inputs['Object'].default_value = suzanne

    rand_node = nodes.new('FunctionNodeRandomValue')
    rand_node.location = (-400, -400)
    rand_node.data_type = 'FLOAT_VECTOR'
    rand_node.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_node.inputs['Max'].default_value = (math.pi * 2, math.pi * 2, math.pi * 2)

    scale_node = nodes.new('GeometryNodeScaleInstances')
    scale_node.location = (0, 0)
    scale_node.inputs['Scale'].default_value = (0.4, 0.4, 0.4)

    # Nodes: Spatial Mathematics (Attribute reading)
    pos_node = nodes.new('GeometryNodeInputPosition')
    pos_node.location = (0, -200)

    dist_node = nodes.new('ShaderNodeVectorMath')
    dist_node.location = (200, -200)
    dist_node.operation = 'DISTANCE'
    dist_node.inputs[1].default_value = (0.0, 0.0, 0.0) # Calculate distance to origin

    # Scale the distance effect
    math_node = nodes.new('ShaderNodeMath')
    math_node.location = (400, -400)
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 0.5 

    # Route distance to Z-axis offset
    comb_node = nodes.new('ShaderNodeCombineXYZ')
    comb_node.location = (400, -200)

    set_pos_node = nodes.new('GeometryNodeSetPosition')
    set_pos_node.location = (600, 0)

    # === Step 4: Link the Node Tree ===
    # Main geometry flow
    links.new(grid_node.outputs['Mesh'], m2p_node.inputs['Mesh'])
    links.new(m2p_node.outputs['Points'], iop_node.inputs['Points'])
    links.new(iop_node.outputs['Instances'], scale_node.inputs['Instances'])
    links.new(scale_node.outputs['Instances'], set_pos_node.inputs['Geometry'])
    links.new(set_pos_node.outputs['Geometry'], out_node.inputs[0])

    # Instancing logic
    links.new(info_node.outputs['Geometry'], iop_node.inputs['Instance'])
    links.new(rand_node.outputs['Value'], iop_node.inputs['Rotation'])

    # Mathematical distortion logic
    links.new(pos_node.outputs['Position'], dist_node.inputs[0])
    links.new(dist_node.outputs['Value'], math_node.inputs[0])
    links.new(math_node.outputs['Value'], comb_node.inputs['Z'])
    links.new(comb_node.outputs['Vector'], set_pos_node.inputs['Offset'])

    # === Step 5: Finalize Location & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created Geometry Nodes system '{object_name}' with spatially distorted instances at {location}."

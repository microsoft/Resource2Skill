def create_object(
    scene_name: str = "Scene",
    object_name: str = "DistanceScaledGrid",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.3, 0.05),
    **kwargs,
) -> str:
    """
    Create a Procedural Distance-Based Instancing grid in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire host object.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            grid_size: float, size of the procedural grid (default 5.0)
            grid_resolution: int, subdivisions of the grid (default 25)

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # 1. Setup Scene and Host Object
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Create a dummy mesh for the object (will be overridden by Geo Nodes)
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # 2. Create Material
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
        bsdf.inputs['Metallic'].default_value = 0.2

    # 3. Setup Geometry Nodes Modifier
    mod = obj.modifiers.new(name="Distance_Instancing", type='NODES')
    tree = bpy.data.node_groups.new(f"{object_name}_Tree", 'GeometryNodeTree')
    mod.node_group = tree

    # Add default Geometry Node interface for compatibility
    tree.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    tree.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # 4. Build Node Tree (following the tutorial exactly)
    nodes = tree.nodes
    links = tree.links

    # Create Nodes
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (1200, 0)

    # Grid Primitive
    grid_node = nodes.new('GeometryNodeMeshGrid')
    grid_node.location = (-600, 0)
    grid_size = kwargs.get('grid_size', 5.0)
    grid_res = kwargs.get('grid_resolution', 25)
    grid_node.inputs['Size X'].default_value = grid_size
    grid_node.inputs['Size Y'].default_value = grid_size
    grid_node.inputs['Vertices X'].default_value = grid_res
    grid_node.inputs['Vertices Y'].default_value = grid_res

    # Mesh to Points (Faces mode to get nice spacing)
    m2p_node = nodes.new('GeometryNodeMeshToPoints')
    m2p_node.location = (-400, 0)
    m2p_node.mode = 'FACES'

    # Instance geometry (Cube)
    cube_node = nodes.new('GeometryNodeMeshCube')
    cube_node.location = (-400, -200)
    cube_node.inputs['Size'].default_value = (1.0, 1.0, 1.0)

    # Instance on Points
    iop_node = nodes.new('GeometryNodeInstanceOnPoints')
    iop_node.location = (-200, 0)

    # Rotate Instances (45 degrees on Z)
    rot_node = nodes.new('GeometryNodeRotateInstances')
    rot_node.location = (0, 0)
    rot_node.inputs['Rotation'].default_value = (0, 0, math.radians(45))

    # Scale Instances 1 (Base uniform scale reduction)
    scale_base_node = nodes.new('GeometryNodeScaleInstances')
    scale_base_node.location = (200, 0)
    scale_base_node.inputs['Scale'].default_value = (0.2, 0.2, 0.2)

    # Scale Instances 2 (Distance-driven scale)
    scale_dist_node = nodes.new('GeometryNodeScaleInstances')
    scale_dist_node.location = (600, 0)

    # Math Logic: Distance from Position to Origin
    pos_node = nodes.new('GeometryNodeInputPosition')
    pos_node.location = (200, -200)

    dist_node = nodes.new('ShaderNodeVectorMath')
    dist_node.operation = 'DISTANCE'
    dist_node.location = (400, -200)
    dist_node.inputs[1].default_value = (0.0, 0.0, 0.0) # Center origin

    # Set Material
    mat_node = nodes.new('GeometryNodeSetMaterial')
    mat_node.location = (900, 0)
    mat_node.inputs['Material'].default_value = mat

    # 5. Link Nodes
    links.new(grid_node.outputs['Mesh'], m2p_node.inputs['Mesh'])
    links.new(m2p_node.outputs['Points'], iop_node.inputs['Points'])
    links.new(cube_node.outputs['Mesh'], iop_node.inputs['Instance'])
    links.new(iop_node.outputs['Instances'], rot_node.inputs['Instances'])
    links.new(rot_node.outputs['Instances'], scale_base_node.inputs['Instances'])
    links.new(scale_base_node.outputs['Instances'], scale_dist_node.inputs['Instances'])
    
    # Math links
    links.new(pos_node.outputs['Position'], dist_node.inputs[0])
    links.new(dist_node.outputs['Value'], scale_dist_node.inputs['Scale'])
    
    # Final output links
    links.new(scale_dist_node.outputs['Instances'], mat_node.inputs['Geometry'])
    links.new(mat_node.outputs['Geometry'], out_node.inputs['Geometry'])

    return f"Created '{object_name}' (Procedural Grid size {grid_size}x{grid_size}) at {location} utilizing distance-based instancing."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSmoothCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a procedural transformed and smoothed primitive entirely via Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            subdivisions (int): Level of subdivision (default: 3).
            edge_crease (float): Sharpness of the edges (default: 0.2).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Object Container ===
    # Create an empty mesh (the real geometry will be generated via nodes)
    mesh = bpy.data.meshes.new(name=f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # Assign explicit RGB color + Alpha
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4

    # === Step 3: Add & Configure Geometry Nodes Modifier ===
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = group

    # Handle Blender 4.0+ vs 3.x Socket API for the Output Node
    if hasattr(group, "interface"):
        group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        group.outputs.new('NodeSocketGeometry', 'Geometry')

    nodes = group.nodes
    links = group.links

    # Clear default nodes (if any generated)
    nodes.clear()

    # Create Nodes
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (1000, 0)

    # Procedural Primitive
    node_cube = nodes.new('GeometryNodeMeshCube')
    node_cube.location = (0, 0)
    
    # Transformation inside GN
    node_transform = nodes.new('GeometryNodeTransform')
    node_transform.location = (200, 0)
    # Applying internal scale slightly to demonstrate the transform node's capability
    node_transform.inputs['Scale'].default_value = (1.0, 1.0, 1.0)

    # Topology Modification
    node_subdiv = nodes.new('GeometryNodeSubdivisionSurface')
    node_subdiv.location = (400, 0)
    
    # Parameterize Subdivision
    subdivisions = kwargs.get('subdivisions', 3)
    if 'Level' in node_subdiv.inputs:
        node_subdiv.inputs['Level'].default_value = subdivisions
    
    edge_crease = kwargs.get('edge_crease', 0.1)
    if 'Edge Crease' in node_subdiv.inputs:
        node_subdiv.inputs['Edge Crease'].default_value = edge_crease

    # Shading Modification
    node_smooth = nodes.new('GeometryNodeSetShadeSmooth')
    node_smooth.location = (600, 0)

    # Material Assignment Modification
    node_mat = nodes.new('GeometryNodeSetMaterial')
    node_mat.location = (800, 0)
    node_mat.inputs['Material'].default_value = mat

    # === Step 4: Link the Node Graph ===
    links.new(node_cube.outputs['Mesh'], node_transform.inputs['Geometry'])
    links.new(node_transform.outputs['Geometry'], node_subdiv.inputs['Mesh'])
    links.new(node_subdiv.outputs['Mesh'], node_smooth.inputs['Geometry'])
    links.new(node_smooth.outputs['Geometry'], node_mat.inputs['Geometry'])
    links.new(node_mat.outputs['Geometry'], node_out.inputs['Geometry'])

    # === Step 5: Object Level Transforms ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' procedurally at {location} using Geometry Nodes (Subdiv Lvl: {subdivisions})."

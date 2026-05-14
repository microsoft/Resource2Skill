def create_procedural_subdivided_cube(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSmoothCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a procedural smooth cube using Geometry Nodes, matching the tutorial's beginner setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            subdivisions (int): Level of subdivision (default: 3).

    Returns:
        Status string.
    """
    import bpy

    # Get target scene or default to the first one
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Object Container ===
    # Create an empty mesh to hold the Geometry Nodes modifier
    mesh = bpy.data.meshes.new(name=f"{object_name}_mesh")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)
    
    obj.location = location
    obj.scale = (scale, scale, scale)

    # === Step 2: Set up Geometry Nodes Modifier & Tree ===
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    modifier.node_group = node_tree

    # Clear default nodes if any exist
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Create Group Output
    node_output = node_tree.nodes.new(type='NodeGroupOutput')
    node_output.location = (800, 0)
    node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # Create Procedural Cube Node (Replaces Group Input)
    node_cube = node_tree.nodes.new(type='GeometryNodeMeshCube')
    node_cube.location = (-200, 0)
    node_cube.inputs['Size'].default_value = (2.0, 2.0, 2.0) # Default blender cube size

    # Create Transform Geometry Node
    node_transform = node_tree.nodes.new(type='GeometryNodeTransform')
    node_transform.location = (0, 0)

    # Create Subdivision Surface Node
    node_subsurf = node_tree.nodes.new(type='GeometryNodeSubdivisionSurface')
    node_subsurf.location = (200, 0)
    node_subsurf.inputs['Level'].default_value = kwargs.get('subdivisions', 3)

    # Create Set Shade Smooth Node
    node_smooth = node_tree.nodes.new(type='GeometryNodeSetShadeSmooth')
    node_smooth.location = (400, 0)
    node_smooth.inputs['Shade Smooth'].default_value = True

    # Create Set Material Node
    node_material = node_tree.nodes.new(type='GeometryNodeSetMaterial')
    node_material.location = (600, 0)

    # Link the nodes together
    links = node_tree.links
    links.new(node_cube.outputs['Mesh'], node_transform.inputs['Geometry'])
    links.new(node_transform.outputs['Geometry'], node_subsurf.inputs['Mesh'])
    links.new(node_subsurf.outputs['Mesh'], node_smooth.inputs['Geometry'])
    links.new(node_smooth.outputs['Geometry'], node_material.inputs['Geometry'])
    links.new(node_material.outputs['Geometry'], node_output.inputs['Geometry'])

    # === Step 3: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
    
    # Assign material to the node
    node_material.inputs['Material'].default_value = mat

    return f"Created '{object_name}' (Procedural Subdivided Cube) at {location} using Geometry Nodes."

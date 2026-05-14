def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSquircle",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    subdivision_level: int = 3,
    edge_crease: float = 0.5,
    **kwargs,
) -> str:
    """
    Create a Procedural Stylized Squircle using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created dummy object and nodes.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        subdivision_level: Resolution of the rounded cube.
        edge_crease: Tension of the cube corners (0.0 = sphere, 1.0 = sharp cube).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get the target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Lightweight Dummy Object ===
    # Create a single vertex mesh as a container
    mesh = bpy.data.meshes.new(name=f"{object_name}_BaseMesh")
    mesh.from_pydata([(0, 0, 0)], [], [])
    mesh.update()
    
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        base_color_input = bsdf.inputs.get("Base Color")
        if base_color_input:
            base_color_input.default_value = (*material_color, 1.0)
        
        roughness_input = bsdf.inputs.get("Roughness")
        if roughness_input:
            roughness_input.default_value = 0.4

    # === Step 3: Build Geometry Nodes Tree ===
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = node_group

    # Setup interface (handles Blender 4.0+ and backwards compatibility)
    if hasattr(node_group, 'interface'):
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # Output Node
    out_node = nodes.new(type='NodeGroupOutput')
    out_node.location = (600, 0)

    # Procedural Cube Node (Replaces missing Group Input)
    cube_node = nodes.new(type='GeometryNodeMeshCube')
    cube_node.location = (-400, 0)

    # Transform Node
    transform_node = nodes.new(type='GeometryNodeTransform')
    transform_node.location = (-200, 0)

    # Subdivision Surface Node
    subdiv_node = nodes.new(type='GeometryNodeSubdivisionSurface')
    subdiv_node.location = (0, 0)
    if subdiv_node.inputs.get('Level'):
        subdiv_node.inputs['Level'].default_value = subdivision_level
    if subdiv_node.inputs.get('Edge Crease'):
        subdiv_node.inputs['Edge Crease'].default_value = edge_crease

    # Smooth Shading Node
    smooth_node = nodes.new(type='GeometryNodeSetShadeSmooth')
    smooth_node.location = (200, 0)

    # Material Assignment Node
    set_mat_node = nodes.new(type='GeometryNodeSetMaterial')
    set_mat_node.location = (400, 0)
    if set_mat_node.inputs.get('Material'):
        set_mat_node.inputs['Material'].default_value = mat

    # Connect the node flow via indices (robust across API versions)
    links.new(cube_node.outputs[0], transform_node.inputs[0])
    links.new(transform_node.outputs[0], subdiv_node.inputs[0])
    links.new(subdiv_node.outputs[0], smooth_node.inputs[0])
    links.new(smooth_node.outputs[0], set_mat_node.inputs[0])
    links.new(set_mat_node.outputs[0], out_node.inputs[0])

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Procedural Squircle) at {location} using GN Subdivision Level {subdivision_level}."

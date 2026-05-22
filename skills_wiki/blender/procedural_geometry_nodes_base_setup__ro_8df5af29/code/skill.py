def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralRoundedCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.5, 0.8),
    **kwargs,
) -> str:
    """
    Create a Procedural Geometry Nodes Base Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created procedural object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (affects the procedural cube node size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides (e.g., subdivision_level).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get the target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Container Object ===
    # We create an empty mesh because Geometry Nodes will replace the geometry
    mesh = bpy.data.meshes.new(name=f"{object_name}_mesh")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    # Position the container
    obj.location = Vector(location)

    # Add the Geometry Nodes modifier
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # Create a new node tree for the modifier
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = node_tree

    # Handle API differences for creating the output socket (Blender 4.0+ vs older)
    if hasattr(node_tree, "interface"):
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_tree.nodes
    links = node_tree.links

    # === Step 2: Build the Node Graph ===
    # Add Group Output
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (800, 0)

    # Add Primitive Mesh Node
    cube_node = nodes.new('GeometryNodeMeshCube')
    cube_node.location = (0, 0)
    cube_node.inputs['Size'].default_value = Vector((scale, scale, scale))

    # Add Transform Node
    transform_node = nodes.new('GeometryNodeTransform')
    transform_node.location = (200, 0)

    # Add Subdivision Surface Node
    subdiv_node = nodes.new('GeometryNodeSubdivisionSurface')
    subdiv_node.location = (400, 0)
    subdiv_node.inputs['Level'].default_value = kwargs.get('subdivision_level', 3)

    # Add Set Shade Smooth Node
    smooth_node = nodes.new('GeometryNodeSetShadeSmooth')
    smooth_node.location = (600, 0)
    
    # Add Set Material Node
    mat_node = nodes.new('GeometryNodeSetMaterial')
    mat_node.location = (700, 0)

    # === Step 3: Create and Assign Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure the tuple is 4-dimensional (RGBA)
            color_with_alpha = (*material_color, 1.0) if len(material_color) == 3 else material_color
            bsdf.inputs["Base Color"].default_value = color_with_alpha
            bsdf.inputs["Roughness"].default_value = kwargs.get("roughness", 0.4)
            
    # Assign material to the node
    mat_node.inputs['Material'].default_value = mat

    # === Step 4: Link the Nodes ===
    # Flow: Cube -> Transform -> Subdiv -> Shade Smooth -> Set Material -> Output
    links.new(cube_node.outputs['Mesh'], transform_node.inputs['Geometry'])
    links.new(transform_node.outputs['Geometry'], subdiv_node.inputs['Mesh'])
    links.new(subdiv_node.outputs['Mesh'], smooth_node.inputs['Geometry'])
    links.new(smooth_node.outputs['Geometry'], mat_node.inputs['Geometry'])
    links.new(mat_node.outputs['Geometry'], out_node.inputs['Geometry'])

    return f"Created procedural object '{object_name}' at {location} using Geometry Nodes."

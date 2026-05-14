def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralRefinedMesh",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    subsurf_level: int = 3,
    edge_crease: float = 0.4,
    transform_translation: tuple = (0.0, 0.0, 0.0),
    **kwargs,
) -> str:
    """
    Create a procedural geometry node setup that transforms, subdivides, 
    and smooths a base mesh, exactly as demonstrated in the beginner tutorial.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color.
        subsurf_level: Level of procedural subdivision.
        edge_crease: Sharpness of the edges during subdivision (0.0 to 1.0).
        transform_translation: Procedural offset applied inside the node tree.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Retrieve scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Link to scene collection if not already
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
    obj.data.materials.append(mat)

    # === Step 3: Build Geometry Nodes Tree ===
    tree_name = f"{object_name}_GeoNodes"
    node_tree = bpy.data.node_groups.new(name=tree_name, type='GeometryNodeTree')
    
    # Handle socket creation across different Blender versions (3.x vs 4.0+)
    if hasattr(node_tree, "interface"):
        node_tree.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_tree.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.inputs.new("NodeSocketGeometry", "Geometry")
        node_tree.outputs.new("NodeSocketGeometry", "Geometry")

    # Add Nodes
    group_in = node_tree.nodes.new("NodeGroupInput")
    group_in.location = (-400, 0)

    group_out = node_tree.nodes.new("NodeGroupOutput")
    group_out.location = (400, 0)

    transform_node = node_tree.nodes.new("GeometryNodeTransform")
    transform_node.location = (-200, 0)
    transform_node.inputs['Translation'].default_value = transform_translation

    subsurf_node = node_tree.nodes.new("GeometryNodeSubdivisionSurface")
    subsurf_node.location = (0, 0)
    subsurf_node.inputs['Level'].default_value = subsurf_level
    subsurf_node.inputs['Edge Crease'].default_value = edge_crease

    smooth_node = node_tree.nodes.new("GeometryNodeSetShadeSmooth")
    smooth_node.location = (200, 0)

    # Link Nodes
    links = node_tree.links
    links.new(group_in.outputs[0], transform_node.inputs[0])
    links.new(transform_node.outputs[0], subsurf_node.inputs[0])
    links.new(subsurf_node.outputs[0], smooth_node.inputs[0])
    links.new(smooth_node.outputs[0], group_out.inputs[0])

    # === Step 4: Add Modifier to Object ===
    mod = obj.modifiers.new(name="Sub-Surf and Smooth", type='NODES')
    mod.node_group = node_tree

    return f"Created '{object_name}' at {location} with Procedural Geometry setup (Level {subsurf_level} SubSurf)."

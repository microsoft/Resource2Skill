def create_procedural_subdivided_primitive(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSmoothCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs
) -> str:
    """
    Create a procedural subdivided primitive using Geometry Nodes.
    Demonstrates generating geometry from scratch, transforming, subdividing, and smoothing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created procedural object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural material.
        **kwargs: Additional overrides (e.g., subdivision_levels).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    subdiv_levels = kwargs.get("subdivision_levels", 3)

    # === Step 1: Create Base Container Object ===
    # Create an empty mesh to hold the Geometry Nodes modifier
    mesh = bpy.data.meshes.new(name=f"{object_name}_Data")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # === Step 2: Set up Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4

    # === Step 3: Build Geometry Nodes Tree ===
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    modifier.node_group = node_group

    # Clear default nodes (we will generate geometry internally, ignoring Group Input)
    node_group.nodes.clear()

    # 1. Group Output
    group_output = node_group.nodes.new(type='NodeGroupOutput')
    group_output.location = (800, 0)
    node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # 2. Cube Primitive
    cube_node = node_group.nodes.new(type='GeometryNodeMeshCube')
    cube_node.location = (-400, 0)
    cube_node.inputs['Size'].default_value = (1.0, 1.0, 1.0)

    # 3. Transform Geometry
    transform_node = node_group.nodes.new(type='GeometryNodeTransform')
    transform_node.location = (-200, 0)
    # (Transform inputs can be left at default to let object-level transforms handle world placement)

    # 4. Subdivision Surface
    subsurf_node = node_group.nodes.new(type='GeometryNodeSubdivisionSurface')
    subsurf_node.location = (0, 0)
    subsurf_node.inputs['Level'].default_value = subdiv_levels

    # 5. Set Shade Smooth
    shade_smooth_node = node_group.nodes.new(type='GeometryNodeSetShadeSmooth')
    shade_smooth_node.location = (200, 0)
    shade_smooth_node.inputs['Shade Smooth'].default_value = True

    # 6. Set Material
    set_mat_node = node_group.nodes.new(type='GeometryNodeSetMaterial')
    set_mat_node.location = (400, 0)
    set_mat_node.inputs['Material'].default_value = mat

    # === Step 4: Link Nodes ===
    links = node_group.links
    links.new(cube_node.outputs['Mesh'], transform_node.inputs['Geometry'])
    links.new(transform_node.outputs['Geometry'], subsurf_node.inputs['Mesh'])
    links.new(subsurf_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])
    links.new(shade_smooth_node.outputs['Geometry'], set_mat_node.inputs['Geometry'])
    links.new(set_mat_node.outputs['Geometry'], group_output.inputs['Geometry'])

    return f"Created '{object_name}' with procedural Subdivision & Smooth Geometry Nodes at {location}."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralPrimitive",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.9),
    **kwargs,
) -> str:
    """
    Create a Procedural Primitive using Geometry Nodes in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides (e.g., subdivision_level).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Object Container ===
    # Create an empty mesh to act as a container for the Geometry Nodes modifier
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    
    # Link object to the scene collection (Additive)
    scene.collection.objects.link(obj)

    # Position and Scale (Object level)
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
        
    # Append material to object (good practice, though we will explicitly set it in GN)
    obj.data.materials.append(mat)

    # === Step 3: Geometry Nodes Setup ===
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    
    # Create Node Group
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    modifier.node_group = node_group
    
    # Create Output Interface (Compatibility for Blender 4.0+)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    # Instantiate Nodes
    group_out = node_group.nodes.new('NodeGroupOutput')
    group_out.location = (600, 0)

    # Node: Mesh Cube (Procedural Base)
    node_cube = node_group.nodes.new('GeometryNodeMeshCube')
    node_cube.location = (-400, 0)
    
    # Node: Transform Geometry
    node_transform = node_group.nodes.new('GeometryNodeTransform')
    node_transform.location = (-200, 0)
    # Apply a slight rotation offset to prove the transform works
    node_transform.inputs['Rotation'].default_value = (0.2, 0.4, 0.1)

    # Node: Subdivision Surface
    node_subsurf = node_group.nodes.new('GeometryNodeSubdivisionSurface')
    node_subsurf.location = (0, 0)
    subsurf_level = kwargs.get('subdivision_level', 3)
    node_subsurf.inputs['Level'].default_value = subsurf_level

    # Node: Set Shade Smooth
    node_smooth = node_group.nodes.new('GeometryNodeSetShadeSmooth')
    node_smooth.location = (200, 0)
    
    # Node: Set Material (Crucial for procedural primitives)
    node_set_mat = node_group.nodes.new('GeometryNodeSetMaterial')
    node_set_mat.location = (400, 0)
    node_set_mat.inputs['Material'].default_value = mat

    # Link Nodes logically from Left to Right
    links = node_group.links
    links.new(node_cube.outputs['Mesh'], node_transform.inputs['Geometry'])
    links.new(node_transform.outputs['Geometry'], node_subsurf.inputs['Mesh'])
    links.new(node_subsurf.outputs['Mesh'], node_smooth.inputs['Geometry'])
    links.new(node_smooth.outputs['Geometry'], node_set_mat.inputs['Geometry'])
    links.new(node_set_mat.outputs['Geometry'], group_out.inputs['Geometry'])

    return f"Created '{object_name}' procedurally at {location} with Subdivision Level {subsurf_level}."

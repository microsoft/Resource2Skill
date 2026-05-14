def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGeoNodeObject",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Basic Procedural Geometry Node Setup in the active Blender scene.
    Demonstrates generating a primitive, transforming, subdividing, and smoothing it procedurally.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object and node group.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Container Object ===
    # Create an empty mesh to act as a host for the geometry nodes
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Position and scale the container object
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # === Step 2: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4

    # === Step 3: Build Geometry Nodes Setup ===
    # Add modifier
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    
    # Create node group
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = node_group

    # Handle API differences for creating interface sockets (Blender 4.0+ vs older)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # Instantiate Nodes
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (800, 0)

    node_cube = nodes.new('GeometryNodeMeshCube')
    node_cube.location = (-200, 0)
    
    # Allows internal offset independent of object origin
    node_transform = nodes.new('GeometryNodeTransform')
    node_transform.location = (0, 0)
    node_transform.inputs['Translation'].default_value = (0.0, 0.0, 0.5)

    node_subdiv = nodes.new('GeometryNodeSubdivisionSurface')
    node_subdiv.location = (200, 0)
    node_subdiv.inputs['Level'].default_value = 3

    node_smooth = nodes.new('GeometryNodeSetShadeSmooth')
    node_smooth.location = (400, 0)

    node_material = nodes.new('GeometryNodeSetMaterial')
    node_material.location = (600, 0)
    node_material.inputs['Material'].default_value = mat

    # Link the procedural pipeline
    # Cube -> Transform -> Subdivision -> Smooth -> Material -> Output
    links.new(node_cube.outputs['Mesh'], node_transform.inputs['Geometry'])
    links.new(node_transform.outputs['Geometry'], node_subdiv.inputs['Mesh'])
    links.new(node_subdiv.outputs['Mesh'], node_smooth.inputs['Geometry'])
    links.new(node_smooth.outputs['Geometry'], node_material.inputs['Geometry'])
    links.new(node_material.outputs['Geometry'], node_out.inputs['Geometry'])

    return f"Created procedural '{object_name}' at {location} utilizing a complete Geometry Nodes pipeline."

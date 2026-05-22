def create_object(
    scene_name: str = "Scene",
    object_name: str = "SmoothedCube",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    subdivision_level: int = 3,
    edge_crease: float = 0.5,
    cube_size: float = 1.0,
    translation: tuple = (0.0, 0.0, 0.0),
    rotation_euler: tuple = (0.0, 0.0, 0.0),
    transform_scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create a procedurally generated and smoothed cube using Geometry Nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the overall object.
        subdivision_level: Level of subdivision for smoothing (e.g., 3).
        edge_crease: Value to control edge sharpness after subdivision (0.0-1.0).
        cube_size: Size of the internal cube primitive.
        translation: (x, y, z) translation for the internal geometry transform.
        rotation_euler: (x, y, z) rotation in radians for the internal geometry transform.
        transform_scale: Uniform scale for the internal geometry transform.
        material_color: (R, G, B) base color in 0-1 range for a new material.
        **kwargs: Additional overrides (e.g., roughness for material).

    Returns:
        Status string, e.g., "Created 'SmoothedCube' at (0, 0, 0) with Geometry Nodes"
    """
    import bpy
    import mathutils
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a new mesh object to apply Geometry Nodes to
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0,0,0))
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = mathutils.Vector(location)
    obj.scale = (scale, scale, scale)

    # Ensure the object has a material (or create a new one)
    if not obj.data.materials:
        mat_name = f"{object_name}_Material"
        mat = bpy.data.materials.new(name=mat_name)
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*material_color, 1) # R, G, B, Alpha

    # Add Geometry Nodes modifier
    gn_modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # Create a new Geometry Node Tree
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_GN_Tree", type='GeometryNodeTree')
    gn_modifier.node_group = node_tree

    # Clear default nodes (Group Input and Group Output)
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Add Group Output node
    node_output = node_tree.nodes.new(type='NodeGroupOutput')
    node_output.location = (800, 0)
    node_tree.outputs.new('NodeSocketGeometry', 'Geometry')

    # Add Mesh Primitive Cube node
    node_cube_primitive = node_tree.nodes.new(type='GeometryNodeMeshCube')
    node_cube_primitive.location = (-600, 0)
    node_cube_primitive.inputs['Size'].default_value = cube_size

    # Add Transform Geometry node
    node_transform = node_tree.nodes.new(type='GeometryNodeTransform')
    node_transform.location = (-300, 0)
    node_transform.inputs['Translation'].default_value = mathutils.Vector(translation)
    node_transform.inputs['Rotation'].default_value = mathutils.Euler(rotation_euler).to_quaternion() # Convert Euler to Quaternion for node input
    node_transform.inputs['Scale'].default_value = (transform_scale, transform_scale, transform_scale)

    # Add Subdivision Surface node
    node_subdiv = node_tree.nodes.new(type='GeometryNodeSubdivisionSurface')
    node_subdiv.location = (0, 0)
    node_subdiv.inputs['Level'].default_value = subdivision_level
    node_subdiv.inputs['Edge Crease'].default_value = edge_crease

    # Add Set Shade Smooth node
    node_set_shade_smooth = node_tree.nodes.new(type='GeometryNodeSetShadeSmooth')
    node_set_shade_smooth.location = (400, 0)
    node_set_shade_smooth.inputs['Shade Smooth'].default_value = True

    # Link nodes
    node_tree.links.new(node_cube_primitive.outputs['Mesh'], node_transform.inputs['Geometry'])
    node_tree.links.new(node_transform.outputs['Geometry'], node_subdiv.inputs['Mesh'])
    node_tree.links.new(node_subdiv.outputs['Mesh'], node_set_shade_smooth.inputs['Geometry'])
    node_tree.links.new(node_set_shade_smooth.outputs['Geometry'], node_output.inputs['Geometry'])

    return f"Created '{object_name}' at {location} with Geometry Nodes"


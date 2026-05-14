def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR Material Setup with Adaptive Displacement in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render Engine Setup ===
    # Displacement requires Cycles and Experimental feature set for Adaptive Subdivision
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6
    
    # Enable Adaptive Subdivision if available
    if hasattr(obj.cycles, 'use_adaptive_subdivision'):
        obj.cycles.use_adaptive_subdivision = True

    # === Step 3: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Set Displacement Method to 'Displacement and Bump' (enum is 'BOTH')
    if hasattr(mat.cycles, 'displacement_method'):
        mat.cycles.displacement_method = 'BOTH'

    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Output & BSDF Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinate & Mapping Nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Procedural Color Map
    color_tex = nodes.new(type='ShaderNodeTexVoronoi')
    color_tex.location = (-300, 300)
    color_tex.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])

    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-50, 300)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    links.new(color_tex.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # Procedural Roughness Map (mimicking Inverted Gloss from tutorial)
    rough_tex = nodes.new(type='ShaderNodeTexNoise')
    rough_tex.location = (-300, 0)
    rough_tex.inputs['Scale'].default_value = 10.0
    links.new(mapping.outputs['Vector'], rough_tex.inputs['Vector'])

    invert_node = nodes.new(type='ShaderNodeInvert')
    invert_node.location = (-100, 0)
    links.new(rough_tex.outputs['Fac'], invert_node.inputs['Color'])

    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (100, 0)
    rough_ramp.color_ramp.elements[0].position = 0.3
    rough_ramp.color_ramp.elements[1].position = 0.8
    links.new(invert_node.outputs['Color'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    # Procedural Normal Map (using Bump node for grayscale to vector conversion)
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (300, -200)
    bump_node.inputs['Strength'].default_value = 0.5
    links.new(rough_tex.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # Procedural Displacement Map (The core geometry driver)
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (600, -300)
    disp_node.inputs['Scale'].default_value = 0.1
    disp_node.inputs['Midlevel'].default_value = 0.0
    links.new(color_tex.outputs['Distance'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' with automated procedural PBR material and Cycles adaptive displacement at {location}"

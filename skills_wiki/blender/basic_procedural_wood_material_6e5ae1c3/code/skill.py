def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralWoodBlock",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a mesh with a basic procedural wood material in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used for the lighter part of the wood grain.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    # Ensure we are in object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Procedural Material ===
    mat_name = f"{object_name}_WoodMaterial"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes just in case, though standard adds Principled + Output
    for node in nodes:
        nodes.remove(node)

    # Add required nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (300, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (-300, -200)
    bump_node.inputs['Strength'].default_value = 0.15
    bump_node.inputs['Distance'].default_value = 0.1

    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    color_ramp_node.location = (-300, 100)
    
    # Configure wood colors (Dark stop and Light stop)
    color_ramp_node.color_ramp.elements[0].position = 0.2
    color_ramp_node.color_ramp.elements[0].color = (0.05, 0.02, 0.01, 1.0) # Very dark brown
    
    color_ramp_node.color_ramp.elements[1].position = 0.8
    # Map the requested material color to the lighter wood grain
    color_ramp_node.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    noise_node = nodes.new(type='ShaderNodeTexNoise')
    noise_node.location = (-550, 0)
    noise_node.inputs['Scale'].default_value = 5.0
    noise_node.inputs['Detail'].default_value = 15.0
    noise_node.inputs['Roughness'].default_value = 0.6
    noise_node.inputs['Distortion'].default_value = 2.0 # Creates the wavy wood look

    mapping_node = nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (-750, 0)
    # Stretch the noise significantly along Z, and compress slightly on X
    mapping_node.inputs['Scale'].default_value = (3.0, 1.0, 0.1)

    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    tex_coord_node.location = (-950, 0)

    # === Step 3: Link Nodes ===
    # Coordinate system -> Mapping -> Noise
    links.new(tex_coord_node.outputs['Object'], mapping_node.inputs['Vector'])
    links.new(mapping_node.outputs['Vector'], noise_node.inputs['Vector'])
    
    # Noise -> ColorRamp -> Base Color
    links.new(noise_node.outputs['Fac'], color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Noise -> Bump -> Normal
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # BSDF -> Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Set some base BSDF properties for wood
    bsdf_node.inputs['Roughness'].default_value = 0.65
    bsdf_node.inputs['Specular IOR Level'].default_value = 0.3

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created '{object_name}' at {location} with Procedural Wood Material."

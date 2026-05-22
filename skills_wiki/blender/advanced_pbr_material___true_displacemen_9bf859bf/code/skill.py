def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create an Advanced PBR Material Pipeline with True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Extraneous arguments.

    Returns:
        Status string describing the operation.
    """
    import bpy
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Enable Experimental feature set for Adaptive Subdivision in Cycles
    if hasattr(scene, 'cycles'):
        scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for true displacement geometry
    subdiv = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    
    # Enable adaptive subdivision if Cycles is available
    if hasattr(obj, 'cycles'):
        obj.cycles.use_adaptive_subdivision = True

    # === Step 2: Build Advanced PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # Output & Principled BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (900, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Global Mapping Setup
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Unified Scale Value node
    scale_val = nodes.new('ShaderNodeValue')
    scale_val.location = (-600, -200)
    scale_val.outputs['Value'].default_value = 5.0
    links.new(scale_val.outputs['Value'], mapping.inputs['Scale'])

    # --- BASE COLOR CHANNEL ---
    # Simulating Color Image Texture
    color_tex = nodes.new('ShaderNodeTexNoise')
    color_tex.location = (-100, 300)
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 300)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = material_color + (1.0,)
    
    # Hue/Saturation node for tweaking
    hsv_node = nodes.new('ShaderNodeHueSaturation')
    hsv_node.location = (500, 300)
    
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])
    links.new(color_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], hsv_node.inputs['Color'])
    links.new(hsv_node.outputs['Color'], bsdf_node.inputs['Base Color'])

    # --- ROUGHNESS (INVERTED GLOSS) CHANNEL ---
    # Simulating Gloss Image Texture (Non-Color Data equivalent)
    gloss_tex = nodes.new('ShaderNodeTexMusgrave') 
    gloss_tex.location = (-100, 0)
    
    # Invert node to convert Gloss to Roughness
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])
    links.new(gloss_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])

    # --- NORMAL CHANNEL ---
    # Simulating Normal Map (using Voronoi to generate bump data)
    bump_tex = nodes.new('ShaderNodeTexVoronoi')
    bump_tex.location = (-100, -300)
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -300)
    bump_node.inputs['Strength'].default_value = 0.5
    
    links.new(mapping.outputs['Vector'], bump_tex.inputs['Vector'])
    links.new(bump_tex.outputs['Distance'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # --- TRUE DISPLACEMENT CHANNEL ---
    # Simulating Displacement Map (Non-Color Data equivalent)
    disp_tex = nodes.new('ShaderNodeTexNoise')
    disp_tex.location = (200, -600)
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (900, -600)
    disp_node.inputs['Midlevel'].default_value = 0.0 # Crucial setting from tutorial
    disp_node.inputs['Scale'].default_value = 0.1   # Tweaked displacement scale
    
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    # Plug directly into Material Output, NOT Principled BSDF
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created PBR Object '{object_name}' at {location} with adaptive subdivision and true displacement enabled."

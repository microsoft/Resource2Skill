def create_pbr_pipeline_material(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    base_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a heavily subdivided plane demonstrating a full PBR shading pipeline.
    Implements Color Tweaking, Gloss Inversion, universal mapping scale, and true Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color: (R, G, B) base color mapping target.

    Returns:
        Status string.
    """
    import bpy

    # Force Cycles engine as it is required for true Displacement
    if bpy.context.scene.render.engine != 'CYCLES':
        bpy.context.scene.render.engine = 'CYCLES'

    # === Step 1: Create Geometry for Displacement ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Subdivide mesh to provide vertices for the displacement node to push/pull
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps edges square
    subsurf.levels = 6
    subsurf.render_levels = 6
    
    # === Step 2: Initialize Material & Settings ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Tell Cycles to use true physical displacement, not just fake bump
    mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # === Step 3: Build Core Shader Nodes ===
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (800, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    
    # === Step 4: Universal Mapping Control ===
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Tip: Use a single Value node to scale all textures simultaneously
    scale_val = nodes.new('ShaderNodeValue')
    scale_val.location = (-800, -200)
    scale_val.outputs[0].default_value = 2.0
    scale_val.label = "Universal Scale"
    links.new(scale_val.outputs[0], mapping.inputs['Scale'])
    
    # === Step 5: Base Color Pipeline ===
    color_tex = nodes.new('ShaderNodeTexNoise')
    color_tex.location = (-300, 300)
    color_tex.inputs['Scale'].default_value = 10.0
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 300)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (base_color[0], base_color[1], base_color[2], 1.0)
    links.new(color_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    
    # Tip: Hue/Saturation node for non-destructive color tweaking
    hsv_node = nodes.new('ShaderNodeHueSaturation')
    hsv_node.location = (200, 300)
    hsv_node.inputs['Saturation'].default_value = 0.85
    hsv_node.inputs['Value'].default_value = 0.5
    links.new(color_ramp.outputs['Color'], hsv_node.inputs['Color'])
    links.new(hsv_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # === Step 6: Gloss to Roughness Pipeline ===
    gloss_tex = nodes.new('ShaderNodeTexNoise')
    gloss_tex.location = (-300, 0)
    gloss_tex.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])
    
    # Tip: Invert node flips Gloss (white=smooth) to Roughness (black=smooth)
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    links.new(gloss_tex.outputs['Color'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # === Step 7: Specular/Reflection Pipeline ===
    spec_val = nodes.new('ShaderNodeValue')
    spec_val.location = (200, 100)
    spec_val.outputs['Value'].default_value = 0.25
    # Handle Blender 4.0+ BSDF node updates gracefully
    try:
        links.new(spec_val.outputs['Value'], bsdf_node.inputs['Specular IOR Level'])
    except KeyError:
        links.new(spec_val.outputs['Value'], bsdf_node.inputs['Specular'])
        
    # === Step 8: Normal/Bump Pipeline ===
    norm_tex = nodes.new('ShaderNodeTexNoise')
    norm_tex.location = (-300, -300)
    norm_tex.inputs['Scale'].default_value = 50.0
    links.new(mapping.outputs['Vector'], norm_tex.inputs['Vector'])
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -300)
    bump_node.inputs['Strength'].default_value = 0.6
    links.new(norm_tex.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # === Step 9: True Displacement Pipeline ===
    disp_tex = nodes.new('ShaderNodeTexNoise')
    disp_tex.location = (-300, -600)
    disp_tex.inputs['Scale'].default_value = 3.0
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (800, -300)
    # Tip: Set midlevel to 0.0 to prevent the entire object from shifting in 3D space
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.inputs['Scale'].default_value = 0.15
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    return f"Created '{object_name}' with complete PBR Displacement material pipeline."

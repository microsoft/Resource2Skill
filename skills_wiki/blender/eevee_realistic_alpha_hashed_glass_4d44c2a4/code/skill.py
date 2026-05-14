def create_object(
    scene_name: str = "Scene",
    object_name: str = "GlassMonkey",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create an Alpha-Hashed EEVEE Glass Object in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the glass in 0-1 range.
        **kwargs: Additional overrides (e.g., roughness, thickness).

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Configure EEVEE Render Settings ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_ssr = True
    scene.eevee.use_ssr_refraction = True
    
    # === Step 2: Create Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_monkey_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True
        
    # Add Subdivision Surface for smooth reflections
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    # Add Solidify for refractive thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = kwargs.get('thickness', 0.03)
    
    # === Step 3: Build Material & Shader Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_EEVEE_Glass")
    mat.use_nodes = True
    
    # Material-level EEVEE settings
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'HASHED'
    mat.use_screen_refraction = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Create Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (200, 0)
    
    transp_node = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node.location = (0, 100)
    
    princ_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    princ_node.location = (0, -100)
    
    ramp_node = nodes.new(type='ShaderNodeValToRGB')
    ramp_node.location = (0, 300)
    
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    fresnel_node.location = (-200, 300)
    
    # Configure Node Values
    fresnel_node.inputs[0].default_value = 1.45  # IOR
    
    # Adjust ColorRamp (Stop 0 to A7A7A7 for reduced transparency at facing angles)
    ramp_node.color_ramp.elements[0].position = 0.0
    ramp_node.color_ramp.elements[0].color = (0.395, 0.395, 0.395, 1.0)
    ramp_node.color_ramp.elements[1].position = 1.0
    ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Configure Principled BSDF (Safe across Blender versions)
    if 'Transmission Weight' in princ_node.inputs: # Blender 4.0+
        princ_node.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in princ_node.inputs: # Blender 3.x
        princ_node.inputs['Transmission'].default_value = 1.0
        
    if 'Roughness' in princ_node.inputs:
        princ_node.inputs['Roughness'].default_value = kwargs.get('roughness', 0.0)
        
    if 'Base Color' in princ_node.inputs:
        # Base Color dictates the glass tint
        color_rgba = (material_color[0], material_color[1], material_color[2], 1.0)
        princ_node.inputs['Base Color'].default_value = color_rgba
        
    # Link Nodes (Using index paths for deep backwards compatibility)
    links.new(fresnel_node.outputs[0], ramp_node.inputs[0])    # Fresnel Fac -> Ramp Fac
    links.new(ramp_node.outputs[0], mix_node.inputs[0])        # Ramp Color -> Mix Fac
    links.new(transp_node.outputs[0], mix_node.inputs[1])      # Transparent -> Mix Top
    links.new(princ_node.outputs[0], mix_node.inputs[2])       # Principled -> Mix Bottom
    links.new(mix_node.outputs[0], out_node.inputs[0])         # Mix Shader -> Material Output
    
    # === Step 4: Finalize ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    return f"Created '{object_name}' at {location} configured with an EEVEE Alpha-Hashed glass material."

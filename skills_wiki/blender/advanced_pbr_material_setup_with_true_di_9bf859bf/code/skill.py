def create_pbr_displacement_material_scene(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    base_color_dark: tuple = (0.1, 0.02, 0.01),
    base_color_light: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a complete PBR material setup with True Adaptive Displacement.
    Mimics the workflow of mapping Albedo, Gloss (Inverted), Normal, and Displacement maps.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color_dark: (R, G, B) dark tone for the procedural albedo.
        base_color_light: (R, G, B) light tone for the procedural albedo.

    Returns:
        Status string describing the created object and material.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Settings for True Displacement ===
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'
    
    # === Step 2: Create Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision modifier for adaptive displacement
    subdiv = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    # Enable adaptive subdivision (requires Cycles Experimental feature set)
    obj.cycles.use_adaptive_subdivision = True
    
    # === Step 3: Build PBR Material Node Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Crucial Setting: Tell the material to physically displace geometry
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Outputs
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 200)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Texture Coordinate & Universal Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Universal Scale Control (Value Node trick from video)
    val_scale = nodes.new('ShaderNodeValue')
    val_scale.location = (-800, -200)
    val_scale.outputs[0].default_value = 1.5
    links.new(val_scale.outputs[0], mapping.inputs['Scale'])
    
    # --- Albedo / Base Color Map Mockup ---
    tex_color = nodes.new('ShaderNodeTexNoise')
    tex_color.location = (-300, 400)
    tex_color.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 400)
    color_ramp.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    color_ramp.color_ramp.elements[1].color = (*base_color_light, 1.0)
    links.new(tex_color.outputs['Fac'], color_ramp.inputs['Fac'])
    
    # Hue Saturation adjustment node
    hsv = nodes.new('ShaderNodeHueSaturation')
    hsv.location = (200, 400)
    hsv.inputs['Saturation'].default_value = 0.9
    links.new(color_ramp.outputs['Color'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], bsdf.inputs['Base Color'])
    
    # --- Gloss to Roughness Mockup ---
    # In PBR, Roughness is Non-Color data. If we have a Gloss map, we invert it to get Roughness.
    tex_gloss = nodes.new('ShaderNodeTexNoise')
    tex_gloss.location = (-300, 100)
    tex_gloss.inputs['Scale'].default_value = 15.0
    tex_gloss.inputs['Detail'].default_value = 5.0
    links.new(mapping.outputs['Vector'], tex_gloss.inputs['Vector'])
    
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (-100, 100)
    links.new(tex_gloss.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])
    
    # --- Normal Map Mockup ---
    tex_normal_data = nodes.new('ShaderNodeTexVoronoi')
    tex_normal_data.location = (-300, -200)
    links.new(mapping.outputs['Vector'], tex_normal_data.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -200)
    bump.inputs['Strength'].default_value = 0.8
    links.new(tex_normal_data.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # --- True Displacement Map Mockup ---
    tex_disp = nodes.new('ShaderNodeTexNoise')
    tex_disp.location = (-300, -500)
    tex_disp.inputs['Scale'].default_value = 3.0
    tex_disp.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], tex_disp.inputs['Vector'])
    
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (800, -200)
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.2  # Keep scale relatively low for realistic displacement
    links.new(tex_disp.outputs['Fac'], disp.inputs['Height'])
    
    # Connect Displacement directly to Material Output
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])
    
    return f"Created PBR Object '{object_name}' with Adaptive Displacement material enabled."

def create_animated_water_with_caustics(
    scene_name: str = "Scene",
    object_name: str = "AnimatedWaterOrb",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.8, 1.0),
    **kwargs,
) -> str:
    """
    Create a procedural animated water sphere with fake caustics.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created sphere.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B, A) base color for the water.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, radius=1.0, location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    
    # Enable EEVEE screen space refractions in the scene (if using EEVEE)
    if hasattr(scene, "eevee"):
        scene.eevee.use_ssr = True
        scene.eevee.use_ssr_refraction = True
        
    # === Step 2: Build Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Material Settings for Glass/Water
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_screen_refraction = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # --- Nodes: Output & Mix Shader ---
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (1000, 0)
    mix_shader.inputs['Fac'].default_value = 0.935
    links.new(mix_shader.outputs[0], out_node.inputs['Surface'])
    
    # --- Nodes: Principled BSDF (Water Base) ---
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (700, -200)
    principled.inputs['Base Color'].default_value = material_color
    principled.inputs['Roughness'].default_value = 0.0
    principled.inputs['IOR'].default_value = 1.33
    
    # Handle version compatibility for Transmission
    if 'Transmission Weight' in principled.inputs:
        principled.inputs['Transmission Weight'].default_value = 1.0  # Blender 4.0+
    elif 'Transmission' in principled.inputs:
        principled.inputs['Transmission'].default_value = 1.0  # Blender < 4.0
        
    links.new(principled.outputs[0], mix_shader.inputs[2]) # Bottom socket
    
    # Transparency Falloff
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (500, 100)
    layer_weight.inputs['Blend'].default_value = 0.86
    links.new(layer_weight.outputs['Fresnel'], principled.inputs['Alpha'])
    
    # --- Nodes: Water Ripples (Bump) ---
    tc_water = nodes.new('ShaderNodeTexCoord')
    tc_water.location = (-600, -200)
    
    map_water = nodes.new('ShaderNodeMapping')
    map_water.location = (-400, -200)
    map_water.inputs['Scale'].default_value = (1.0, 1.5, 1.0)
    # Add driver to Y location for flowing wave animation
    loc_driver = map_water.inputs['Location'].driver_add("default_value", 1) 
    loc_driver.driver.expression = "frame / 1500"
    links.new(tc_water.outputs['Generated'], map_water.inputs['Vector'])
    
    noise_water = nodes.new('ShaderNodeTexNoise')
    noise_water.location = (-200, -200)
    noise_water.noise_dimensions = '4D'
    noise_water.inputs['Scale'].default_value = 5.6
    noise_water.inputs['Detail'].default_value = 3.2
    noise_water.inputs['Roughness'].default_value = 0.5
    # Add driver to W parameter for evolving wave shapes
    w_water_driver = noise_water.inputs['W'].driver_add("default_value")
    w_water_driver.driver.expression = "frame / 500"
    links.new(map_water.outputs['Vector'], noise_water.inputs['Vector'])
    
    bump_water = nodes.new('ShaderNodeBump')
    bump_water.location = (400, -400)
    bump_water.inputs['Strength'].default_value = 0.7
    links.new(noise_water.outputs['Fac'], bump_water.inputs['Height'])
    links.new(bump_water.outputs['Normal'], principled.inputs['Normal'])
    
    # --- Nodes: Fake Caustics ---
    tc_caustic = nodes.new('ShaderNodeTexCoord')
    tc_caustic.location = (-1000, 400)
    
    noise_distort = nodes.new('ShaderNodeTexNoise')
    noise_distort.location = (-1000, 200)
    noise_distort.inputs['Scale'].default_value = 10.3
    noise_distort.inputs['Detail'].default_value = 2.0
    
    # Version safe Mix node for coordinates
    try:
        mix_distort = nodes.new('ShaderNodeMix')
        mix_distort.data_type = 'RGBA'
        mix_distort.location = (-800, 400)
        mix_distort.inputs['Factor'].default_value = 0.07
        links.new(tc_caustic.outputs['Generated'], mix_distort.inputs['A'])
        links.new(noise_distort.outputs['Color'], mix_distort.inputs['B'])
    except Exception:
        mix_distort = nodes.new('ShaderNodeMixRGB')
        mix_distort.location = (-800, 400)
        mix_distort.inputs['Fac'].default_value = 0.07
        links.new(tc_caustic.outputs['Generated'], mix_distort.inputs['Color1'])
        links.new(noise_distort.outputs['Color'], mix_distort.inputs['Color2'])
        
    map_caustic = nodes.new('ShaderNodeMapping')
    map_caustic.location = (-600, 400)
    mix_out = mix_distort.outputs.get('Result') or mix_distort.outputs.get('Color')
    links.new(mix_out, map_caustic.inputs['Vector'])
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 400)
    voronoi.voronoi_dimensions = '4D'
    voronoi.feature = 'SMOOTH_F1'
    voronoi.inputs['Scale'].default_value = 8.7
    voronoi.inputs['Smoothness'].default_value = 0.05
    # Add driver to W parameter to animate caustics
    w_caustic_driver = voronoi.inputs['W'].driver_add("default_value")
    w_caustic_driver.driver.expression = "frame / 400"
    links.new(map_caustic.outputs['Vector'], voronoi.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-200, 400)
    ramp.color_ramp.elements[0].position = 0.17
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.255
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    
    math_min = nodes.new('ShaderNodeMath')
    math_min.operation = 'MINIMUM'
    math_min.location = (100, 400)
    math_min.inputs[1].default_value = 0.96
    links.new(ramp.outputs['Color'], math_min.inputs[0])
    
    math_log = nodes.new('ShaderNodeMath')
    math_log.operation = 'LOGARITHM'
    math_log.location = (300, 400)
    math_log.inputs[1].default_value = 0.85
    links.new(math_min.outputs['Value'], math_log.inputs[0])
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (500, 400)
    emission.inputs['Strength'].default_value = 7.4
    links.new(math_log.outputs['Value'], emission.inputs['Color'])
    
    links.new(emission.outputs['Emission'], mix_shader.inputs[1]) # Top socket
    
    # === Step 3: Material Assignment ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    return f"Created '{object_name}' at {location} with animated caustics (play timeline to see effect)."

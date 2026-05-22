def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralCarPaint",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.01, 0.2, 0.4), # Deep Teal
    **kwargs,
) -> str:
    """
    Create a procedural pearlescent car paint material with metallic flakes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created sphere.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary base color.
        **kwargs: 
            secondary_color: (R, G, B) color seen at grazing angles.
            flake_scale: Density of the metallic flakes (default 2500).

    Returns:
        Status string.
    """
    import bpy

    # Extract kwargs
    secondary_color = kwargs.get("secondary_color", (0.3, 0.02, 0.5)) # Purple
    flake_scale = kwargs.get("flake_scale", 2500.0)
    flake_color_intensity = kwargs.get("flake_color_intensity", 0.75)
    flake_bump_strength = kwargs.get("flake_bump_strength", 0.075)
    orange_peel_strength = kwargs.get("orange_peel_strength", 0.015)

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    # Add Subdivision for smooth clearcoat reflections
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Configure Principled BSDF
    bsdf.inputs['Metallic'].default_value = 1.0
    
    # API Compatibility: Blender 4.0 renamed 'Clearcoat' to 'Coat Weight'
    coat_weight = bsdf.inputs.get('Coat Weight') or bsdf.inputs.get('Clearcoat')
    if coat_weight: 
        coat_weight.default_value = 1.0
    
    coat_rough = bsdf.inputs.get('Coat Roughness') or bsdf.inputs.get('Clearcoat Roughness')
    if coat_rough: 
        coat_rough.default_value = 0.05
    
    coat_normal = bsdf.inputs.get('Coat Normal') or bsdf.inputs.get('Clearcoat Normal')
    
    # Generate Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-800, 300)
    layer_weight.inputs['Blend'].default_value = 0.4
    
    # Robust node creation for Color Mixing (handles Blender 3.x and 4.x API changes)
    try:
        # Blender 3.4+ syntax
        base_mix = nodes.new('ShaderNodeMix')
        base_mix.data_type = 'RGBA'
        base_mix.inputs[6].default_value = (*material_color, 1.0)
        base_mix.inputs[7].default_value = (*secondary_color, 1.0)
        links.new(layer_weight.outputs['Facing'], base_mix.inputs[0])
        base_color_out = base_mix.outputs[2]
        
        flake_mix = nodes.new('ShaderNodeMix')
        flake_mix.data_type = 'RGBA'
        flake_mix.blend_type = 'DIVIDE'
        flake_mix.inputs[0].default_value = flake_color_intensity
        links.new(base_color_out, flake_mix.inputs[6])
        flake_color_in = flake_mix.inputs[7]
        flake_color_out = flake_mix.outputs[2]
    except Exception:
        # Fallback for Blender < 3.4
        base_mix = nodes.new('ShaderNodeMixRGB')
        base_mix.inputs[1].default_value = (*material_color, 1.0)
        base_mix.inputs[2].default_value = (*secondary_color, 1.0)
        links.new(layer_weight.outputs['Facing'], base_mix.inputs['Fac'])
        base_color_out = base_mix.outputs['Color']
        
        flake_mix = nodes.new('ShaderNodeMixRGB')
        flake_mix.blend_type = 'DIVIDE'
        flake_mix.inputs['Fac'].default_value = flake_color_intensity
        links.new(base_color_out, flake_mix.inputs[1])
        flake_color_in = flake_mix.inputs[2]
        flake_color_out = flake_mix.outputs['Color']
        
    base_mix.location = (-500, 300)
    flake_mix.location = (-200, 100)
    links.new(flake_color_out, bsdf.inputs['Base Color'])
    
    # Flakes Generator (Voronoi)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-1000, -200)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, -200)
    voronoi.inputs['Scale'].default_value = flake_scale
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(voronoi.outputs['Color'], flake_color_in)
    
    # Flake Roughness Variation
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (-200, -100)
    map_range.inputs['From Min'].default_value = 0.0
    map_range.inputs['From Max'].default_value = 1.0
    map_range.inputs['To Min'].default_value = 0.4
    map_range.inputs['To Max'].default_value = 0.15
    links.new(voronoi.outputs['Color'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
    
    # Flake Normal Faceting
    # Using Object Space makes the voronoi RGB values act directly as tilted surface normals
    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.space = 'OBJECT'
    normal_map.location = (-200, -400)
    normal_map.inputs['Strength'].default_value = flake_bump_strength
    links.new(voronoi.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Clearcoat Orange Peel Imperfections
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, -700)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 10.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (100, -700)
    bump.inputs['Strength'].default_value = orange_peel_strength
    bump.inputs['Distance'].default_value = 0.1
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    
    # Link Orange Peel to Clearcoat
    if coat_normal:
        links.new(bump.outputs['Normal'], coat_normal)
        
    return f"Created '{object_name}' at {location} with procedural car paint shader applied."

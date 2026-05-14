def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralMat",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.6, 0.1), # Default color for the plastic toy
    **kwargs,
) -> str:
    """
    Creates three spheres side-by-side to showcase procedural Wood, Plastic, and Snow materials.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space center position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the plastic material.
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Helper function to create a smooth sphere with subdivision
    def create_display_sphere(name, loc):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        bpy.ops.object.shade_smooth()
        
        # Add Subsurf for high-quality displacement
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 3
        subsurf.render_levels = 3
        return obj

    center_loc = Vector(location)
    
    # ==========================================
    # 1. PROCEDURAL WOOD (Left)
    # ==========================================
    wood_obj = create_display_sphere(f"{object_name}_Wood", center_loc + Vector((-2.5 * scale, 0, 0)))
    wood_obj.scale = (scale, scale, scale)
    wood_mat = bpy.data.materials.new(name=f"{object_name}_Wood_Mat")
    wood_mat.use_nodes = True
    wood_obj.data.materials.append(wood_mat)
    
    nodes = wood_mat.node_tree.nodes
    links = wood_mat.node_tree.links
    nodes.clear()
    
    out_wood = nodes.new('ShaderNodeOutputMaterial')
    bsdf_wood = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(bsdf_wood.outputs[0], out_wood.inputs[0])
    
    # Stretch noise using mapping node
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (1.0, 5.0, 1.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    noise_wood = nodes.new('ShaderNodeTexNoise')
    noise_wood.inputs['Scale'].default_value = 3.0
    noise_wood.inputs['Detail'].default_value = 15.0
    noise_wood.inputs['Roughness'].default_value = 0.65
    noise_wood.inputs['Distortion'].default_value = 1.0
    links.new(mapping.outputs['Vector'], noise_wood.inputs['Vector'])
    
    # Base Color
    wood_color_ramp = nodes.new('ShaderNodeValToRGB')
    wood_color_ramp.color_ramp.elements[0].position = 0.4
    wood_color_ramp.color_ramp.elements[0].color = (0.1, 0.05, 0.02, 1.0)
    wood_color_ramp.color_ramp.elements[1].position = 0.6
    wood_color_ramp.color_ramp.elements[1].color = (0.4, 0.25, 0.1, 1.0)
    links.new(noise_wood.outputs['Fac'], wood_color_ramp.inputs['Fac'])
    links.new(wood_color_ramp.outputs['Color'], bsdf_wood.inputs['Base Color'])
    
    # Roughness (Driven by base color)
    wood_rough_ramp = nodes.new('ShaderNodeValToRGB')
    wood_rough_ramp.color_ramp.elements[0].position = 0.1
    wood_rough_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    wood_rough_ramp.color_ramp.elements[1].position = 0.6
    wood_rough_ramp.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1.0)
    links.new(wood_color_ramp.outputs['Color'], wood_rough_ramp.inputs['Fac'])
    links.new(wood_rough_ramp.outputs['Color'], bsdf_wood.inputs['Roughness'])
    
    # Bump
    bump_wood = nodes.new('ShaderNodeBump')
    bump_wood.inputs['Distance'].default_value = 0.1
    links.new(noise_wood.outputs['Fac'], bump_wood.inputs['Height'])
    links.new(bump_wood.outputs['Normal'], bsdf_wood.inputs['Normal'])

    # ==========================================
    # 2. PROCEDURAL PLASTIC WITH DIRT (Center)
    # ==========================================
    plastic_obj = create_display_sphere(f"{object_name}_Plastic", center_loc)
    plastic_obj.scale = (scale, scale, scale)
    plastic_mat = bpy.data.materials.new(name=f"{object_name}_Plastic_Mat")
    plastic_mat.use_nodes = True
    plastic_obj.data.materials.append(plastic_mat)
    
    nodes = plastic_mat.node_tree.nodes
    links = plastic_mat.node_tree.links
    nodes.clear()
    
    out_plastic = nodes.new('ShaderNodeOutputMaterial')
    mix_shader = nodes.new('ShaderNodeMixShader')
    links.new(mix_shader.outputs[0], out_plastic.inputs[0])
    
    # Clean and Dirty BSDFs
    clean_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    clean_bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    clean_bsdf.inputs['Roughness'].default_value = 0.3
    links.new(clean_bsdf.outputs[0], mix_shader.inputs[1])
    
    dirty_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    dirty_bsdf.inputs['Base Color'].default_value = (0.05, 0.04, 0.03, 1.0)
    dirty_bsdf.inputs['Roughness'].default_value = 0.8
    links.new(dirty_bsdf.outputs[0], mix_shader.inputs[2])
    
    # Micro bump detail shared by both
    micro_noise = nodes.new('ShaderNodeTexNoise')
    micro_noise.inputs['Scale'].default_value = 500.0
    micro_noise.inputs['Detail'].default_value = 2.0
    
    bump_plastic = nodes.new('ShaderNodeBump')
    bump_plastic.inputs['Distance'].default_value = 0.02
    bump_plastic.inputs['Strength'].default_value = 0.3
    links.new(micro_noise.outputs['Fac'], bump_plastic.inputs['Height'])
    links.new(bump_plastic.outputs['Normal'], clean_bsdf.inputs['Normal'])
    links.new(bump_plastic.outputs['Normal'], dirty_bsdf.inputs['Normal'])
    
    # Procedural Dirt Mask
    dirt_coord = nodes.new('ShaderNodeTexCoord')
    dirt_noise = nodes.new('ShaderNodeTexNoise')
    dirt_noise.inputs['Scale'].default_value = 15.0
    dirt_noise.inputs['Detail'].default_value = 15.0
    dirt_noise.inputs['Roughness'].default_value = 0.6
    links.new(dirt_coord.outputs['Object'], dirt_noise.inputs['Vector'])
    
    dirt_ramp = nodes.new('ShaderNodeValToRGB')
    dirt_ramp.color_ramp.elements[0].position = 0.4
    dirt_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    dirt_ramp.color_ramp.elements[1].position = 0.6
    dirt_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(dirt_noise.outputs['Fac'], dirt_ramp.inputs['Fac'])
    links.new(dirt_ramp.outputs['Color'], mix_shader.inputs['Fac'])

    # ==========================================
    # 3. PROCEDURAL SNOW (Right)
    # ==========================================
    snow_obj = create_display_sphere(f"{object_name}_Snow", center_loc + Vector((2.5 * scale, 0, 0)))
    snow_obj.scale = (scale, scale, scale)
    snow_mat = bpy.data.materials.new(name=f"{object_name}_Snow_Mat")
    snow_mat.use_nodes = True
    snow_mat.cycles.displacement_method = 'BOTH' # Enable true displacement
    snow_obj.data.materials.append(snow_mat)
    
    nodes = snow_mat.node_tree.nodes
    links = snow_mat.node_tree.links
    nodes.clear()
    
    out_snow = nodes.new('ShaderNodeOutputMaterial')
    bsdf_snow = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(bsdf_snow.outputs[0], out_snow.inputs[0])
    
    # Subsurface scattering properties (handles multiple Blender version APIs safely)
    if bsdf_snow.inputs.get("Subsurface Weight"):
        bsdf_snow.inputs["Subsurface Weight"].default_value = 0.5
        bsdf_snow.inputs["Subsurface Radius"].default_value = (1.0, 1.0, 1.0)
    elif bsdf_snow.inputs.get("Subsurface"):
        bsdf_snow.inputs["Subsurface"].default_value = 0.5
        bsdf_snow.inputs["Subsurface Radius"].default_value = (1.0, 1.0, 1.0)

    bsdf_snow.inputs['Roughness'].default_value = 0.2
    
    # Voronoi base color mixing
    snow_mix = nodes.new('ShaderNodeMixRGB')
    snow_mix.inputs[1].default_value = (0.85, 0.9, 1.0, 1.0) # Light icy blue
    snow_mix.inputs[2].default_value = (1.0, 1.0, 1.0, 1.0)  # Pure white
    
    voronoi_snow = nodes.new('ShaderNodeTexVoronoi')
    voronoi_snow.inputs['Scale'].default_value = 80.0
    links.new(voronoi_snow.outputs['Distance'], snow_mix.inputs['Fac'])
    links.new(snow_mix.outputs['Color'], bsdf_snow.inputs['Base Color'])
    
    # Normal Chaining (Sparkles -> Large bumps)
    bump_sparkles = nodes.new('ShaderNodeBump')
    bump_sparkles.inputs['Strength'].default_value = 0.3
    bump_sparkles.inputs['Distance'].default_value = 0.05
    links.new(voronoi_snow.outputs['Distance'], bump_sparkles.inputs['Height'])
    
    noise_large = nodes.new('ShaderNodeTexNoise')
    noise_large.inputs['Scale'].default_value = 6.0
    noise_large.inputs['Detail'].default_value = 15.0
    
    bump_large = nodes.new('ShaderNodeBump')
    bump_large.inputs['Strength'].default_value = 0.5
    bump_large.inputs['Distance'].default_value = 0.2
    links.new(noise_large.outputs['Fac'], bump_large.inputs['Height'])
    
    # Chain them together
    links.new(bump_sparkles.outputs['Normal'], bump_large.inputs['Normal'])
    links.new(bump_large.outputs['Normal'], bsdf_snow.inputs['Normal'])
    
    # True Displacement
    disp_noise = nodes.new('ShaderNodeTexNoise')
    disp_noise.inputs['Scale'].default_value = 10.0
    disp_noise.inputs['Detail'].default_value = 15.0
    
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.inputs['Scale'].default_value = 0.1
    links.new(disp_noise.outputs['Fac'], displacement.inputs['Height'])
    links.new(displacement.outputs['Displacement'], out_snow.inputs['Displacement'])
    
    return f"Created three material display spheres (Wood, Plastic, Snow) centered at {location}"

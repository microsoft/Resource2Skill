def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicNight",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused, overriding with specific environment colors
    **kwargs,
) -> str:
    """
    Create a Cinematic Night Environment setup in the active Blender scene.
    Generates a volumetric fog box, moon/practical lights, and a procedural starry sky.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created environment objects.
        location: (x, y, z) world-space base position for the rig.
        scale: Uniform scale factor for the environment size.
        material_color: Ignored (handles strict lighting/volumetric colors).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created environment.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create the Fog Volume Box ===
    bpy.ops.mesh.primitive_cube_add(size=1)
    fog_obj = bpy.context.active_object
    fog_obj.name = f"{object_name}_FogVolume"
    # Scale box to encompass a large scene area
    fog_obj.scale = (100 * scale, 100 * scale, 30 * scale)
    fog_obj.location = Vector(location) + Vector((0, 0, 15 * scale))
    
    # Hide from selection so it doesn't get in the user's way
    fog_obj.hide_select = True 

    # Create Volumetric Material
    mat = bpy.data.materials.new(name=f"{object_name}_Fog_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Principled Volume Setup
    vol_node = nodes.new(type="ShaderNodeVolumePrincipled")
    vol_node.location = (0, 0)
    vol_node.inputs['Density'].default_value = 0.02
    vol_node.inputs['Anisotropy'].default_value = 0.7
    
    # Handle Blender version differences for Emission
    if 'Emission Color' in vol_node.inputs: # Pre-4.0
        vol_node.inputs['Emission Color'].default_value = (0.005, 0.015, 0.04, 1.0) # Dark blue tint
    elif 'Emission' in vol_node.inputs: # Blender 4.0+
        vol_node.inputs['Emission'].default_value = (0.005, 0.015, 0.04, 1.0)
        if 'Emission Strength' in vol_node.inputs:
            vol_node.inputs['Emission Strength'].default_value = 0.5

    out_node = nodes.new(type="ShaderNodeOutputMaterial")
    out_node.location = (300, 0)
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    
    fog_obj.data.materials.append(mat)

    # === Step 2: Create Lighting Setup ===
    
    # 2a. Moonlight (High Energy, Cyan/Blue)
    moon_data = bpy.data.lights.new(name=f"{object_name}_MoonLight", type='POINT')
    moon_data.energy = 10000 * (scale ** 2) # Maintain relative brightness if scaled
    moon_data.color = (0.65, 0.93, 1.0) # Hex #A8EEFF equiv
    moon_data.shadow_soft_size = 5.0 # Soft shadows from atmospheric scatter
    
    moon_obj = bpy.data.objects.new(name=f"{object_name}_MoonLight", object_data=moon_data)
    scene.collection.objects.link(moon_obj)
    # Place high up and slightly offset
    moon_obj.location = Vector(location) + Vector((-20 * scale, 15 * scale, 25 * scale))

    # 2b. Practical Light (Low Energy, Warm Orange for contrast)
    prac_data = bpy.data.lights.new(name=f"{object_name}_PracticalLight", type='POINT')
    prac_data.energy = 200 * (scale ** 2)
    prac_data.color = (1.0, 0.5, 0.15) # Warm Tungsten
    
    prac_obj = bpy.data.objects.new(name=f"{object_name}_PracticalLight", object_data=prac_data)
    scene.collection.objects.link(prac_obj)
    # Place near ground level
    prac_obj.location = Vector(location) + Vector((2 * scale, -2 * scale, 1.5 * scale))

    # === Step 3: Procedural Starry Night World Shader ===
    
    # Create new world to be safely additive (preserves user's old world)
    world = bpy.data.worlds.new(name=f"{object_name}_StarrySky")
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    wnodes.clear()

    w_out = wnodes.new("ShaderNodeOutputWorld")
    w_out.location = (600, 0)

    # Mix Shader
    mix_node = wnodes.new("ShaderNodeMixShader")
    mix_node.location = (400, 0)
    wlinks.new(mix_node.outputs[0], w_out.inputs['Surface'])

    # Sky Base (Nishita)
    sky_bg = wnodes.new("ShaderNodeBackground")
    sky_bg.location = (200, -150)
    sky_bg.inputs['Strength'].default_value = 0.05
    wlinks.new(sky_bg.outputs['Background'], mix_node.inputs[1])

    sky_tex = wnodes.new("ShaderNodeTexSky")
    sky_tex.location = (0, -150)
    sky_tex.sky_type = 'NISHITA'
    sky_tex.sun_elevation = 0.0
    sky_tex.altitude = 40000.0
    wlinks.new(sky_tex.outputs['Color'], sky_bg.inputs['Color'])

    # Star Emissive Layer
    star_bg = wnodes.new("ShaderNodeBackground")
    star_bg.location = (200, 150)
    star_bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    star_bg.inputs['Strength'].default_value = 10.0
    wlinks.new(star_bg.outputs['Background'], mix_node.inputs[2])

    # Star Generator (Noise + ColorRamp)
    noise_node = wnodes.new("ShaderNodeTexNoise")
    noise_node.location = (-300, 250)
    noise_node.inputs['Scale'].default_value = 1000.0
    noise_node.inputs['Detail'].default_value = 0.0
    noise_node.inputs['Roughness'].default_value = 0.5

    ramp_node = wnodes.new("ShaderNodeValToRGB")
    ramp_node.location = (-100, 250)
    ramp_node.color_ramp.elements[0].position = 0.88 # Clamp to create small specs
    ramp_node.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp_node.color_ramp.elements[1].position = 0.98
    ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    wlinks.new(noise_node.outputs['Fac'], ramp_node.inputs['Fac'])
    wlinks.new(ramp_node.outputs['Color'], mix_node.inputs['Fac']) # Use dots as mix factor

    # Assign World to Scene
    scene.world = world

    return f"Created Cinematic Night Environment '{object_name}': Volumetric Fog, 2 Lights, and Procedural World Sky applied to {scene.name}."

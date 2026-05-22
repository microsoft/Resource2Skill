def create_object(
    scene_name: str = "Scene",
    object_name: str = "DynamicLightingRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.4, 0.8),
    **kwargs,
) -> str:
    """
    Create Dynamic Dual-Sky Lighting with Glossy Override in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the generated Light Probe anchor.
        location: (x, y, z) world-space position for the reflection probe.
        scale: Uniform scale factor for the reflection probe.
        material_color: (R, G, B) custom tint applied strictly to glossy reflections.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create World Lighting Setup ===
    world = bpy.data.worlds.new(name=f"{object_name}_World")
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    # Sky 1 (Large sun for soft, dispersed shadows)
    sky1 = nodes.new("ShaderNodeTexSky")
    sky1.sky_type = 'NISHITA'
    sky1.sun_rotation = math.radians(30.0)
    sky1.sun_size = math.radians(5.0)
    sky1.sun_intensity = 0.5
    sky1.location = (-600, 200)

    # Sky 2 (Small sun, slightly offset, for sharp core shadows)
    sky2 = nodes.new("ShaderNodeTexSky")
    sky2.sky_type = 'NISHITA'
    sky2.sun_rotation = math.radians(32.0)
    sky2.sun_size = math.radians(1.0)
    sky2.sun_intensity = 0.5
    sky2.location = (-600, -100)

    # Blackbody for thermal color temperature (Warm Daylight)
    blackbody = nodes.new("ShaderNodeBlackbody")
    blackbody.inputs['Temperature'].default_value = 5500.0
    blackbody.location = (-400, -300)

    # Handle Mix node API differences between Blender versions (<3.4 vs >=3.4)
    is_legacy = bpy.app.version < (3, 4, 0)
    
    if not is_legacy:
        mix_skies = nodes.new("ShaderNodeMix")
        mix_skies.data_type = 'RGBA'
        mix_skies.blend_type = 'MIX'
        in_a1, in_b1 = mix_skies.inputs['A'], mix_skies.inputs['B']
        out1 = mix_skies.outputs['Result']
        
        mix_temp = nodes.new("ShaderNodeMix")
        mix_temp.data_type = 'RGBA'
        mix_temp.blend_type = 'MIX'
        in_a2, in_b2 = mix_temp.inputs['A'], mix_temp.inputs['B']
        out2 = mix_temp.outputs['Result']
    else:
        mix_skies = nodes.new("ShaderNodeMixRGB")
        mix_skies.blend_type = 'MIX'
        in_a1, in_b1 = mix_skies.inputs['Color1'], mix_skies.inputs['Color2']
        out1 = mix_skies.outputs['Color']
        
        mix_temp = nodes.new("ShaderNodeMixRGB")
        mix_temp.blend_type = 'MIX'
        in_a2, in_b2 = mix_temp.inputs['Color1'], mix_temp.inputs['Color2']
        out2 = mix_temp.outputs['Color']

    mix_skies.inputs['Factor'].default_value = 0.5
    mix_skies.location = (-400, 100)
    
    mix_temp.inputs['Factor'].default_value = 0.5
    mix_temp.location = (-200, 0)

    # Blend the two offset skies together
    links.new(sky1.outputs['Color'], in_a1)
    links.new(sky2.outputs['Color'], in_b1)

    # Mix the combined skies with the Blackbody temperature node
    links.new(out1, in_a2)
    links.new(blackbody.outputs['Color'], in_b2)

    # Backgrounds
    bg_main = nodes.new("ShaderNodeBackground")
    bg_main.location = (0, 100)
    links.new(out2, bg_main.inputs['Color'])

    bg_glossy = nodes.new("ShaderNodeBackground")
    bg_glossy.inputs['Color'].default_value = (*material_color, 1.0)
    bg_glossy.location = (0, -100)

    # Light Path & Mix Shader for Glossy Override
    light_path = nodes.new("ShaderNodeLightPath")
    light_path.location = (0, 300)

    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (200, 0)

    # 'Is Glossy Ray' dictates that reflections see bg_glossy, while everything else sees bg_main
    links.new(light_path.outputs['Is Glossy Ray'], mix_shader.inputs['Fac'])
    links.new(bg_main.outputs['Background'], mix_shader.inputs[1])
    links.new(bg_glossy.outputs['Background'], mix_shader.inputs[2])

    world_out = nodes.new("ShaderNodeOutputWorld")
    world_out.location = (400, 0)
    links.new(mix_shader.outputs['Shader'], world_out.inputs['Surface'])

    # Apply the newly created dynamic lighting setup to the current scene
    scene.world = world

    # === Step 2: Create Spatial Anchor (Light Probe) ===
    # Because World lighting is global, we add a Reflection Cubemap at the requested location.
    # This captures the new glossy environment for the specific area, giving the skill a physical manifestation.
    bpy.ops.object.lightprobe_add(type='CUBEMAP', location=location)
    probe_obj = bpy.context.active_object
    probe_obj.name = object_name
    probe_obj.scale = (scale, scale, scale)

    return f"Created World '{world.name}' and Reflection Probe '{probe_obj.name}' at {location}"

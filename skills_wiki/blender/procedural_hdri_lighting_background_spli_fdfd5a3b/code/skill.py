def create_advanced_environment_lighting(
    scene_name: str = "Scene",
    rotation_z_degrees: float = 45.0,
    lighting_gamma: float = 0.8,
    lighting_saturation: float = 0.6,
    lighting_strength: float = 1.0,
    visible_bg_strength: float = 1.0,
) -> str:
    """
    Create an advanced World Shader that decouples the visible background 
    from the lighting rays, allowing independent control over contrast (shadow softness) 
    and color cast.

    Args:
        scene_name: Name of the target scene.
        rotation_z_degrees: Rotates the environment lighting and background.
        lighting_gamma: <1.0 for soft overcast shadows, >1.0 for punchy harsh shadows.
        lighting_saturation: <1.0 to remove unwanted ambient color cast from the scene.
        lighting_strength: Intensity of the light cast into the scene.
        visible_bg_strength: Brightness of the background visible to the camera.

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Create a new world to ensure the operation is purely additive
    world_name = "Advanced_Lighting_Splitter"
    world = bpy.data.worlds.new(name=world_name)
    world.use_nodes = True
    scene.world = world
    
    tree = world.node_tree
    links = tree.links
    
    # Clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
        
    # === Step 1: Create Nodes ===
    output = tree.nodes.new(type='ShaderNodeOutputWorld')
    output.location = (1000, 0)
    
    mix_shader = tree.nodes.new(type='ShaderNodeMixShader')
    mix_shader.location = (800, 0)
    
    light_path = tree.nodes.new(type='ShaderNodeLightPath')
    light_path.location = (500, 300)
    
    bg_light = tree.nodes.new(type='ShaderNodeBackground')
    bg_light.name = "Background_Lighting"
    bg_light.label = "Lighting Rays"
    bg_light.inputs['Strength'].default_value = lighting_strength
    bg_light.location = (500, 0)
    
    bg_visible = tree.nodes.new(type='ShaderNodeBackground')
    bg_visible.name = "Background_Visible"
    bg_visible.label = "Visible Background"
    bg_visible.inputs['Strength'].default_value = visible_bg_strength
    bg_visible.location = (500, -200)
    
    hsv = tree.nodes.new(type='ShaderNodeHueSaturation')
    hsv.inputs['Saturation'].default_value = lighting_saturation
    hsv.location = (300, 0)
    
    gamma = tree.nodes.new(type='ShaderNodeGamma')
    gamma.inputs['Gamma'].default_value = lighting_gamma
    gamma.location = (100, 0)
    
    # Using procedural Sky Texture for zero-dependency reproduction. 
    # (Users can swap this node for an Environment Texture EXR/HDR later)
    env_tex = tree.nodes.new(type='ShaderNodeTexSky')
    env_tex.sky_type = 'NISHITA'
    env_tex.location = (-200, -100)
    
    mapping = tree.nodes.new(type='ShaderNodeMapping')
    mapping.inputs['Rotation'].default_value[2] = math.radians(rotation_z_degrees)
    mapping.location = (-400, -100)
    
    tex_coord = tree.nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, -100)
    
    # === Step 2: Link Nodes ===
    
    # Coordinate mapping
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
    
    # Lighting Path (Modified by Gamma and HSV)
    links.new(env_tex.outputs['Color'], gamma.inputs['Color'])
    links.new(gamma.outputs['Color'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], bg_light.inputs['Color'])
    
    # Visible Path (Unmodified)
    links.new(env_tex.outputs['Color'], bg_visible.inputs['Color'])
    
    # Splitter Logic: Fac=0 (Diffuse/Lighting) uses Socket 1. Fac=1 (Camera) uses Socket 2.
    links.new(light_path.outputs['Is Camera Ray'], mix_shader.inputs['Fac'])
    links.new(bg_light.outputs['Background'], mix_shader.inputs[1])
    links.new(bg_visible.outputs['Background'], mix_shader.inputs[2])
    
    # Final Output
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    
    return f"Created and assigned Advanced Environment Lighting World '{world.name}'"

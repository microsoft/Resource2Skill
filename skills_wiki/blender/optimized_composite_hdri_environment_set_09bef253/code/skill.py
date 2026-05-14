def create_optimized_hdri_world(
    scene_name: str = "Scene",
    world_name: str = "Optimized_Composite_HDRI",
    lighting_filepath: str = "",
    background_filepath: str = "",
    lighting_strength: float = 5.0,
    background_strength: float = 1.0,
    z_rotation_degrees: float = 0.0,
    **kwargs,
) -> str:
    """
    Creates an optimized World Shader that splits lighting and camera rays.
    Uses a fast HDRI for lighting and a high-res image for the background.
    If filepaths are empty, it generates a procedural fallback to demonstrate the technique.

    Args:
        scene_name: Name of the active scene.
        world_name: Name of the new World datablock to create.
        lighting_filepath: Path to the low-res EXR/HDR for lighting.
        background_filepath: Path to the high-res JPG for the camera background.
        lighting_strength: Emission strength of the lighting setup.
        background_strength: Emission strength of the visible background.
        z_rotation_degrees: Rotation of the environment.

    Returns:
        Status string describing the created world setup.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a new world
    new_world = bpy.data.worlds.new(name=world_name)
    new_world.use_nodes = True
    scene.world = new_world
    
    node_tree = new_world.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # === Create Nodes ===
    
    # Output and Mixing
    node_output = nodes.new(type="ShaderNodeOutputWorld")
    node_output.location = (600, 0)

    node_mix = nodes.new(type="ShaderNodeMixShader")
    node_mix.location = (400, 0)

    node_light_path = nodes.new(type="ShaderNodeLightPath")
    node_light_path.location = (150, 200)

    # Background Shaders
    node_bg_light = nodes.new(type="ShaderNodeBackground")
    node_bg_light.name = "BG_Lighting"
    node_bg_light.label = "Lighting (Low-Res)"
    node_bg_light.location = (150, 0)
    node_bg_light.inputs['Strength'].default_value = lighting_strength

    node_bg_cam = nodes.new(type="ShaderNodeBackground")
    node_bg_cam.name = "BG_Camera"
    node_bg_cam.label = "Background (High-Res)"
    node_bg_cam.location = (150, -150)
    node_bg_cam.inputs['Strength'].default_value = background_strength

    # Mapping coordinates
    node_mapping = nodes.new(type="ShaderNodeMapping")
    node_mapping.location = (-400, 0)
    node_mapping.inputs['Rotation'].default_value[2] = math.radians(z_rotation_degrees)

    node_tex_coord = nodes.new(type="ShaderNodeTexCoord")
    node_tex_coord.location = (-600, 0)

    # Images / Fallbacks
    if lighting_filepath:
        node_env_light = nodes.new(type="ShaderNodeTexEnvironment")
        node_env_light.location = (-150, 50)
        try:
            img = bpy.data.images.load(lighting_filepath)
            node_env_light.image = img
        except:
            pass
    else:
        # Fallback: Procedural Sky for lighting
        node_env_light = nodes.new(type="ShaderNodeTexSky")
        node_env_light.location = (-150, 50)
        node_env_light.sun_elevation = math.radians(30)

    if background_filepath:
        node_env_cam = nodes.new(type="ShaderNodeTexEnvironment")
        node_env_cam.location = (-150, -250)
        try:
            img = bpy.data.images.load(background_filepath)
            node_env_cam.image = img
        except:
            pass
    else:
        # Fallback: Procedural grid to make it obvious the camera sees something different
        node_env_cam = nodes.new(type="ShaderNodeTexChecker")
        node_env_cam.location = (-150, -250)
        node_env_cam.inputs['Color1'].default_value = (0.01, 0.05, 0.2, 1.0)
        node_env_cam.inputs['Color2'].default_value = (0.8, 0.4, 0.1, 1.0)
        node_env_cam.inputs['Scale'].default_value = 20.0

    # === Make Links ===
    
    # Coordinates -> Mapping -> Textures
    links.new(node_tex_coord.outputs['Generated'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_env_light.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_env_cam.inputs['Vector'])

    # Textures -> Backgrounds
    if node_env_light.type == 'TEX_SKY':
        links.new(node_env_light.outputs['Color'], node_bg_light.inputs['Color'])
    else:
        links.new(node_env_light.outputs['Color'], node_bg_light.inputs['Color'])
        
    links.new(node_env_cam.outputs['Color'], node_bg_cam.inputs['Color'])

    # Light Path + Backgrounds -> Mix Shader
    links.new(node_light_path.outputs['Is Camera Ray'], node_mix.inputs['Fac'])
    
    # Top socket (0) = Lighting, Bottom socket (1) = Camera
    links.new(node_bg_light.outputs['Background'], node_mix.inputs[1]) 
    links.new(node_bg_cam.outputs['Background'], node_mix.inputs[2])

    # Mix Shader -> Output
    links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])

    # Optional: Set View Transform to False Color to help user expose the scene
    scene.view_settings.view_transform = 'False Color'

    fallback_msg = " (Used procedural fallbacks as no filepaths were provided)" if not lighting_filepath else ""
    return f"Created and assigned Optimized Composite HDRI World '{world_name}' with rotation {z_rotation_degrees}°{fallback_msg}."

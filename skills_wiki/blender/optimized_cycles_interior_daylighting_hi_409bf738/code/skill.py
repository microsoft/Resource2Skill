def setup_interior_daylight(
    scene_name: str = "Scene",
    world_name: str = "Archviz_Daylight_World",
    sun_elevation_deg: float = 25.0,
    sun_rotation_deg: float = 135.0,
    sun_intensity: float = 1.0,
    diffuse_bounces: int = 12,
    transparent_bounces: int = 18,
    **kwargs
) -> str:
    """
    Configures Cycles render settings for deep interior light bouncing and 
    sets up a procedural daylight environment.

    Args:
        scene_name: Name of the target scene.
        world_name: Name for the generated World data block.
        sun_elevation_deg: Height of the sun (lower = warmer/sunset, higher = cooler/noon).
        sun_rotation_deg: Compass direction of the sun.
        sun_intensity: Overall brightness of the sky/sun.
        diffuse_bounces: High value (12+) allows light to bounce deep into rooms.
        transparent_bounces: High value (18+) prevents glass windows from rendering black.

    Returns:
        Status string confirming rendering and lighting configuration.
    """
    import bpy
    import math

    # 1. Get the target scene
    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene

    # 2. Force Cycles Render Engine (required for complex path tracing)
    scene.render.engine = 'CYCLES'
    
    # Optional: Set GPU compute if available, otherwise fallback to CPU
    try:
        scene.cycles.device = 'GPU'
    except Exception:
        scene.cycles.device = 'CPU'

    # 3. Configure crucial Light Path bounces for interiors
    # Ensure total max bounces is at least as high as our highest specific bounce requirement
    required_max = max(diffuse_bounces, transparent_bounces, scene.cycles.max_bounces)
    scene.cycles.max_bounces = required_max
    
    # Apply the specific bounce optimizations from the tutorial
    scene.cycles.diffuse_bounces = diffuse_bounces
    scene.cycles.transparent_max_bounces = transparent_bounces

    # 4. Set up the World Shader for Environmental Daylighting
    # Create non-destructively: get existing by name or create new
    world = bpy.data.worlds.get(world_name)
    if not world:
        world = bpy.data.worlds.new(name=world_name)
    
    scene.world = world
    world.use_nodes = True
    
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links
    
    # Clear existing nodes in this specific world material
    nodes.clear()
    
    # Create procedural Sky Texture (Nishita) as a standalone proxy for an HDRI
    node_sky = nodes.new(type='ShaderNodeTexSky')
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = math.radians(sun_elevation_deg)
    node_sky.sun_rotation = math.radians(sun_rotation_deg)
    # Default Nishita is very bright, scaling down slightly for easier exposure management
    node_sky.sun_intensity = 0.5 
    
    # Create Background Node
    node_bg = nodes.new(type='ShaderNodeBackground')
    node_bg.inputs['Strength'].default_value = sun_intensity
    
    # Create Output Node
    node_out = nodes.new(type='ShaderNodeOutputWorld')
    
    # Position nodes for neatness in the Shader Editor
    node_sky.location = (-400, 0)
    node_bg.location = (-200, 0)
    node_out.location = (0, 0)
    
    # Link the environment node chain
    links.new(node_sky.outputs['Color'], node_bg.inputs['Color'])
    links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])
    
    return f"Configured interior daylighting on '{scene.name}': Cycles active, Diffuse Bounces={diffuse_bounces}, Transparent={transparent_bounces}. Generated World '{world_name}'."

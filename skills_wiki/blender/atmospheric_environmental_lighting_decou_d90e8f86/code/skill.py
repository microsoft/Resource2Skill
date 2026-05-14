def create_atmospheric_lighting(
    scene_name: str = "Scene",
    mood: str = "sunset", 
    sun_rotation: float = 45.0, 
    sun_angle: float = 5.0, 
    ambient_strength: float = 1.0,
    **kwargs,
) -> str:
    """
    Create Atmospheric Environmental Lighting (Decoupled Sky + Custom Sun).

    Args:
        scene_name: Name of the target scene.
        mood: Lighting mood - 'sunny', 'sunset', or 'night'.
        sun_rotation: Azimuth of the sun in degrees.
        sun_angle: Softness of the sun's shadows in degrees (larger = softer).
        ambient_strength: Strength of the ambient sky light.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Euler

    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene

    # === Step 1: Create Procedural Sky Environment ===
    # Creates an additive new world to not destroy existing setups
    world_name = f"Atmospheric_World_{mood.capitalize()}"
    world = bpy.data.worlds.new(name=world_name)
    scene.world = world
    world.use_nodes = True
    tree = world.node_tree

    # Clear default nodes safely
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Create new nodes
    sky_node = tree.nodes.new(type="ShaderNodeTexSky")
    sky_node.sky_type = 'NISHITA'
    
    # CRITICAL: Decouple direct sun from ambient sky (matches tutorial technique)
    # This prevents double shadows and lets the Custom Sun take over.
    sky_node.sun_disc = False 
    sky_node.location = (0, 0)

    bg_node = tree.nodes.new(type="ShaderNodeBackground")
    bg_node.location = (300, 0)

    out_node = tree.nodes.new(type="ShaderNodeOutputWorld")
    out_node.location = (600, 0)

    # Link nodes
    tree.links.new(sky_node.outputs['Color'], bg_node.inputs['Color'])
    tree.links.new(bg_node.outputs['Background'], out_node.inputs['Surface'])

    # === Step 2: Configure Mood Parameters ===
    if mood.lower() == "sunny":
        sun_elevation = 60.0
        sky_node.dust_density = 1.0
        sky_node.air_density = 1.0
        sun_color = (1.0, 0.95, 0.9)
        sun_energy = 5.0
    elif mood.lower() == "sunset":
        sun_elevation = 3.0
        sky_node.dust_density = 4.0
        sky_node.air_density = 2.0
        sun_color = (1.0, 0.4, 0.1)
        sun_energy = 2.0
    elif mood.lower() == "night":
        sun_elevation = -5.0 # Sun below horizon for twilight/night sky
        sky_node.dust_density = 0.5
        sky_node.air_density = 1.0
        sun_color = (0.2, 0.4, 0.8) # Moonlight
        sun_energy = 0.2
        ambient_strength *= 0.5 # Dimmer ambient for night
    else:
        sun_elevation = 35.0
        sun_color = (1.0, 0.9, 0.8)
        sun_energy = 3.0

    # Apply to Sky Node
    sky_node.sun_elevation = math.radians(sun_elevation)
    sky_node.sun_rotation = math.radians(sun_rotation)
    bg_node.inputs['Strength'].default_value = ambient_strength

    # === Step 3: Create Custom Sun Light ===
    # This acts as the primary shadow caster, allowing independent control
    # of shadow softness (sun_angle) and crisp lighting direction.
    sun_data = bpy.data.lights.new(name=f"Custom_Env_Sun_{mood}_Data", type='SUN')
    sun_data.energy = sun_energy
    sun_data.color = sun_color
    sun_data.angle = math.radians(sun_angle) 

    sun_obj = bpy.data.objects.new(name=f"Custom_Env_Sun_{mood}", object_data=sun_data)
    scene.collection.objects.link(sun_obj)

    # Align custom sun rotation to match the procedural sky
    if mood.lower() == "night":
        # Moon at an independent high angle
        pitch = math.radians(90 - 45.0) 
    else:
        pitch = math.radians(90 - sun_elevation)
        
    yaw = math.radians(sun_rotation)
    
    # Roll (Y) is 0. Pitch is rotation around X axis. Yaw is rotation around Z axis.
    sun_obj.rotation_euler = Euler((pitch, 0, yaw), 'XYZ')

    return f"Created atmospheric '{mood}' lighting with sun at rotation {sun_rotation} deg and angle {sun_angle} deg."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "StudioLightSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.9, 0.8), # Used as the Warm Key Light Color
    **kwargs,
) -> str:
    """
    Create Parametric Three-Point Studio Lighting in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created lighting objects.
        location: (x, y, z) world-space position of the focal target.
        scale: Distance multiplier for the lights (Energy scales automatically).
        material_color: (R, G, B) color of the main Key Light.
        **kwargs: Additional overrides for fill/rim ratios and colors.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Lighting Parameters
    base_distance = 5.0 * scale
    
    # Energy scales with the square of the distance (Inverse Square Law)
    key_energy = kwargs.get('key_energy', 1000.0 * (scale ** 2)) 
    fill_ratio = kwargs.get('fill_ratio', 0.4) # Fill is 40% as bright as Key
    fill_color = kwargs.get('fill_color', (0.8, 0.9, 1.0)) # Cool Cyan/Blue
    rim_energy = kwargs.get('rim_energy', 2000.0 * (scale ** 2)) # Rim is hottest
    rim_color = kwargs.get('rim_color', (0.7, 0.8, 1.0)) # Cool Blue
    
    # 1. Create target empty for lights to track
    target_obj = bpy.data.objects.new(f"{object_name}_Target", None)
    target_obj.location = Vector(location)
    target_obj.empty_display_type = 'CROSS'
    target_obj.empty_display_size = scale
    scene.collection.objects.link(target_obj)

    # Helper function to create, position, and aim lights
    def add_light(name, location_offset, energy, color, size):
        # Create light data
        light_data = bpy.data.lights.new(name=f"{name}_Data", type='AREA')
        light_data.energy = energy
        light_data.color = color
        light_data.size = size
        light_data.shape = 'SQUARE'

        # Create light object
        light_obj = bpy.data.objects.new(name, light_data)
        scene.collection.objects.link(light_obj)
        
        # Position in world space relative to the target
        light_obj.location = target_obj.location + Vector(location_offset)
        
        # Add Track To constraint pointing at the target Empty
        track = light_obj.constraints.new(type='TRACK_TO')
        track.target = target_obj
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        return light_obj

    # === Step 2: Spawn Lights ===
    
    # Key Light (Front-Right, High, Warm, Medium softness)
    key_offset = (base_distance * 0.7, -base_distance * 0.8, base_distance * 0.7)
    add_light(
        name=f"{object_name}_Key", 
        location_offset=key_offset, 
        energy=key_energy, 
        color=material_color, 
        size=base_distance * 0.5
    )

    # Fill Light (Front-Left, Lower, Cool, Maximum softness)
    fill_offset = (-base_distance * 0.8, -base_distance * 0.5, base_distance * 0.3)
    add_light(
        name=f"{object_name}_Fill", 
        location_offset=fill_offset, 
        energy=key_energy * fill_ratio, 
        color=fill_color, 
        size=base_distance * 0.8
    )

    # Rim Light (Back-Left, High, Cool, Harder shadows for sharp silhouette)
    rim_offset = (-base_distance * 0.4, base_distance * 0.9, base_distance * 0.6)
    add_light(
        name=f"{object_name}_Rim", 
        location_offset=rim_offset, 
        energy=rim_energy, 
        color=rim_color, 
        size=base_distance * 0.2
    )

    return f"Created Three-Point Lighting setup '{object_name}' focused at {location} (Scale: {scale})."

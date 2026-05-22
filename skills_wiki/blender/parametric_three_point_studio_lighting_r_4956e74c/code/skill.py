def create_object(
    scene_name: str = "Scene",
    object_name: str = "ThreePointRig",
    location: tuple = (0.0, 0.0, 1.0),
    scale: float = 3.0,
    material_color: tuple = (1.0, 1.0, 1.0),  # Unused for lights, but kept for signature compliance
    **kwargs,
) -> str:
    """
    Create a parametric Three-Point Studio Lighting Rig with physically accurate temperatures.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig components.
        location: (x, y, z) focal point of the rig (where the subject should be).
        scale: Radius/distance of the lights from the focal point.
        material_color: Ignored for lights.
        **kwargs: 
            key_energy (float): Power in Watts for the Key light (default 1000).
            fill_ratio (float): Ratio of fill energy to key energy (default 0.3).
            rim_ratio (float): Ratio of rim energy to key energy (default 1.5).

    Returns:
        Status string detailing the rig creation.
    """
    import bpy
    import math
    from mathutils import Vector

    # Get target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # Variables
    target_loc = Vector(location)
    radius = scale
    
    key_energy = kwargs.get('key_energy', 1000.0)
    fill_energy = key_energy * kwargs.get('fill_ratio', 0.3)
    rim_energy = key_energy * kwargs.get('rim_ratio', 1.5)

    created_objects = []

    # 1. Create the Target Empty
    target_data = bpy.data.objects.new(f"{object_name}_Target", None)
    target_data.empty_display_type = 'CROSS'
    target_data.empty_display_size = 0.5
    target_data.location = target_loc
    collection.objects.link(target_data)
    created_objects.append(target_data.name)

    # Helper function to create a light with a blackbody node and tracking constraint
    def add_studio_light(name, light_type, location_offset, energy, size, temp_kelvin):
        # Create light data
        light_data = bpy.data.lights.new(name=name, type=light_type)
        light_data.energy = energy
        if light_type == 'AREA':
            light_data.shape = 'RECTANGLE'
            light_data.size = size
            light_data.size_y = size * 1.5
            
        # Setup Node Tree for Blackbody Color Temperature
        light_data.use_nodes = True
        tree = light_data.node_tree
        nodes = tree.nodes
        links = tree.links
        
        # Clear default color connections
        emission_node = None
        for node in nodes:
            if node.type == 'EMISSION':
                emission_node = node
                break
                
        if emission_node:
            bb_node = nodes.new(type='ShaderNodeBlackbody')
            bb_node.location = (emission_node.location.x - 200, emission_node.location.y)
            bb_node.inputs['Temperature'].default_value = temp_kelvin
            links.new(bb_node.outputs['Color'], emission_node.inputs['Color'])

        # Create light object
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        light_obj.location = target_loc + Vector(location_offset)
        collection.objects.link(light_obj)
        
        # Add Track To Constraint
        track = light_obj.constraints.new(type='TRACK_TO')
        track.target = target_data
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        # Parent to empty for easy moving of the whole rig
        light_obj.parent = target_data
        
        return light_obj

    # 2. Key Light (Front-Left, High, Neutral-Warm Daylight)
    # Positions x=-radius, y=-radius (front), z=radius (high)
    add_studio_light(
        name=f"{object_name}_Key",
        light_type='AREA',
        location_offset=(-radius, -radius * 1.2, radius * 0.8),
        energy=key_energy,
        size=radius * 0.5,
        temp_kelvin=5500.0
    )

    # 3. Fill Light (Front-Right, Lower, Cooler to mimic sky fill)
    add_studio_light(
        name=f"{object_name}_Fill",
        light_type='AREA',
        location_offset=(radius * 0.8, -radius, radius * 0.2),
        energy=fill_energy,
        size=radius * 0.8, # Larger = softer
        temp_kelvin=7500.0
    )

    # 4. Rim Light (Back-Center, High, Warmer to separate from background)
    add_studio_light(
        name=f"{object_name}_Rim",
        light_type='AREA',
        location_offset=(radius * 0.2, radius * 1.5, radius * 1.2),
        energy=rim_energy,
        size=radius * 0.3, # Smaller = sharper edge
        temp_kelvin=4500.0
    )

    return f"Created Three-Point Lighting Rig '{object_name}' tracking to {location} with scale/radius {scale}. Target Empty and 3 Lights added."

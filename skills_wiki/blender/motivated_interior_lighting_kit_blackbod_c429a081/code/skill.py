def create_motivated_interior_lighting(
    scene_name: str = "Scene",
    kit_name: str = "Motivated_Light_Kit",
    location: tuple = (0, 0, 0),
    scale: float = 1.0, # Scales relative positions
    key_temperature: float = 4500.0,  # Neutral/Warm overhead
    fill_temperature: float = 6500.0, # Cool screen/window fill
    alarm_color: tuple = (1.0, 0.02, 0.0) # RGB for emergency light
) -> str:
    """
    Creates an interior lighting kit utilizing Spot, Area, and Point lights 
    driven by procedural Blackbody temperature nodes for physical accuracy.
    
    Args:
        scene_name: Name of the target scene.
        kit_name: Base name for the generated objects.
        location: (x, y, z) world-space base position for the kit.
        scale: Spacing multiplier for the light arrangement.
        key_temperature: Kelvin temperature for the overhead spotlight.
        fill_temperature: Kelvin temperature for the area light.
        alarm_color: RGB tuple for the local practical point light.
        
    Returns:
        Status string detailing the created lighting setup.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)
    
    # Create a collection to keep the scene organized
    kit_collection = bpy.data.collections.new(kit_name)
    scene.collection.children.link(kit_collection)

    # --- Helper Function: Create Light with Node Setup ---
    def add_physical_light(name, l_type, rel_loc, rot_euler, energy, temp=None, color=None):
        # Create Data and Object
        light_data = bpy.data.lights.new(name=name + "_Data", type=l_type)
        light_data.energy = energy
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        kit_collection.objects.link(light_obj)
        
        # Transform
        light_obj.location = base_loc + (Vector(rel_loc) * scale)
        light_obj.rotation_euler = rot_euler
        
        # Setup Nodes (Blackbody or RGB)
        light_data.use_nodes = True
        tree = light_data.node_tree
        nodes = tree.nodes
        links = tree.links
        
        # Clear default nodes safely
        for n in nodes:
            nodes.remove(n)
            
        out_node = nodes.new('ShaderNodeOutputLight')
        out_node.location = (300, 0)
        
        em_node = nodes.new('ShaderNodeEmission')
        em_node.location = (100, 0)
        links.new(em_node.outputs['Emission'], out_node.inputs['Surface'])
        
        if temp is not None:
            bb_node = nodes.new('ShaderNodeBlackbody')
            bb_node.location = (-100, 0)
            bb_node.inputs['Temperature'].default_value = temp
            links.new(bb_node.outputs['Color'], em_node.inputs['Color'])
        elif color is not None:
            em_node.inputs['Color'].default_value = (*color, 1.0)
            
        return light_obj, light_data

    # === 1. Overhead Motivated Key (Spotlight) ===
    # Points straight down, high blend for soft edges
    spot_obj, spot_data = add_physical_light(
        name=f"{kit_name}_Overhead_Spot",
        l_type='SPOT',
        rel_loc=(0, 0, 3),
        rot_euler=(0, 0, 0), # Points down -Z
        energy=1500.0 * scale,
        temp=key_temperature
    )
    spot_data.spot_size = math.radians(75)
    spot_data.spot_blend = 1.0 # 100% softened edge
    spot_data.shadow_soft_size = 0.25 # Soft shadows

    # === 2. Screen/Panel Motivated Fill (Area Light) ===
    # Rectangular, points +Y into the room
    area_obj, area_data = add_physical_light(
        name=f"{kit_name}_Screen_Area",
        l_type='AREA',
        rel_loc=(0, -2, 1.5),
        rot_euler=(math.pi/2, 0, 0), 
        energy=800.0 * scale,
        temp=fill_temperature
    )
    area_data.shape = 'RECTANGLE'
    area_data.size = 3.0 * scale
    area_data.size_y = 0.5 * scale

    # === 3. Alarm/Practical (Point Light) ===
    # Small radius for hard shadows, colored RGB
    point_loc = (2.0, 0, 2.0)
    point_obj, point_data = add_physical_light(
        name=f"{kit_name}_Alarm_Point",
        l_type='POINT',
        rel_loc=point_loc,
        rot_euler=(0, 0, 0),
        energy=200.0 * scale,
        color=alarm_color
    )
    point_data.shadow_soft_size = 0.05 * scale # Crisp shadows for small bulb

    # === 4. Motivating Geometry for the Alarm ===
    # A physical object with an emission shader to represent the bulb
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, 
        radius=0.1 * scale, 
        depth=0.15 * scale,
        location=base_loc + (Vector(point_loc) * scale),
        rotation=(math.pi/2, 0, 0)
    )
    bulb_obj = bpy.context.active_object
    bulb_obj.name = f"{kit_name}_Alarm_Fixture"
    
    # Move from default collection to kit collection
    for coll in bulb_obj.users_collection:
        coll.objects.unlink(bulb_obj)
    kit_collection.objects.link(bulb_obj)

    # Pure Emission Material for the bulb
    mat = bpy.data.materials.new(name=f"{kit_name}_Alarm_Mat")
    mat.use_nodes = True
    mnodes = mat.node_tree.nodes
    for n in mnodes:
        mnodes.remove(n)
    
    m_out = mnodes.new('ShaderNodeOutputMaterial')
    m_em = mnodes.new('ShaderNodeEmission')
    m_em.inputs['Color'].default_value = (*alarm_color, 1.0)
    m_em.inputs['Strength'].default_value = 10.0 # Blown out visually
    mat.node_tree.links.new(m_em.outputs['Emission'], m_out.inputs['Surface'])
    
    bulb_obj.data.materials.append(mat)

    # === 5. Scene Rendering Context ===
    # Set to High Contrast for cinematic falloff as recommended in tutorial
    scene.view_settings.look = 'High Contrast'

    return f"Created '{kit_name}' at {location}. Includes: Soft Spot ({key_temperature}K), Rectangular Area ({fill_temperature}K), and Point light with physical fixture."

def create_artificial_lighting_rig(
    scene_name: str = "Scene",
    object_name: str = "NightLightingRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    temperature_k: float = 4500.0,
    exposure_value: float = 3.0,
    gi_bounces: int = 8,
    **kwargs,
) -> str:
    """
    Creates a highly realistic interior artificial lighting rig and configures 
    scene render settings (Cycles, Bounces, Exposure) for windowless/night renders.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root empty controlling the lighting rig.
        location: (x, y, z) base position of the rig.
        scale: Uniform scale factor for the rig.
        material_color: Ignored here; lighting relies on physical temperature.
        temperature_k: Blackbody temperature for the lights (e.g., 4500 for neutral/warm).
        exposure_value: Camera exposure compensation (since World is dark).
        gi_bounces: Number of Diffuse/Glossy bounces to propagate light.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render & Scene Context Configuration ===
    scene.render.engine = 'CYCLES'
    
    # Isolate from external natural light (Disable World)
    if scene.world and scene.world.node_tree:
        bg_node = scene.world.node_tree.nodes.get('Background')
        if bg_node:
            bg_node.inputs['Strength'].default_value = 0.0

    # Increase Exposure to compensate for isolated artificial light
    scene.view_settings.exposure = exposure_value

    # Maximize Global Illumination (GI) bounces for realistic interior light spread
    scene.cycles.max_bounces = gi_bounces + 4
    scene.cycles.diffuse_bounces = gi_bounces
    scene.cycles.glossy_bounces = gi_bounces
    scene.cycles.transparent_max_bounces = gi_bounces

    # === Step 2: Create Master Rig Controller ===
    rig_root = bpy.data.objects.new(object_name, None)
    rig_root.empty_display_type = 'SPHERE'
    rig_root.empty_display_size = 0.5
    rig_root.location = Vector(location)
    rig_root.scale = (scale, scale, scale)
    scene.collection.objects.link(rig_root)

    # === Helper Function to Build Node-Based Lights ===
    def add_blackbody_light(l_name, l_type, rel_loc, energy, temp, spread_deg=None):
        l_data = bpy.data.lights.new(name=f"{l_name}_Data", type=l_type)
        l_data.energy = energy
        
        # Apply Spread for Area Lights
        if l_type == 'AREA' and spread_deg is not None:
            l_data.spread = math.radians(spread_deg)
            
        # Create Node Tree for Blackbody calculation
        l_data.use_nodes = True
        tree = l_data.node_tree
        tree.nodes.clear()
        
        out_node = tree.nodes.new('ShaderNodeOutputLight')
        out_node.location = (300, 0)
        
        em_node = tree.nodes.new('ShaderNodeEmission')
        em_node.location = (100, 0)
        
        bb_node = tree.nodes.new('ShaderNodeBlackbody')
        bb_node.location = (-100, 0)
        bb_node.inputs['Temperature'].default_value = temp
        
        # Connect nodes: Blackbody -> Emission -> Output
        tree.links.new(bb_node.outputs['Color'], em_node.inputs['Color'])
        tree.links.new(em_node.outputs['Emission'], out_node.inputs['Surface'])
        
        # Create object and parent to rig
        l_obj = bpy.data.objects.new(l_name, l_data)
        l_obj.location = Vector(rel_loc)
        l_obj.parent = rig_root
        scene.collection.objects.link(l_obj)
        return l_obj

    # === Step 3: Populate Lighting Rig ===
    # 1. Diffuse Ambient Fill (High Spread Area Light)
    fill_light = add_blackbody_light(
        l_name=f"{object_name}_AmbientFill",
        l_type='AREA',
        rel_loc=(0, 0, 3), # 3 meters up
        energy=50.0,
        temp=temperature_k,
        spread_deg=180.0 # Wide diffuse
    )
    fill_light.data.shape = 'RECTANGLE'
    fill_light.data.size = 4.0
    fill_light.data.size_y = 4.0

    # 2. Focused Architectural Downlights (Low Spread Area Lights)
    offsets = [(-1.5, -1.5, 2.9), (1.5, -1.5, 2.9), (-1.5, 1.5, 2.9), (1.5, 1.5, 2.9)]
    for i, pos in enumerate(offsets):
        add_blackbody_light(
            l_name=f"{object_name}_Downlight_{i}",
            l_type='AREA',
            rel_loc=pos,
            energy=15.0,
            temp=temperature_k,
            spread_deg=50.0 # Focused spot
        )
        
    # 3. Practical Glow (Low Energy Point Light for fixture simulation)
    add_blackbody_light(
        l_name=f"{object_name}_PracticalChandelier",
        l_type='POINT',
        rel_loc=(0, 0, 1.5),
        energy=1.0,
        temp=temperature_k + 500, # Slightly warmer/cooler variation
    )

    # === Step 4: Create Corresponding Emissive Material for LED Strips ===
    mat_name = f"{object_name}_LED_Material"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        bsdf = nodes.get("Principled BSDF")
        bb_node = nodes.new('ShaderNodeBlackbody')
        bb_node.location = (-300, -200)
        bb_node.inputs['Temperature'].default_value = temperature_k
        
        links.new(bb_node.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = 5.0
        bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0) # Dark base

    return f"Created '{object_name}' (Night Lighting Rig) at {location}. Setup Cycles with {gi_bounces} bounces, exposure {exposure_value}, and {temperature_k}K blackbody lighting."

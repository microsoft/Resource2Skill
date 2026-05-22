def create_object(
    scene_name: str = "Scene",
    object_name: str = "RealisticFire",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.4, 0.0), # Base orange/red hue
    **kwargs,
) -> str:
    """
    Create a Realistic Volumetric Fire Simulation.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position of the fire source.
        scale: Size multiplier for the emitter and domain.
        material_color: (R, G, B) mid-tone color of the fire.
        **kwargs: Optional 'resolution' (default 64, recommend 128+ for final renders).

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Cycles for physically accurate volumetric emission
    scene.render.engine = 'CYCLES'

    # === Step 1: Create the Flow Object (Emitter) ===
    bpy.ops.mesh.primitive_ico_sphere_add(radius=scale, location=location)
    flow_obj = bpy.context.active_object
    flow_obj.name = f"{object_name}_Emitter"
    
    # Add Fluid Modifier to Flow Object
    fluid_mod_flow = flow_obj.modifiers.new(name="Fluid", type='FLUID')
    fluid_mod_flow.fluid_type = 'FLOW'
    flow_settings = fluid_mod_flow.flow_settings
    flow_settings.flow_type = 'FIRE'
    flow_settings.flow_behavior = 'INFLOW'
    
    # Advanced fire properties
    if hasattr(flow_settings, 'fuel_amount'):
        flow_settings.fuel_amount = 2.0
    if hasattr(flow_settings, 'surface_distance'):
        flow_settings.surface_distance = 1.0
        
    # Flow Texture for chaotic, uneven emission
    tex = bpy.data.textures.new(name=f"{object_name}_FireTex", type='CLOUDS')
    tex.noise_scale = 0.1
    tex.contrast = 5.0
    if hasattr(flow_settings, 'use_texture'):
        flow_settings.use_texture = True
        flow_settings.noise_texture = tex

    # === Step 2: Create the Domain Object ===
    # Position the domain slightly above the emitter
    domain_loc = (location[0], location[1], location[2] + scale * 2.0)
    bpy.ops.mesh.primitive_cube_add(size=scale * 6, location=domain_loc)
    domain_obj = bpy.context.active_object
    domain_obj.name = f"{object_name}_Domain"
    domain_obj.display_type = 'BOUNDS' # Keep viewport clean
    
    # Add Fluid Modifier to Domain Object
    fluid_mod_domain = domain_obj.modifiers.new(name="Fluid", type='FLUID')
    fluid_mod_domain.fluid_type = 'DOMAIN'
    domain_settings = fluid_mod_domain.domain_settings
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = kwargs.get('resolution', 64)
    
    if hasattr(domain_settings, 'use_adaptive_domain'):
        domain_settings.use_adaptive_domain = True
        
    # Gas & Fire behavior parameters
    if hasattr(domain_settings, 'vorticity'):
        domain_settings.vorticity = 0.1
    if hasattr(domain_settings, 'flame_vorticity'):
        domain_settings.flame_vorticity = 0.1
    if hasattr(domain_settings, 'flame_reaction_speed'):
        domain_settings.flame_reaction_speed = 0.5
        
    # Set to REPLAY so it evaluates dynamically on the timeline
    if hasattr(domain_settings, 'cache_type'):
        domain_settings.cache_type = 'REPLAY'

    # === Step 3: Create Volumetric Material for Domain ===
    mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    mat.use_nodes = True
    domain_obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Core Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)
    
    vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
    vol_node.location = (100, 0)
    if 'Density' in vol_node.inputs:
        vol_node.inputs['Density'].default_value = 0.0 # Remove black smoke
        
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    
    # Import Mantaflow 'heat' attribute
    attr_node = nodes.new(type='ShaderNodeAttribute')
    attr_node.attribute_name = 'heat'
    attr_node.location = (-500, 0)
    
    # Color Ramp for Emission Color
    ramp_color = nodes.new(type='ShaderNodeValToRGB')
    ramp_color.location = (-200, 150)
    c_elements = ramp_color.color_ramp.elements
    c_elements[0].position = 0.0
    c_elements[0].color = (0.0, 0.0, 0.0, 1.0)
    c_elements[1].position = 0.5
    c_elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    el = c_elements.new(0.9)
    el.color = (1.0, 0.8, 0.2, 1.0) # Bright yellow core
    
    # Color Ramp for Emission Strength Masking
    ramp_strength = nodes.new(type='ShaderNodeValToRGB')
    ramp_strength.location = (-200, -150)
    s_elements = ramp_strength.color_ramp.elements
    s_elements[0].position = 0.0
    s_elements[0].color = (0.0, 0.0, 0.0, 1.0)
    s_elements[1].position = 1.0
    s_elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Math Node to Multiply Strength
    math_node = nodes.new(type='ShaderNodeMath')
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 15.0 # Intensity boost multiplier
    math_node.location = (50, -150)
    
    # Connect mapping logic
    links.new(attr_node.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(attr_node.outputs['Fac'], ramp_strength.inputs['Fac'])
    
    if 'Emission Color' in vol_node.inputs:
        links.new(ramp_color.outputs['Color'], vol_node.inputs['Emission Color'])
    
    links.new(ramp_strength.outputs['Color'], math_node.inputs[0])
    
    if 'Emission Strength' in vol_node.inputs:
        links.new(math_node.outputs['Value'], vol_node.inputs['Emission Strength'])
        
    # === Step 4: Evaluate Physics Cache ===
    # Fast-forward the timeline to frame 30 to pre-calculate the volumetric data
    # so the fire is immediately visible to the user/agent without manually pressing play.
    bpy.context.view_layer.objects.active = domain_obj
    domain_obj.select_set(True)
    
    scene.frame_set(1)
    bpy.context.view_layer.update()
    for f in range(2, 31):
        scene.frame_set(f)
        bpy.context.view_layer.update()

    return f"Created '{object_name}' (Emitter & Domain) at {location}. Advanced timeline to frame 30 to display simulation."

def create_fake_volumetrics(
    scene_name: str = "Scene",
    object_name: str = "Volumetric_Portal",
    location: tuple = (0, 5, 2),
    scale: float = 2.0,
    material_color: tuple = (1.0, 0.9, 0.7),
    mist_depth: float = 30.0,
    ray_length: float = 0.15,
    sun_source_x: float = 0.0,
    sun_source_y: float = 1.0,
    **kwargs,
) -> str:
    """
    Creates a compositor-based fake volumetric fog and god ray setup, along with 
    a hidden emission portal plane to generate the rays.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the helper emission plane.
        location: (x, y, z) position for the emission plane (place outside windows).
        scale: Uniform scale for the emission plane.
        material_color: (R, G, B) color of the god rays.
        mist_depth: Distance in meters for the fog to reach maximum density.
        ray_length: Length of the sun beams (0.0 to 1.0).
        sun_source_x: 2D X coordinate for the origin of the sun beams (0-1).
        sun_source_y: 2D Y coordinate for the origin of the sun beams (0-1).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Enable Rendering Passes and World Mist ===
    view_layer = scene.view_layers[0]
    view_layer.use_pass_mist = True
    view_layer.use_pass_emit = True

    world = scene.world
    if world:
        world.mist_settings.start = 0.0
        world.mist_settings.depth = mist_depth

    # === Step 2: Build the Compositor Node Tree ===
    scene.use_nodes = True
    tree = scene.node_tree

    # Find existing input/output nodes or create them
    rl_node = None
    comp_node = None
    for node in tree.nodes:
        if node.type == 'R_LAYERS':
            rl_node = node
        elif node.type == 'COMPOSITE':
            comp_node = node

    if not rl_node:
        rl_node = tree.nodes.new('CompositorNodeRLayers')
        rl_node.location = (-300, 0)
    
    if not comp_node:
        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = (1500, 0)

    # Fog setup
    fog_mix = tree.nodes.new('CompositorNodeMixRGB')
    fog_mix.blend_type = 'ADD'
    fog_mix.location = (200, 100)

    fog_ramp = tree.nodes.new('CompositorNodeValToRGB')
    fog_ramp.location = (-100, -100)
    # Default Black to White mapping is correct for Mist

    # Sun Beams setup
    sun_beams = tree.nodes.new('CompositorNodeSunBeams')
    sun_beams.location = (200, -300)
    sun_beams.ray_length = ray_length
    sun_beams.source = (sun_source_x, sun_source_y)

    sun_mix = tree.nodes.new('CompositorNodeMixRGB')
    sun_mix.blend_type = 'ADD'
    sun_mix.location = (500, 0)

    # Post Processing setup
    glare = tree.nodes.new('CompositorNodeGlare')
    glare.glare_type = 'FOG_GLOW'
    glare.quality = 'HIGH'
    glare.location = (800, 0)

    blur = tree.nodes.new('CompositorNodeBokehBlur')
    blur.use_variable_size = False
    blur.blur_max = 0.02  # Slight softening
    blur.location = (1100, 0)

    # Connect the compositing pipeline
    links = tree.links
    # Fog chain
    links.new(rl_node.outputs['Image'], fog_mix.inputs[1])
    links.new(rl_node.outputs['Mist'], fog_ramp.inputs['Fac'])
    links.new(fog_ramp.outputs[0], fog_mix.inputs[2])
    
    # Sun rays chain
    links.new(rl_node.outputs['Emit'], sun_beams.inputs['Image'])
    
    # Combine Fog and Rays
    links.new(fog_mix.outputs['Image'], sun_mix.inputs[1])
    links.new(sun_beams.outputs['Image'], sun_mix.inputs[2])
    
    # Polish and Output
    links.new(sun_mix.outputs['Image'], glare.inputs['Image'])
    links.new(glare.outputs['Image'], blur.inputs['Image'])
    links.new(blur.outputs['Image'], comp_node.inputs['Image'])


    # === Step 3: Create the Emission Portal Helper Mesh ===
    bpy.ops.mesh.primitive_plane_add(size=1)
    obj = bpy.context.active_object
    obj.name = object_name
    
    obj.location = location
    obj.scale = (scale, scale, scale)
    obj.rotation_euler = (1.5708, 0, 0)  # Rotated 90 degrees on X to stand upright

    # Prevent the plane from casting shadows and blocking real light
    obj.visible_shadow = False
    
    # Create the Emission material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    mat.shadow_method = 'NONE' # EEVEE shadow compatibility
    
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        nodes.remove(bsdf)
        
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
    emit.inputs['Strength'].default_value = 5.0  # High intensity for the emit pass
    
    mat_out = nodes.get("Material Output")
    mat.node_tree.links.new(emit.outputs['Emission'], mat_out.inputs['Surface'])
    
    obj.data.materials.append(mat)

    return f"Created Compositor Volumetric setup and '{object_name}' helper plane at {location}. Position the plane outside the scene windows."

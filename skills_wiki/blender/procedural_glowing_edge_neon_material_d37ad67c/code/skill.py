def create_glowing_edge_object(
    scene_name: str = "Scene",
    object_name: str = "NeonEdge_Suzanne",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    glow_color: tuple = (1.0, 0.05, 0.05), # Bright Neon Red
    glow_strength: float = 15.0,
    **kwargs,
) -> str:
    """
    Create a mesh with a procedural glowing edge (neon) shader and sets up compositing bloom.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        glow_color: (R, G, B) color of the neon emission.
        glow_strength: Intensity of the emission (high values trigger bloom).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    # Get or create the scene
    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene

    # === Step 1: Create Base Geometry ===
    # Add a Suzanne (Monkey) as the base mesh to show off curved edges
    bpy.ops.mesh.primitive_monkey_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Smooth shading is critical for Layer Weight / Facing gradients
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # Add Subdivision Surface for smoother edge normals
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Build the Procedural Glowing Edge Material ===
    mat = bpy.data.materials.new(name=f"Mat_NeonEdge_{object_name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes safely
    nodes.clear()

    # Create Material Nodes
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (800, 0)

    node_mix = nodes.new('ShaderNodeMixShader')
    node_mix.location = (600, 0)

    node_principled = nodes.new('ShaderNodeBsdfPrincipled')
    node_principled.location = (300, 100)
    # Set base color to very dark, high roughness
    node_principled.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
    if 'Roughness' in node_principled.inputs:
        node_principled.inputs['Roughness'].default_value = 0.8

    node_emission = nodes.new('ShaderNodeEmission')
    node_emission.location = (300, -100)
    node_emission.inputs['Color'].default_value = (*glow_color, 1.0)
    node_emission.inputs['Strength'].default_value = glow_strength

    node_ramp = nodes.new('ShaderNodeValToRGB')
    node_ramp.location = (300, 350)
    # Configure ColorRamp to B-Spline as per tutorial for smooth transition
    ramp = node_ramp.color_ramp
    ramp.interpolation = 'B_SPLINE'
    ramp.elements[0].position = 0.15 # Pinch the dark core slightly
    ramp.elements[1].position = 0.85 # Smoothly fall off before the absolute edge

    node_layer_weight = nodes.new('ShaderNodeLayerWeight')
    node_layer_weight.location = (100, 350)
    node_layer_weight.inputs['Blend'].default_value = 0.2

    # Link Material Nodes
    links.new(node_layer_weight.outputs['Facing'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_mix.inputs['Fac']) # Drives the mix
    links.new(node_principled.outputs['BSDF'], node_mix.inputs[1]) # Core (Dark)
    links.new(node_emission.outputs['Emission'], node_mix.inputs[2]) # Edge (Glow)
    links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 3: Setup Compositor for Bloom ===
    # Because Cycles doesn't have native bloom (and Eevee relies on scene settings),
    # the tutorial explicitly enables Compositor nodes and adds a Glare(Bloom) node.
    scene.use_nodes = True
    comp_tree = scene.node_tree
    comp_nodes = comp_tree.nodes
    comp_links = comp_tree.links

    # Find existing Render Layers and Composite nodes
    node_rlayers = next((n for n in comp_nodes if n.type == 'R_LAYERS'), None)
    node_comp = next((n for n in comp_nodes if n.type == 'COMPOSITE'), None)

    # Add them if missing
    if not node_rlayers:
        node_rlayers = comp_nodes.new('CompositorNodeRLayers')
        node_rlayers.location = (-300, 0)
    if not node_comp:
        node_comp = comp_nodes.new('CompositorNodeComposite')
        node_comp.location = (300, 0)

    # Check if a Glare node already exists so we don't spam them on multiple calls
    node_glare = next((n for n in comp_nodes if n.type == 'GLARE'), None)
    if not node_glare:
        node_glare = comp_nodes.new('CompositorNodeGlare')
        node_glare.location = (0, 0)
    
    # Configure Glare Node for Bloom
    node_glare.glare_type = 'BLOOM'
    node_glare.quality = 'HIGH'
    node_glare.inputs['Threshold'].default_value = 1.0 # Only catch high emission values

    # Link Compositor
    comp_links.new(node_rlayers.outputs['Image'], node_glare.inputs['Image'])
    comp_links.new(node_glare.outputs['Image'], node_comp.inputs['Image'])

    # Optional: Try to set Viewport Compositor to 'ALWAYS' for real-time preview 
    # (Matches tutorial's real-time viewport feedback). 
    # Wrapped in try-except to avoid context errors in headless execution.
    try:
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.use_compositor = 'ALWAYS'
    except Exception:
        pass # Silently fail if context is unavailable (e.g., background mode)

    return f"Created '{object_name}' with Glowing Edge Material at {location}. Compositor Bloom active."

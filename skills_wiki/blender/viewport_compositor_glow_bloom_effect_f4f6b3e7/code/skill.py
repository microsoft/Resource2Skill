def create_object(
    scene_name: str = "Scene",
    object_name: str = "GlowingCube",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.05, 0.2),  # Pink/Red glow by default
    **kwargs,
) -> str:
    """
    Create Viewport Compositor Glow (Bloom Effect) in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created glowing object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            emission_strength (float): Intensity of the glow (default 2.0).

    Returns:
        Status string describing the operation.
    """
    import bpy

    # Extract kwargs
    emission_strength = kwargs.get("emission_strength", 2.0)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Material ===
    mat_name = f"{object_name}_EmissionMat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create Emission and Output nodes
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.location = (0, 0)
    # Blender expects RGBA for colors
    node_emission.inputs['Color'].default_value = (*material_color, 1.0)
    node_emission.inputs['Strength'].default_value = emission_strength

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (200, 0)

    # Link material nodes
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 3: Set up Compositor for Bloom ===
    scene.use_nodes = True
    comp_tree = scene.node_tree
    comp_links = comp_tree.links

    # Ensure Render Layers node exists
    render_layers = next((n for n in comp_tree.nodes if n.type == 'R_LAYERS'), None)
    if not render_layers:
        render_layers = comp_tree.nodes.new('CompositorNodeRLayers')
        render_layers.location = (-200, 0)

    # Ensure Composite node exists
    composite = next((n for n in comp_tree.nodes if n.type == 'COMPOSITE'), None)
    if not composite:
        composite = comp_tree.nodes.new('CompositorNodeComposite')
        composite.location = (400, 0)

    # Add Glare node if it doesn't exist
    glare = next((n for n in comp_tree.nodes if n.type == 'GLARE'), None)
    if not glare:
        glare = comp_tree.nodes.new('CompositorNodeGlare')
        glare.location = (100, 0)
        glare.glare_type = 'BLOOM'
        glare.mix = 0.0 # Standard mix

        # Relink through Glare node
        comp_links.new(render_layers.outputs['Image'], glare.inputs['Image'])
        comp_links.new(glare.outputs['Image'], composite.inputs['Image'])
    else:
        # If glare already exists, ensure it's set to BLOOM
        glare.glare_type = 'BLOOM'

    # === Step 4: Configure Viewport (Interactive visual feedback) ===
    # This safely attempts to enable Viewport Compositor if executed in a UI context
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        # 'ALWAYS' setting allows compositor effects in the 3D viewport (Blender 3.5+)
                        if hasattr(space.shading, "compositor"):
                            space.shading.compositor = 'ALWAYS'

    return f"Created glowing '{object_name}' at {location} with Emission Strength {emission_strength} and enabled Compositor Bloom."

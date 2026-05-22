def create_interior_lighting_pipeline(
    scene_name: str = "Scene",
    object_name: str = "Interior_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    white_balance_color: tuple = (0.8, 0.8, 0.8),
    sun_elevation: float = 25.0,
    sun_size: float = 5.0,
    **kwargs,
) -> str:
    """
    Create an interior lighting pipeline with Sky lighting, optimized glass/fabric materials,
    and a cinematic compositor stack. Also spawns demo objects (window and curtain).

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated demo objects.
        location: (x, y, z) position for the demo window.
        scale: Scale factor for the demo objects.
        white_balance_color: (R, G, B) color to neutralize in the compositor.
        sun_elevation: Sun height in degrees.
        sun_size: Sun size in degrees (higher = softer shadows).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: World Sky Lighting ===
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("Interior_World")
        scene.world = world
    world.use_nodes = True
    wtree = world.node_tree
    wtree.nodes.clear()

    bg_node = wtree.nodes.new(type="ShaderNodeBackground")
    out_node = wtree.nodes.new(type="ShaderNodeOutputWorld")
    sky_node = wtree.nodes.new(type="ShaderNodeTexSky")
    
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(sun_elevation)
    sky_node.sun_size = math.radians(sun_size)
    sky_node.sun_intensity = 0.5
    
    wtree.links.new(sky_node.outputs["Color"], bg_node.inputs["Color"])
    wtree.links.new(bg_node.outputs["Background"], out_node.inputs["Surface"])

    # === Step 2: Compositor Post-Processing ===
    scene.use_nodes = True
    comp_tree = scene.node_tree
    
    # Get or create Render Layers and Composite out
    render_layers = comp_tree.nodes.get("Render Layers")
    if not render_layers:
        render_layers = comp_tree.nodes.new(type="CompositorNodeRLayers")
    
    comp_out = comp_tree.nodes.get("Composite")
    if not comp_out:
        comp_out = comp_tree.nodes.new(type="CompositorNodeComposite")

    # Nodes: Divide (White Balance), Brightness/Contrast, Color Balance, Glare
    # Use MixRGB for backward compatibility, automatically maps in Blender 4.0+
    divide_node = comp_tree.nodes.new(type="CompositorNodeMixRGB")
    divide_node.blend_type = 'DIVIDE'
    
    # Helper to safely set second image socket (MixRGB uses 'Image2', Mix uses 'B')
    for sock_name in ["Image2", "B"]:
        if sock_name in divide_node.inputs:
            divide_node.inputs[sock_name].default_value = (*white_balance_color, 1.0)
            break
            
    bc_node = comp_tree.nodes.new(type="CompositorNodeBrightContrast")
    bc_node.inputs["Contrast"].default_value = 2.0
    
    cb_node = comp_tree.nodes.new(type="CompositorNodeColorBalance")
    cb_node.correction_method = 'LIFT_GAMMA_GAIN'
    cb_node.lift = (0.95, 0.97, 1.0) # Slightly cool shadows
    
    glare_node = comp_tree.nodes.new(type="CompositorNodeGlare")
    glare_node.glare_type = 'FOG_GLOW'
    glare_node.quality = 'HIGH'
    glare_node.mix = -0.8

    # Safe linking helper to bypass socket name changes across Blender versions
    def link_sock(out_sock, target_node, possible_names):
        for name in possible_names:
            if name in target_node.inputs:
                comp_tree.links.new(out_sock, target_node.inputs[name])
                return
        comp_tree.links.new(out_sock, target_node.inputs[1])

    link_sock(render_layers.outputs["Image"], divide_node, ["Image1", "A", "Image"])
    link_sock(divide_node.outputs[0], bc_node, ["Image"])
    link_sock(bc_node.outputs[0], cb_node, ["Image"])
    link_sock(cb_node.outputs[0], glare_node, ["Image"])
    link_sock(glare_node.outputs[0], comp_out, ["Image"])

    # === Step 3: Architectural Glass Material ===
    glass_mat = bpy.data.materials.new("Arch_Glass")
    glass_mat.use_nodes = True
    gtree = glass_mat.node_tree
    gtree.nodes.clear()

    g_out = gtree.nodes.new(type="ShaderNodeOutputMaterial")
    g_mix = gtree.nodes.new(type="ShaderNodeMixShader")
    g_glass = gtree.nodes.new(type="ShaderNodeBsdfGlass")
    g_transp = gtree.nodes.new(type="ShaderNodeBsdfTransparent")
    g_lp = gtree.nodes.new(type="ShaderNodeLightPath")
    g_math = gtree.nodes.new(type="ShaderNodeMath")
    
    g_glass.inputs["Roughness"].default_value = 0.05
    g_math.operation = 'MAXIMUM'
    
    gtree.links.new(g_lp.outputs["Is Shadow Ray"], g_math.inputs[0])
    gtree.links.new(g_lp.outputs["Is Diffuse Ray"], g_math.inputs[1])
    gtree.links.new(g_math.outputs["Value"], g_mix.inputs["Fac"])
    gtree.links.new(g_glass.outputs["BSDF"], g_mix.inputs[1])
    gtree.links.new(g_transp.outputs["BSDF"], g_mix.inputs[2])
    gtree.links.new(g_mix.outputs["Shader"], g_out.inputs["Surface"])

    # === Step 4: Translucent Fabric Material ===
    curtain_mat = bpy.data.materials.new("Arch_Fabric")
    curtain_mat.use_nodes = True
    ctree = curtain_mat.node_tree
    ctree.nodes.clear()

    c_out = ctree.nodes.new(type="ShaderNodeOutputMaterial")
    c_mix_final = ctree.nodes.new(type="ShaderNodeMixShader")
    c_mix_base = ctree.nodes.new(type="ShaderNodeMixShader")
    c_diffuse = ctree.nodes.new(type="ShaderNodeBsdfDiffuse")
    c_transluc = ctree.nodes.new(type="ShaderNodeBsdfTranslucent")
    c_transp = ctree.nodes.new(type="ShaderNodeBsdfTransparent")
    c_lp = ctree.nodes.new(type="ShaderNodeLightPath")
    c_math = ctree.nodes.new(type="ShaderNodeMath")
    
    fabric_color = (0.85, 0.8, 0.75, 1.0)
    c_diffuse.inputs["Color"].default_value = fabric_color
    c_transluc.inputs["Color"].default_value = fabric_color
    c_mix_base.inputs["Fac"].default_value = 0.5
    
    c_math.operation = 'MULTIPLY'
    c_math.inputs[1].default_value = 0.6  # Allows 60% of shadow rays through
    
    ctree.links.new(c_diffuse.outputs["BSDF"], c_mix_base.inputs[1])
    ctree.links.new(c_transluc.outputs["BSDF"], c_mix_base.inputs[2])
    ctree.links.new(c_lp.outputs["Is Shadow Ray"], c_math.inputs[0])
    ctree.links.new(c_math.outputs["Value"], c_mix_final.inputs["Fac"])
    ctree.links.new(c_mix_base.outputs["Shader"], c_mix_final.inputs[1])
    ctree.links.new(c_transp.outputs["BSDF"], c_mix_final.inputs[2])
    ctree.links.new(c_mix_final.outputs["Shader"], c_out.inputs["Surface"])

    # === Step 5: Spawn Demo Geometry ===
    # Glass Window Pane
    bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 1.5 * scale))
    glass_pane = bpy.context.active_object
    glass_pane.name = f"{object_name}_GlassPane"
    glass_pane.scale = (scale * 1.0, scale * 0.05, scale * 1.5)
    glass_pane.data.materials.append(glass_mat)

    # Fabric Curtain
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0] + 0.5 * scale, location[1] - 0.2 * scale, location[2] + 1.5 * scale))
    curtain = bpy.context.active_object
    curtain.name = f"{object_name}_Curtain"
    curtain.rotation_euler = (math.radians(90), 0, 0)
    curtain.scale = (scale * 0.8, scale * 1.5, scale * 1.0)
    curtain.data.materials.append(curtain_mat)

    # Subdivide curtain and add wave modifier for fabric folds
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=20)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    disp = curtain.modifiers.new(name="Wave", type='WAVE')
    disp.width = 0.4 * scale
    disp.height = 0.08 * scale
    disp.speed = 0.0
    
    # Apply shade smooth to both
    for obj in [glass_pane, curtain]:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()

    return f"Created Lighting Pipeline and '{object_name}' demo assets at {location}"

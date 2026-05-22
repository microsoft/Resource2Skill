def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricWaterPool",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.2, 0.5), # Base dark water color
    **kwargs,
) -> str:
    """
    Create a Procedural Volumetric Water Pool in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created water object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) deep water base color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # EEVEE setup for refraction (fails gracefully in Cycles)
    if hasattr(scene, 'eevee'):
        try:
            scene.eevee.use_ssr = True
            scene.eevee.use_ssr_refraction = True
        except AttributeError:
            pass # Handle API changes in newer Eevee versions

    # Secondary color for the wave peaks
    light_color = (0.1, 0.8, 0.7)

    # === Step 1: Create Container (Pool) ===
    # A dark container is needed so the water has an environment to refract
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.0 * scale, depth=1.0 * scale, location=location)
    container = bpy.context.active_object
    container.name = f"{object_name}_Container"
    bpy.ops.object.shade_smooth()
    
    # Clean up shading on flat faces
    edge_split_pool = container.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    edge_split_pool.split_angle = math.radians(45)
    
    # Cutter for the boolean hollow
    cutter_loc = (location[0], location[1], location[2] + 0.1 * scale)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.9 * scale, depth=1.0 * scale, location=cutter_loc)
    cutter = bpy.context.active_object
    cutter.name = f"{object_name}_Cutter"
    cutter.hide_viewport = True
    cutter.hide_render = True
    
    bool_mod = container.modifiers.new(name="Hollow", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'
    
    # Dark rock material for the pool
    mat_pool = bpy.data.materials.new(name=f"{object_name}_Pool_Mat")
    mat_pool.use_nodes = True
    pool_bsdf = mat_pool.node_tree.nodes.get("Principled BSDF")
    if pool_bsdf:
        pool_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
        pool_bsdf.inputs['Roughness'].default_value = 0.9
    container.data.materials.append(mat_pool)

    # === Step 2: Create Water Body ===
    # Fits exactly inside the boolean cut
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.9 * scale, depth=0.8 * scale, location=location)
    water = bpy.context.active_object
    water.name = object_name
    bpy.ops.object.shade_smooth()
    
    edge_split_water = water.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    edge_split_water.split_angle = math.radians(45)

    # === Step 3: Build Procedural Water Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Shader")
    mat.use_nodes = True
    mat.use_screen_refraction = True # Important for EEVEE
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'HASHED'
    water.data.materials.append(mat)

    tree = mat.node_tree
    tree.nodes.clear()

    # Create Nodes
    out_node = tree.nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    mix_node = tree.nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (600, 100)
    mix_node.inputs['Fac'].default_value = 0.5

    glass_node = tree.nodes.new(type='ShaderNodeBsdfGlass')
    glass_node.location = (400, 200)
    glass_node.inputs['IOR'].default_value = 1.333

    refraction_node = tree.nodes.new(type='ShaderNodeBsdfRefraction')
    refraction_node.location = (400, 0)
    refraction_node.inputs['IOR'].default_value = 1.333

    volume_node = tree.nodes.new(type='ShaderNodeVolumePrincipled')
    volume_node.location = (600, -200)
    # Scale density inversely to object size to maintain consistent darkness
    volume_node.inputs['Density'].default_value = 0.75 / max(scale, 0.01)
    volume_node.inputs['Anisotropy'].default_value = 0.8
    volume_node.inputs['Color'].default_value = (*material_color, 1.0)

    ramp_node = tree.nodes.new(type='ShaderNodeValToRGB')
    ramp_node.location = (100, 200)
    ramp_node.color_ramp.elements[0].position = 0.0
    ramp_node.color_ramp.elements[0].color = (*material_color, 1.0)
    ramp_node.color_ramp.elements[1].position = 1.0
    ramp_node.color_ramp.elements[1].color = (*light_color, 1.0)

    bump_node = tree.nodes.new(type='ShaderNodeBump')
    bump_node.location = (100, -100)
    bump_node.inputs['Strength'].default_value = 0.25

    noise_node = tree.nodes.new(type='ShaderNodeTexNoise')
    noise_node.name = "AnimatedNoise"
    noise_node.location = (-100, -100)
    noise_node.noise_dimensions = '4D'
    noise_node.inputs['Scale'].default_value = 3.0

    # Connect Nodes
    links = tree.links
    links.new(glass_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(refraction_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    links.new(volume_node.outputs['Volume'], out_node.inputs['Volume'])

    links.new(ramp_node.outputs['Color'], glass_node.inputs['Color'])
    links.new(ramp_node.outputs['Color'], refraction_node.inputs['Color'])
    
    links.new(noise_node.outputs['Fac'], ramp_node.inputs['Fac'])
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    
    links.new(bump_node.outputs['Normal'], glass_node.inputs['Normal'])
    links.new(bump_node.outputs['Normal'], refraction_node.inputs['Normal'])

    # === Step 4: Add Animation Driver ===
    # Drive the 'W' value of the 4D Noise to animate the water ripples over time
    try:
        driver_fcurve = tree.driver_add(f'nodes["{noise_node.name}"].inputs["W"].default_value')
        driver_fcurve.driver.expression = "frame / 500"
    except Exception as e:
        print(f"Notice: Could not attach driver to Noise Texture: {e}")

    # Parent water to container for easy moving
    water.parent = container
    cutter.parent = container

    return f"Created '{object_name}' inside a pool container at {location} with animated volumetric shader."

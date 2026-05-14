def create_magic_trail(
    scene_name: str = "Scene",
    object_name: str = "MagicTrail",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    color_start: tuple = (0.0, 0.8, 1.0, 1.0),
    color_mid: tuple = (0.8, 0.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a procedural, glowing particle trail tracing an animated spiral path.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) base world-space position.
        scale: Overall scale multiplier for the motion and fields.
        color_start: (R, G, B, A) color near the beginning of the trail.
        color_mid: (R, G, B, A) color towards the tail before it fades out.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Enable Eevee Bloom for the glowing "Halo" effect
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_bloom = True
        scene.eevee.bloom_intensity = 0.05
        scene.eevee.bloom_radius = 4.0

    # === Step 1: Create Instance Object (Particle Mesh) ===
    # Very low poly icosphere to keep viewport performant with 10k particles
    bpy.ops.mesh.primitive_icosphere_add(subdivisions=1, radius=0.1 * scale, location=(0, 0, -50))
    instance_obj = bpy.context.active_object
    instance_obj.name = f"{object_name}_Particle"
    instance_obj.hide_viewport = True
    instance_obj.hide_render = True

    # === Step 2: Build Material (Age-based fading emission) ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlowMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (600, 0)

    emission_node = nodes.new('ShaderNodeEmission')
    emission_node.location = (400, 0)
    emission_node.inputs['Strength'].default_value = 5.0
    links.new(emission_node.outputs[0], out_node.inputs[0])

    part_info = nodes.new('ShaderNodeParticleInfo')
    part_info.location = (-400, 0)

    math_div = nodes.new('ShaderNodeMath')
    math_div.operation = 'DIVIDE'
    math_div.location = (-200, 0)
    links.new(part_info.outputs['Age'], math_div.inputs[0])
    links.new(part_info.outputs['Lifetime'], math_div.inputs[1])

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 0)
    elements = color_ramp.color_ramp.elements
    
    # Base stops (Core white fading to black invisibility)
    elements[0].position = 0.0
    elements[0].color = (1.0, 1.0, 1.0, 1.0)
    elements[1].position = 1.0
    elements[1].color = (0.0, 0.0, 0.0, 1.0)
    
    # Mid stops for transition colors
    el1 = elements.new(0.1)
    el1.color = color_start
    el2 = elements.new(0.6)
    el2.color = color_mid
    
    links.new(math_div.outputs[0], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission_node.inputs['Color'])
    instance_obj.data.materials.append(mat)

    # === Step 3: Create Pivot for Spiral Motion ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    pivot_obj = bpy.context.active_object
    pivot_obj.name = f"{object_name}_Pivot"
    
    # Animate Pivot Rotation (Spins) and Z-location (Rises)
    pivot_obj.rotation_euler[2] = 0.0
    pivot_obj.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    pivot_obj.rotation_euler[2] = math.radians(360 * 2) # Spin 2 times over 250 frames
    pivot_obj.keyframe_insert(data_path="rotation_euler", index=2, frame=250)
    
    pivot_obj.location[2] = location[2]
    pivot_obj.keyframe_insert(data_path="location", index=2, frame=1)
    pivot_obj.location[2] = location[2] + (4.0 * scale)
    pivot_obj.keyframe_insert(data_path="location", index=2, frame=250)
    
    # Make motion linear for a smooth continuous trail
    if pivot_obj.animation_data and pivot_obj.animation_data.action:
        for fcurve in pivot_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    # === Step 4: Create Emitter ===
    emitter_loc = (location[0] + (2.0 * scale), location[1], location[2])
    bpy.ops.mesh.primitive_icosphere_add(radius=0.1 * scale, location=emitter_loc)
    emitter_obj = bpy.context.active_object
    emitter_obj.name = f"{object_name}_Emitter"
    
    # Orbiting logic: Parenting an offset object to a spinning pivot creates a circle
    emitter_obj.parent = pivot_obj
    
    # Hide the emitter geometry so only the particles render
    emitter_obj.show_instancer_for_render = False
    emitter_obj.show_instancer_for_viewport = False

    # === Step 5: Add Particle System ===
    bpy.context.view_layer.objects.active = emitter_obj
    bpy.ops.object.particle_system_add()
    psys = emitter_obj.particle_systems[0]
    pset = psys.settings
    pset.name = f"{object_name}_PSettings"
    
    pset.count = 10000
    pset.frame_start = 1
    pset.frame_end = 250
    pset.lifetime = 50
    
    # Motionless spawn parameters (forms solid trail behind moving object)
    pset.normal_factor = 0.0
    pset.factor_random = 0.0
    pset.effector_weights.gravity = 0.0
    
    # Render settings
    pset.render_type = 'OBJECT'
    pset.instance_object = instance_obj
    pset.particle_size = 1.0
    pset.size_random = 0.6

    # === Step 6: Create Organic Turbulence Force Field ===
    bpy.ops.object.effector_add(type='TURBULENCE', radius=1.0, location=location)
    turb_obj = bpy.context.active_object
    turb_obj.name = f"{object_name}_Turbulence"
    turb_obj.field.strength = 5.0 * scale
    turb_obj.field.size = 0.5 * scale
    turb_obj.field.noise = 1.0
    
    # Slowly move the turbulence upwards to make the noise evolve and undulate the smoke
    turb_obj.location[2] = location[2]
    turb_obj.keyframe_insert(data_path="location", index=2, frame=1)
    turb_obj.location[2] = location[2] + (6.0 * scale)
    turb_obj.keyframe_insert(data_path="location", index=2, frame=250)

    if turb_obj.animation_data and turb_obj.animation_data.action:
        for fcurve in turb_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    return f"Created '{object_name}' glowing particle trail system with animated spiral path and turbulence."

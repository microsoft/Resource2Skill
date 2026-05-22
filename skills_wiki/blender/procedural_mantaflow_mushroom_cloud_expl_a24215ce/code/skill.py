def create_object(
    scene_name: str = "Scene",
    object_name: str = "MushroomExplosion",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.15, 0.15),
    **kwargs,
) -> str:
    """
    Create a procedural Mantaflow Mushroom Cloud Explosion in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects (Domain, Crown, Stem).
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default 40x40x60m domain).
        material_color: (R, G, B) base color for the smoke in 0-1 range.
        **kwargs: Extensible parameters.
        
    Returns:
        Status string describing the generated system.
    """
    import bpy
    import bmesh

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. CREATE CROWN EMITTER (Hemisphere) ---
    bm_crown = bmesh.new()
    bmesh.ops.create_uvsphere(bm_crown, u_segments=16, v_segments=8, radius=6.0 * scale)
    # Delete bottom half to make a dome
    verts_to_del = [v for v in bm_crown.verts if v.co.z < 0.1]
    bmesh.ops.delete(bm_crown, geom=verts_to_del, context='VERTS')
    # Flatten dome and ensure normals point UP and OUT
    for v in bm_crown.verts:
        v.co.z *= 0.3
    for f in bm_crown.faces:
        if f.normal.z < 0:
            f.normal_flip()
            
    mesh_crown = bpy.data.meshes.new(f"{object_name}_CrownMesh")
    bm_crown.to_mesh(mesh_crown)
    bm_crown.free()
    
    crown = bpy.data.objects.new(f"{object_name}_Crown_Emitter", mesh_crown)
    crown.location = location
    scene.collection.objects.link(crown)
    crown.hide_render = True
    crown.display_type = 'WIRE'

    # --- 2. CREATE STEM EMITTER (Flat Circle) ---
    bm_stem = bmesh.new()
    bmesh.ops.create_circle(bm_stem, cap_ends=True, cap_tris=False, segments=16, radius=5.0 * scale)
    # Ensure normals point UP
    for f in bm_stem.faces:
        if f.normal.z < 0:
            f.normal_flip()
            
    mesh_stem = bpy.data.meshes.new(f"{object_name}_StemMesh")
    bm_stem.to_mesh(mesh_stem)
    bm_stem.free()
    
    stem = bpy.data.objects.new(f"{object_name}_Stem_Emitter", mesh_stem)
    stem.location = location
    scene.collection.objects.link(stem)
    stem.hide_render = True
    stem.display_type = 'WIRE'

    # --- 3. CREATE DOMAIN ---
    bm_dom = bmesh.new()
    bmesh.ops.create_cube(bm_dom, size=1.0)
    for v in bm_dom.verts:
        v.co.x *= 40.0 * scale
        v.co.y *= 40.0 * scale
        v.co.z *= 60.0 * scale
        
    mesh_dom = bpy.data.meshes.new(f"{object_name}_DomainMesh")
    bm_dom.to_mesh(mesh_dom)
    bm_dom.free()
    
    domain = bpy.data.objects.new(object_name, mesh_dom)
    # Shift domain up so emitters sit near the bottom
    domain.location = (location[0], location[1], location[2] + 25.0 * scale)
    scene.collection.objects.link(domain)

    # --- 4. PARTICLE SYSTEMS ---
    # Crown Particles
    mod_p_crown = crown.modifiers.new(name="CrownParticles", type='PARTICLE_SYSTEM')
    psys_crown = crown.particle_systems[0]
    pset_crown = psys_crown.settings
    pset_crown.count = 20000
    pset_crown.frame_start = 10
    pset_crown.frame_end = 16
    pset_crown.lifetime = 12
    pset_crown.lifetime_random = 1.0
    pset_crown.normal_factor = 85.0 * scale
    pset_crown.factor_random = 30.0 * scale
    pset_crown.effector_weights.gravity = 0.0
    pset_crown.render_type = 'NONE'
    pset_crown.show_unborn = False

    # Stem Particles
    mod_p_stem = stem.modifiers.new(name="StemParticles", type='PARTICLE_SYSTEM')
    psys_stem = stem.particle_systems[0]
    pset_stem = psys_stem.settings
    pset_stem.count = 10000
    pset_stem.frame_start = 12
    pset_stem.frame_end = 26
    pset_stem.lifetime = 20
    pset_stem.normal_factor = 55.0 * scale
    pset_stem.factor_random = 2.0 * scale
    pset_stem.effector_weights.gravity = 0.0
    pset_stem.render_type = 'NONE'
    pset_stem.show_unborn = False

    # --- 5. MANTAFLOW PHYSICS ---
    # Domain Settings
    mod_dom = domain.modifiers.new(name="FluidDomain", type='FLUID')
    mod_dom.fluid_type = 'DOMAIN'
    dom_set = mod_dom.domain_settings
    dom_set.domain_type = 'GAS'
    dom_set.resolution_max = 80  # Optimized for real-time preview playback
    dom_set.use_adaptive_time_steps = True
    dom_set.time_steps_max = 4
    dom_set.time_steps_min = 1
    dom_set.alpha = 1.0
    dom_set.beta = 0.05  # Heat: causes fire to dissipate quickly into smoke
    dom_set.vorticity = 0.2
    dom_set.cache_type = 'REPLAY'

    # Crown Flow (Fire & Smoke)
    mod_f_crown = crown.modifiers.new(name="FluidFlow", type='FLUID')
    mod_f_crown.fluid_type = 'FLOW'
    flow_c = mod_f_crown.flow_settings
    flow_c.flow_type = 'FIRE_AND_SMOKE'
    flow_c.flow_behavior = 'INFLOW'
    flow_c.subframes = 3
    flow_c.flow_source = 'PARTICLES'
    flow_c.particle_system = psys_crown
    flow_c.use_initial_velocity = True
    flow_c.velocity_factor = 1.0

    # Stem Flow (Smoke Only)
    mod_f_stem = stem.modifiers.new(name="FluidFlow", type='FLUID')
    mod_f_stem.fluid_type = 'FLOW'
    flow_s = mod_f_stem.flow_settings
    flow_s.flow_type = 'SMOKE'
    flow_s.flow_behavior = 'INFLOW'
    flow_s.subframes = 3
    flow_s.flow_source = 'PARTICLES'
    flow_s.particle_system = psys_stem
    flow_s.use_initial_velocity = True
    flow_s.velocity_factor = 1.0

    # --- 6. SHADER & MATERIAL ---
    mat = bpy.data.materials.new(name=f"{object_name}_Volumetric")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    vol_out = nodes.new('ShaderNodeOutputMaterial')
    vol_out.location = (300, 0)

    prin_vol = nodes.new('ShaderNodeVolumePrincipled')
    prin_vol.location = (0, 0)
    prin_vol.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)

    vol_info = nodes.new('ShaderNodeVolumeInfo')
    vol_info.location = (-600, 0)

    math_dens = nodes.new('ShaderNodeMath')
    math_dens.operation = 'MULTIPLY'
    math_dens.inputs[1].default_value = 6.0
    math_dens.location = (-300, 100)

    math_emis = nodes.new('ShaderNodeMath')
    math_emis.operation = 'MULTIPLY'
    math_emis.inputs[1].default_value = 10.0
    math_emis.location = (-300, -100)

    cramp = nodes.new('ShaderNodeValToRGB')
    cramp.location = (-300, -350)
    cramp.color_ramp.elements[0].position = 0.0
    cramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    cramp.color_ramp.elements[1].position = 0.1
    cramp.color_ramp.elements[1].color = (0.8, 0.1, 0.0, 1.0) # Core Red
    elem2 = cramp.color_ramp.elements.new(0.4)
    elem2.color = (1.0, 0.5, 0.0, 1.0) # Mid Orange
    elem3 = cramp.color_ramp.elements.new(0.8)
    elem3.color = (1.0, 0.9, 0.6, 1.0) # Hot White/Yellow

    links.new(vol_info.outputs['Density'], math_dens.inputs[0])
    links.new(math_dens.outputs[0], prin_vol.inputs['Density'])

    links.new(vol_info.outputs['Flame'], math_emis.inputs[0])
    links.new(math_emis.outputs[0], prin_vol.inputs['Emission Strength'])

    links.new(vol_info.outputs['Flame'], cramp.inputs[0])
    links.new(cramp.outputs[0], prin_vol.inputs['Emission Color'])

    links.new(prin_vol.outputs['Volume'], vol_out.inputs['Volume'])

    domain.data.materials.append(mat)

    # --- 7. COMPOSITING (GLARE) ---
    scene.use_nodes = True
    tree = scene.node_tree
    
    # Check if a Glare node already exists
    has_glare = any(n.type == 'GLARE' for n in tree.nodes)
    
    if not has_glare:
        try:
            rl = next(n for n in tree.nodes if n.type == 'R_LAYERS')
            comp = next(n for n in tree.nodes if n.type == 'COMPOSITE')
            
            glare = tree.nodes.new('CompositorNodeGlare')
            glare.glare_type = 'BLOOM'
            glare.mix = -0.8
            glare.threshold = 0.5
            
            tree.links.new(rl.outputs['Image'], glare.inputs['Image'])
            tree.links.new(glare.outputs['Image'], comp.inputs['Image'])
        except StopIteration:
            pass # Standard render nodes not found, gracefully skip compositing

    return f"Created '{object_name}' (Fluid Domain) and emitters at {location}. Press Play (Spacebar) to simulate the explosion."

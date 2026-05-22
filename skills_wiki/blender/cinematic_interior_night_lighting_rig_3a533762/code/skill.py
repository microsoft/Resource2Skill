def create_cinematic_night_lights(
    scene_name: str = "Scene",
    rig_name: str = "NightLightingRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    moon_color: tuple = (0.15, 0.35, 0.8),
    warm_color: tuple = (1.0, 0.6, 0.2),
    **kwargs,
) -> str:
    """
    Create a Cinematic Interior Night Lighting Rig in the active scene.

    Args:
        scene_name: Name of the target scene.
        rig_name: Base name for the created objects and collection.
        location: (x, y, z) base world-space position.
        scale: Uniform scale factor for the rig.
        moon_color: (R, G, B) color for the fill moon light.
        warm_color: (R, G, B) color for the warm key/accent lights.

    Returns:
        Status string detailing the created rig.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.render.engine = 'CYCLES'  # Required for accurate spread and light paths
    
    # Create a dedicated collection
    rig_coll = bpy.data.collections.get(rig_name)
    if not rig_coll:
        rig_coll = bpy.data.collections.new(rig_name)
        scene.collection.children.link(rig_coll)
        
    base_loc = Vector(location)
    
    # ==========================================
    # 1. FILL LIGHT (Soft Moonlight)
    # ==========================================
    sun_data = bpy.data.lights.new(name=f"{rig_name}_Moonlight", type='SUN')
    sun_data.color = moon_color
    sun_data.energy = 0.5
    sun_data.angle = math.radians(5.0) # Soft shadows
    sun_obj = bpy.data.objects.new(name=f"{rig_name}_Moonlight", object_data=sun_data)
    # Angled to simulate moonlight shining through a window
    sun_obj.rotation_euler = (math.radians(45), math.radians(0), math.radians(45))
    rig_coll.objects.link(sun_obj)
    
    # ==========================================
    # 2. KEY LIGHT (Pendant Lamp Setup)
    # ==========================================
    pendant_z = 2.5 * scale
    
    # A. Pendant Shade Mesh
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.4*scale, depth=0.3*scale, location=base_loc + Vector((0, 0, pendant_z)))
    pendant_mesh = bpy.context.active_object
    pendant_mesh.name = f"{rig_name}_PendantShade"
    
    # Remove bottom face to make a shell
    bm = bmesh.new()
    bm.from_mesh(pendant_mesh.data)
    bottom_faces = [f for f in bm.faces if f.normal.z < -0.9]
    bmesh.ops.delete(bm, geom=bottom_faces, context='FACES')
    bm.to_mesh(pendant_mesh.data)
    bm.free()
    
    # Solidify modifier
    solid_mod = pendant_mesh.modifiers.new(name="Solidify", type='SOLIDIFY')
    solid_mod.thickness = 0.02 * scale
    
    # B. Frosted Glass Material with "Light Path" Shadow Trick
    mat_shade = bpy.data.materials.new(name=f"{rig_name}_FrostedGlass")
    mat_shade.use_nodes = True
    tree = mat_shade.node_tree
    nodes = tree.nodes
    links = tree.links
    for n in nodes: nodes.remove(n)
        
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (300, 0)
    mix_node = nodes.new('ShaderNodeMixShader')
    mix_node.location = (100, 0)
    transp_node = nodes.new('ShaderNodeBsdfTransparent')
    transp_node.location = (-100, -100)
    princ_node = nodes.new('ShaderNodeBsdfPrincipled')
    princ_node.location = (-100, 100)
    princ_node.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
    princ_node.inputs['Roughness'].default_value = 0.8 # Frosted look
    
    lpath_node = nodes.new('ShaderNodeLightPath')
    lpath_node.location = (-100, 300)
    
    # If Shadow Ray is True, evaluate as Transparent so light passes through
    links.new(lpath_node.outputs['Is Shadow Ray'], mix_node.inputs['Fac'])
    links.new(princ_node.outputs['BSDF'], mix_node.inputs[1]) # Top socket (Not Shadow)
    links.new(transp_node.outputs['BSDF'], mix_node.inputs[2]) # Bottom socket (Is Shadow)
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    pendant_mesh.data.materials.append(mat_shade)
    
    # C. Emissive Bulb Mesh (for visible glow)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08*scale, location=base_loc + Vector((0, 0, pendant_z - 0.05*scale)))
    bulb_mesh = bpy.context.active_object
    bulb_mesh.name = f"{rig_name}_Bulb"
    
    mat_bulb = bpy.data.materials.new(name=f"{rig_name}_BulbMat")
    mat_bulb.use_nodes = True
    for n in mat_bulb.node_tree.nodes: mat_bulb.node_tree.nodes.remove(n)
    bulb_out = mat_bulb.node_tree.nodes.new('ShaderNodeOutputMaterial')
    bulb_out.location = (200, 0)
    bulb_em = mat_bulb.node_tree.nodes.new('ShaderNodeEmission')
    bulb_em.location = (0, 0)
    bulb_em.inputs['Color'].default_value = warm_color + (1.0,)
    bulb_em.inputs['Strength'].default_value = 50.0
    mat_bulb.node_tree.links.new(bulb_em.outputs['Emission'], bulb_out.inputs['Surface'])
    bulb_mesh.data.materials.append(mat_bulb)
    
    # D. Key Light Area Lamp (Creates the actual illumination)
    area_data = bpy.data.lights.new(name=f"{rig_name}_PendantLight", type='AREA')
    area_data.shape = 'DISK'
    area_data.size = 0.25 * scale
    area_data.color = warm_color
    area_data.energy = 150.0 * (scale**2)
    area_data.spread = math.radians(120) # Crucial for shaping the cone
    area_obj = bpy.data.objects.new(name=f"{rig_name}_PendantLight", object_data=area_data)
    area_obj.location = base_loc + Vector((0, 0, pendant_z - 0.1*scale))
    # Point down (default is down, no rotation needed)
    
    # Organize into collection
    for obj in [pendant_mesh, bulb_mesh, area_obj]:
        for coll in obj.users_collection: coll.objects.unlink(obj)
        rig_coll.objects.link(obj)
        
    # ==========================================
    # 3. ACCENT LIGHT (Cove / Wall Washer)
    # ==========================================
    cove_data = bpy.data.lights.new(name=f"{rig_name}_CoveAccent", type='AREA')
    cove_data.shape = 'RECTANGLE'
    cove_data.size = 4.0 * scale
    cove_data.size_y = 0.1 * scale
    cove_data.color = warm_color
    cove_data.energy = 50.0 * (scale**2)
    cove_data.spread = math.radians(160)
    cove_obj = bpy.data.objects.new(name=f"{rig_name}_CoveAccent", object_data=cove_data)
    cove_obj.location = base_loc + Vector((-2*scale, 2*scale, 3*scale))
    cove_obj.rotation_euler = (math.radians(180), 0, 0) # Pointing UP
    rig_coll.objects.link(cove_obj)
    
    # ==========================================
    # 4. COMPOSITOR SETUP (Glare & Vignette)
    # ==========================================
    scene.use_nodes = True
    ctree = scene.node_tree
    
    # Find or create Render Layers and Composite nodes
    rl_node = next((n for n in ctree.nodes if n.type == 'R_LAYERS'), None)
    comp_node = next((n for n in ctree.nodes if n.type == 'COMPOSITE'), None)
    if not rl_node:
        rl_node = ctree.nodes.new('CompositorNodeRLayers')
        rl_node.location = (-400, 0)
    if not comp_node:
        comp_node = ctree.nodes.new('CompositorNodeComposite')
        comp_node.location = (800, 0)
        
    glare_node = ctree.nodes.new('CompositorNodeGlare')
    glare_node.location = (0, 0)
    glare_node.glare_type = 'FOG_GLOW'
    glare_node.mix = -0.8 
    glare_node.threshold = 1.0
    
    mask_node = ctree.nodes.new('CompositorNodeBoxMask')
    mask_node.location = (0, -200)
    mask_node.x = 0.5
    mask_node.y = 0.5
    mask_node.width = 0.8
    mask_node.height = 0.8
    
    blur_node = ctree.nodes.new('CompositorNodeBlur')
    blur_node.location = (200, -200)
    blur_node.use_relative = True
    blur_node.size_x = 20.0
    blur_node.size_y = 20.0
    
    mix_node = ctree.nodes.new('CompositorNodeMixRGB')
    mix_node.location = (400, 0)
    mix_node.blend_type = 'MULTIPLY'
    mix_node.inputs['Fac'].default_value = 0.8 # Vignette opacity
    
    try:
        ctree.links.new(rl_node.outputs['Image'], glare_node.inputs['Image'])
        ctree.links.new(mask_node.outputs['Mask'], blur_node.inputs['Image'])
        ctree.links.new(glare_node.outputs['Image'], mix_node.inputs[1])
        ctree.links.new(blur_node.outputs['Image'], mix_node.inputs[2])
        ctree.links.new(mix_node.outputs['Image'], comp_node.inputs['Image'])
    except Exception as e:
        print(f"Compositor links warning (safe to ignore if using non-standard Blender version): {e}")

    return f"Created '{rig_name}' at {location}. Includes Moonlight (Sun), Key Light (Pendant w/ Light Path trick), Cove Light (Area), and Compositing nodes."

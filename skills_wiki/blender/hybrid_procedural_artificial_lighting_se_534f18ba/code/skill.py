def create_object(
    scene_name: str = "Scene",
    object_name: str = "HybridLightRig",
    location: tuple = (0.0, 0.0, 3.0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.85, 0.6),
    **kwargs,
) -> str:
    """
    Create a Hybrid Procedural & Artificial Lighting Setup.
    Sets up a Nishita sky and creates a physical drop-lamp with a noise-free emissive bulb.

    Args:
        scene_name: Name of the active scene.
        object_name: Name of the light fixture object.
        location: (x, y, z) position (intended for ceilings).
        scale: Uniform scale.
        material_color: (R, G, B) color for both the bulb emission and the light source.
        **kwargs: 
            sun_elevation (float): Angle of the sun in degrees (default: 15.0).
            sun_rotation (float): Rotation of the sun in degrees (default: 135.0).
            light_energy (float): Wattage of the indoor point light (default: 100.0).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Procedural Environment Sky ---
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("Procedural_World")
        scene.world = world
    
    world.use_nodes = True
    w_tree = world.node_tree
    
    # Retrieve or create nodes
    sky_node = next((n for n in w_tree.nodes if n.type == 'TEX_SKY'), None)
    if not sky_node:
        sky_node = w_tree.nodes.new(type='ShaderNodeTexSky')
        sky_node.location = (-300, 0)
        
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(kwargs.get('sun_elevation', 15.0))
    sky_node.sun_rotation = math.radians(kwargs.get('sun_rotation', 135.0))
    
    bg_node = next((n for n in w_tree.nodes if n.type == 'BACKGROUND'), None)
    if not bg_node:
        bg_node = w_tree.nodes.new(type='ShaderNodeBackground')
        bg_node.location = (0, 0)
        
    out_node = next((n for n in w_tree.nodes if n.type == 'OUTPUT_WORLD'), None)
    if not out_node:
        out_node = w_tree.nodes.new(type='ShaderNodeOutputWorld')
        out_node.location = (200, 0)
        
    w_tree.links.new(sky_node.outputs['Color'], bg_node.inputs['Color'])
    w_tree.links.new(bg_node.outputs['Background'], out_node.inputs['Surface'])


    # --- 2. Lamp Geometry ---
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base (Ceiling mount)
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=0.1, radius2=0.1, depth=0.05)
    
    # Drop Cord
    cord = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=0.01, radius2=0.01, depth=1.0)
    bmesh.ops.translate(bm, verts=cord['verts'], vec=(0.0, 0.0, -0.5))
    
    # Bulb
    bulb = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.15)
    bmesh.ops.translate(bm, verts=bulb['verts'], vec=(0.0, 0.0, -1.0))
    
    bm.to_mesh(mesh)
    bm.free()


    # --- 3. Analytic Point Light ---
    light_data = bpy.data.lights.new(name=f"{object_name}_Point", type='POINT')
    light_data.color = material_color
    light_data.energy = kwargs.get('light_energy', 100.0)
    light_data.shadow_soft_size = 0.15 # Match bulb radius for soft, realistic shadows
    
    light_obj = bpy.data.objects.new(f"{object_name}_Light", light_data)
    scene.collection.objects.link(light_obj)
    
    # Parent light to fixture and position inside the bulb
    light_obj.parent = obj
    light_obj.location = (0.0, 0.0, -1.0)


    # --- 4. Materials ---
    # Material A: Dark Fixture Metal
    mat_fixture = bpy.data.materials.new(name=f"{object_name}_FixtureMat")
    mat_fixture.use_nodes = True
    bsdf_fix = next((n for n in mat_fixture.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf_fix:
        bsdf_fix.inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1.0)
        if "Metallic" in bsdf_fix.inputs:
            bsdf_fix.inputs["Metallic"].default_value = 1.0
        if "Roughness" in bsdf_fix.inputs:
            bsdf_fix.inputs["Roughness"].default_value = 0.3

    # Material B: Emissive Bulb (Shadow-transparent trick)
    mat_bulb = bpy.data.materials.new(name=f"{object_name}_BulbMat")
    mat_bulb.use_nodes = True
    mat_bulb.blend_method = 'BLEND'  # Ensure Eevee transparency works
    mat_bulb.shadow_method = 'NONE'  # Stop Eevee from casting mesh shadows
    
    m_tree = mat_bulb.node_tree
    for n in m_tree.nodes:
        m_tree.nodes.remove(n)
        
    node_emit = m_tree.nodes.new('ShaderNodeEmission')
    node_emit.inputs['Color'].default_value = (*material_color, 1.0)
    node_emit.inputs['Strength'].default_value = 10.0
    node_emit.location = (-200, 100)
    
    node_transp = m_tree.nodes.new('ShaderNodeBsdfTransparent')
    node_transp.location = (-200, -100)
    
    node_mix = m_tree.nodes.new('ShaderNodeMixShader')
    node_mix.location = (0, 0)
    
    node_lp = m_tree.nodes.new('ShaderNodeLightPath')
    node_lp.location = (-200, 300)
    
    node_out = m_tree.nodes.new('ShaderNodeOutputMaterial')
    node_out.location = (200, 0)
    
    # If a shadow ray hits the bulb, make it transparent so the inner Point Light shines through
    m_tree.links.new(node_lp.outputs['Is Shadow Ray'], node_mix.inputs['Fac'])
    m_tree.links.new(node_emit.outputs['Emission'], node_mix.inputs[1])
    m_tree.links.new(node_transp.outputs['BSDF'], node_mix.inputs[2])
    m_tree.links.new(node_mix.outputs['Shader'], node_out.inputs['Surface'])

    # Append materials to object
    obj.data.materials.append(mat_fixture) # Index 0
    obj.data.materials.append(mat_bulb)    # Index 1

    # Assign materials to faces based on Z height (bulb is at Z = -1.0)
    bm_mat = bmesh.new()
    bm_mat.from_mesh(mesh)
    for face in bm_mat.faces:
        if face.calc_center_median().z < -0.8:
            face.material_index = 1
        else:
            face.material_index = 0
    bm_mat.to_mesh(mesh)
    bm_mat.free()


    # --- 5. Finalize ---
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created hybrid lighting rig '{object_name}' (Nishita Sky + Physical Lamp) at {location}."

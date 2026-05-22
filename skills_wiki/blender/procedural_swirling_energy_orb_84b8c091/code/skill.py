def create_magic_energy_orb(
    scene_name: str = "Scene",
    object_name: str = "EnergyOrb",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    core_color: tuple = (1.0, 1.0, 0.8, 1.0),
    edge_color: tuple = (0.1, 0.8, 0.3, 1.0),
    point_density: float = 15000.0,
    **kwargs,
) -> str:
    """
    Create a Procedural Swirling Energy Orb in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created orb.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        core_color: (R, G, B, A) color of the hot center.
        edge_color: (R, G, B, A) color of the swirling corona.
        point_density: Density of the point cloud (higher = more solid but slower).
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_icosphere_add(subdivisions=4, radius=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Enable Bloom for Eevee to make the glow visible
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_bloom = True

    # === Step 2: Build the Volumetric Emission Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlowMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'  # Crucial for transparency in Eevee
    mat.shadow_method = 'NONE'
    obj.data.materials.append(mat)

    m_nodes = mat.node_tree.nodes
    m_links = mat.node_tree.links
    m_nodes.clear()

    # Core Output and Shaders
    out_node = m_nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    mix_node = m_nodes.new('ShaderNodeMixShader')
    mix_node.location = (600, 0)
    m_links.new(mix_node.outputs[0], out_node.inputs[0])

    trans_node = m_nodes.new('ShaderNodeBsdfTransparent')
    trans_node.location = (400, -100)
    m_links.new(trans_node.outputs[0], mix_node.inputs[1])  # Top slot (Factor=0)

    em_node = m_nodes.new('ShaderNodeEmission')
    em_node.location = (400, 100)
    m_links.new(em_node.outputs[0], mix_node.inputs[2])     # Bottom slot (Factor=1)

    # Calculate distance from center
    tex_coord = m_nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)

    len_node = m_nodes.new('ShaderNodeVectorMath')
    len_node.math_type = 'LENGTH'
    len_node.location = (-200, 0)
    m_links.new(tex_coord.outputs['Object'], len_node.inputs[0])

    # Falloff: 1.0 at Center, 0.0 at Edges
    map_falloff = m_nodes.new('ShaderNodeMapRange')
    map_falloff.location = (0, 0)
    map_falloff.inputs[1].default_value = 0.0  # From Min
    map_falloff.inputs[2].default_value = 1.2  # From Max (allows for noise offset)
    map_falloff.inputs[3].default_value = 1.0  # To Min (Center strength)
    map_falloff.inputs[4].default_value = 0.0  # To Max (Edge strength)
    m_links.new(len_node.outputs.get('Value') or len_node.outputs[0], map_falloff.inputs[0])

    # Drive Transparency Mix
    m_links.new(map_falloff.outputs[0], mix_node.inputs[0])

    # Color Ramp
    cr_color = m_nodes.new('ShaderNodeValToRGB')
    cr_color.location = (200, 200)
    cr_color.color_ramp.elements[0].position = 0.0
    cr_color.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0) # Void
    cr_color.color_ramp.elements[1].position = 0.8
    cr_color.color_ramp.elements[1].color = core_color           # Core
    
    cr_mid = cr_color.color_ramp.elements.new(0.4)
    cr_mid.color = edge_color                                    # Corona
    
    m_links.new(map_falloff.outputs[0], cr_color.inputs[0])
    m_links.new(cr_color.outputs[0], em_node.inputs['Color'])

    # Multiply Strength
    mult_str = m_nodes.new('ShaderNodeMath')
    mult_str.operation = 'MULTIPLY'
    mult_str.inputs[1].default_value = 30.0
    mult_str.location = (200, 50)
    m_links.new(map_falloff.outputs[0], mult_str.inputs[0])
    m_links.new(mult_str.outputs[0], em_node.inputs['Strength'])

    # === Step 3: Build Geometry Nodes for Turbulence & Volume ===
    gn_mod = obj.modifiers.new(name="MagicOrb_GeoNodes", type='NODES')
    gn_tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    gn_mod.node_group = gn_tree

    g_nodes = gn_tree.nodes
    g_links = gn_tree.links

    gn_in = g_nodes.new('NodeGroupInput')
    gn_out = g_nodes.new('NodeGroupOutput')

    # Interface compatibility across Blender versions
    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.inputs.new('NodeSocketGeometry', 'Geometry')
        gn_tree.outputs.new('NodeSocketGeometry', 'Geometry')

    # 1. Distribute points
    dist_pts = g_nodes.new('GeometryNodeDistributePointsOnFaces')
    dist_pts.inputs['Density'].default_value = point_density

    # 2. Push points inwards to fill volume
    set_pos_vol = g_nodes.new('GeometryNodeSetPosition')
    norm_node = g_nodes.new('GeometryNodeInputNormal')
    
    rand_val = g_nodes.new('FunctionNodeRandomValue')
    rand_val.data_type = 'FLOAT'
    rand_val.inputs['Min'].default_value = -1.0
    rand_val.inputs['Max'].default_value = 0.0
    
    scale_norm = g_nodes.new('ShaderNodeVectorMath')
    scale_norm.math_type = 'SCALE'
    
    g_links.new(norm_node.outputs[0], scale_norm.inputs[0])
    g_links.new(rand_val.outputs.get('Value') or rand_val.outputs[1], scale_norm.inputs['Scale'])
    g_links.new(scale_norm.outputs[0], set_pos_vol.inputs['Offset'])

    # 3. Add Swirling Turbulence (4D Noise)
    set_pos_turb = g_nodes.new('GeometryNodeSetPosition')
    pos_node = g_nodes.new('GeometryNodeInputPosition')
    
    noise_tex = g_nodes.new('ShaderNodeTexNoise')
    noise_tex.noise_dimensions = '4D'
    noise_tex.inputs['Scale'].default_value = 2.5
    
    scene_time = g_nodes.new('GeometryNodeInputSceneTime')
    time_scale = g_nodes.new('ShaderNodeMath')
    time_scale.operation = 'MULTIPLY'
    time_scale.inputs[1].default_value = 0.3
    
    g_links.new(scene_time.outputs.get('Seconds') or scene_time.outputs[0], time_scale.inputs[0])
    g_links.new(time_scale.outputs[0], noise_tex.inputs['W'])
    g_links.new(pos_node.outputs[0], noise_tex.inputs['Vector'])
    
    sub_half = g_nodes.new('ShaderNodeVectorMath')
    sub_half.math_type = 'SUBTRACT'
    sub_half.inputs[1].default_value = (0.5, 0.5, 0.5)
    g_links.new(noise_tex.outputs.get('Color') or noise_tex.outputs[1], sub_half.inputs[0])
    
    turb_scale = g_nodes.new('ShaderNodeVectorMath')
    turb_scale.math_type = 'SCALE'
    turb_scale.inputs['Scale'].default_value = 0.8
    g_links.new(sub_half.outputs[0], turb_scale.inputs[0])
    
    g_links.new(turb_scale.outputs[0], set_pos_turb.inputs['Offset'])

    # 4. Instance micro-spheres
    inst_pts = g_nodes.new('GeometryNodeInstanceOnPoints')
    ico_inst = g_nodes.new('GeometryNodeMeshIcoSphere')
    ico_inst.inputs['Radius'].default_value = 0.008
    ico_inst.inputs['Subdivisions'].default_value = 1
    g_links.new(ico_inst.outputs[0], inst_pts.inputs['Instance'])

    # 5. Apply Material
    set_mat_node = g_nodes.new('GeometryNodeSetMaterial')
    set_mat_node.inputs['Material'].default_value = mat

    # Connect Main Flow
    g_links.new(gn_in.outputs[0], dist_pts.inputs[0])
    g_links.new(dist_pts.outputs[0], set_pos_vol.inputs[0])
    g_links.new(set_pos_vol.outputs[0], set_pos_turb.inputs[0])
    g_links.new(set_pos_turb.outputs[0], inst_pts.inputs[0])
    g_links.new(inst_pts.outputs[0], set_mat_node.inputs[0])
    g_links.new(set_mat_node.outputs[0], gn_out.inputs[0])

    return f"Created '{obj.name}' at {location}. Press Play/Spacebar to see the procedural turbulence animate!"

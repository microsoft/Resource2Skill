def create_anime_grass_field(
    scene_name: str = "Scene",
    object_name: str = "AnimeGrassField",
    location: tuple = (0, 0, 0),
    scale: float = 10.0,
    base_color: tuple = (0.3, 0.8, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural Anime Cel-Shaded Grass Field with wind dynamics.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated terrain object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor of the terrain.
        base_color: (R, G, B) primary light-green grass color.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Enforce EEVEE (Required for Shader to RGB)
    if bpy.app.version >= (4, 2, 0):
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'

    # Ensure a Sun light exists for the cel-shading to react to
    if not any(l.type == 'SUN' for l in bpy.data.lights):
        bpy.ops.object.light_add(type='SUN', location=(location[0]+5, location[1]-5, location[2]+10))
        sun = bpy.context.active_object
        sun.data.energy = 2.0
        sun.data.angle = 0.1
        sun.rotation_euler = (0.8, 0.3, 0.5)

    # 2. Create the Base Grass Blade Mesh
    blade_mesh = bpy.data.meshes.new("AnimeGrassBlade")
    blade_obj = bpy.data.objects.new("AnimeGrassBlade", blade_mesh)
    scene.collection.objects.link(blade_obj)
    
    bm = bmesh.new()
    v1 = bm.verts.new((-0.03, 0, 0))
    v2 = bm.verts.new((0.03, 0, 0))
    v3 = bm.verts.new((0, 0, 0.8)) # Tapered to a point
    bm.faces.new((v1, v2, v3))
    bm.to_mesh(blade_mesh)
    bm.free()
    
    blade_obj.hide_viewport = True
    blade_obj.hide_render = True

    # 3. Create Terrain Plane
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    terrain = bpy.context.active_object
    terrain.name = object_name
    terrain.scale = (scale, scale, 1)

    # 4. Materials Setup
    # 4a. Terrain Dirt Material
    dirt_mat = bpy.data.materials.new(name="AnimeDirt_Mat")
    dirt_mat.use_nodes = True
    d_nodes = dirt_mat.node_tree.nodes
    d_links = dirt_mat.node_tree.links
    d_nodes.clear()
    
    d_out = d_nodes.new("ShaderNodeOutputMaterial")
    d_diffuse = d_nodes.new("ShaderNodeBsdfDiffuse")
    d_s2r = d_nodes.new("ShaderNodeShaderToRGB")
    d_ramp = d_nodes.new("ShaderNodeValToRGB")
    d_ramp.color_ramp.interpolation = 'CONSTANT'
    d_ramp.color_ramp.elements[0].position = 0.3
    d_ramp.color_ramp.elements[0].color = (0.2, 0.15, 0.1, 1)
    d_ramp.color_ramp.elements[1].position = 0.35
    d_ramp.color_ramp.elements[1].color = (0.3, 0.25, 0.18, 1)
    d_emission = d_nodes.new("ShaderNodeEmission")
    
    d_links.new(d_diffuse.outputs['BSDF'], d_s2r.inputs['Shader'])
    d_links.new(d_s2r.outputs['Color'], d_ramp.inputs['Fac'])
    d_links.new(d_ramp.outputs['Color'], d_emission.inputs['Color'])
    d_links.new(d_emission.outputs['Emission'], d_out.inputs['Surface'])
    
    terrain.data.materials.append(dirt_mat)

    # 4b. Anime Grass Material (The Secret Sauce)
    mat = bpy.data.materials.new(name="AnimeGrass_Mat")
    mat.use_nodes = True
    mat.shadow_method = 'NONE' # Disable self-shadowing noise
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    color_ramp = nodes.new("ShaderNodeValToRGB")
    color_ramp.color_ramp.interpolation = 'CONSTANT'
    color_ramp.color_ramp.elements[0].position = 0.45
    color_ramp.color_ramp.elements[0].color = (base_color[0]*0.5, base_color[1]*0.5, base_color[2]*0.5, 1) # Shadow
    color_ramp.color_ramp.elements[1].position = 0.5
    color_ramp.color_ramp.elements[1].color = (base_color[0], base_color[1], base_color[2], 1) # Highlight
    
    shader_to_rgb = nodes.new("ShaderNodeShaderToRGB")
    diffuse = nodes.new("ShaderNodeBsdfDiffuse")
    
    # Procedural "Blobby" Normal Logic (replaces complex Data Transfer modifier)
    geom_node = nodes.new("ShaderNodeNewGeometry")
    noise_normal = nodes.new("ShaderNodeTexNoise")
    noise_normal.inputs['Scale'].default_value = 0.8
    vec_add = nodes.new("ShaderNodeVectorMath")
    vec_add.operation = 'ADD'
    vec_add.inputs[1].default_value = (0, 0, 1.5) # Force normal bias upwards
    vec_norm = nodes.new("ShaderNodeVectorMath")
    vec_norm.operation = 'NORMALIZE'
    
    links.new(geom_node.outputs['Position'], noise_normal.inputs['Vector'])
    links.new(noise_normal.outputs['Color'], vec_add.inputs[0])
    links.new(vec_add.outputs[0], vec_norm.inputs[0])
    links.new(vec_norm.outputs[0], diffuse.inputs['Normal'])
    
    links.new(diffuse.outputs['BSDF'], shader_to_rgb.inputs['Shader'])
    links.new(shader_to_rgb.outputs['Color'], color_ramp.inputs['Fac'])
    
    # Apply Wind Shadow Overlay
    attr = nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "WindMask"
    attr.attribute_type = 'INSTANCER'
    
    if bpy.app.version >= (3, 4, 0):
        mix_wind = nodes.new("ShaderNodeMix")
        mix_wind.data_type = 'RGBA'
        mix_wind.blend_type = 'MULTIPLY'
        c1, c2, fac = mix_wind.inputs['A'], mix_wind.inputs['B'], mix_wind.inputs['Factor']
        out_col = mix_wind.outputs['Result']
    else:
        mix_wind = nodes.new("ShaderNodeMixRGB")
        mix_wind.blend_type = 'MULTIPLY'
        c1, c2, fac = mix_wind.inputs['Color1'], mix_wind.inputs['Color2'], mix_wind.inputs['Fac']
        out_col = mix_wind.outputs['Color']
        
    c2.default_value = (0.6, 0.7, 0.6, 1.0) # Darkening factor when wind hits
    links.new(attr.outputs['Fac'], fac)
    links.new(color_ramp.outputs['Color'], c1)
    links.new(out_col, emission.inputs['Color'])
    links.new(emission.outputs['Emission'], out_node.inputs['Surface'])
    
    blade_obj.data.materials.append(mat)

    # 5. Geometry Nodes Configuration
    gn_mod = terrain.modifiers.new(name="AnimeGrassScatter", type='NODES')
    gn_tree = bpy.data.node_groups.new(name="AnimeGrassTree", type='GeometryNodeTree')
    gn_mod.node_group = gn_tree

    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.inputs.new('NodeSocketGeometry', "Geometry")
        gn_tree.outputs.new('NodeSocketGeometry', "Geometry")

    gn_nodes = gn_tree.nodes
    gn_links = gn_tree.links

    group_in = gn_nodes.new("NodeGroupInput")
    group_out = gn_nodes.new("NodeGroupOutput")

    # Procedural Dirt Path Mask
    path_noise = gn_nodes.new("ShaderNodeTexNoise")
    path_noise.inputs['Scale'].default_value = 0.8
    path_ramp = gn_nodes.new("ShaderNodeValToRGB")
    path_ramp.color_ramp.elements[0].position = 0.4
    path_ramp.color_ramp.elements[1].position = 0.55

    distribute = gn_nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute.inputs['Density'].default_value = 10000.0 # Dense anime grass
    
    gn_links.new(path_noise.outputs['Fac'], path_ramp.inputs['Fac'])
    gn_links.new(path_ramp.outputs['Color'], distribute.inputs['Density Factor'])

    instance_pts = gn_nodes.new("GeometryNodeInstanceOnPoints")
    obj_info = gn_nodes.new("GeometryNodeObjectInfo")
    obj_info.inputs['Object'].default_value = blade_obj
    
    # Random Sizing, tapered by path
    rand_scale = gn_nodes.new("FunctionNodeRandomValue")
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.4
    rand_scale.inputs['Max'].default_value = 1.0
    
    scale_mult = gn_nodes.new("ShaderNodeMath")
    scale_mult.operation = 'MULTIPLY'
    gn_links.new(rand_scale.outputs['Value'], scale_mult.inputs[0])
    gn_links.new(path_ramp.outputs['Color'], scale_mult.inputs[1])
    gn_links.new(scale_mult.outputs[0], instance_pts.inputs['Scale'])

    # Orient to Terrain Normal
    normal_node = gn_nodes.new("GeometryNodeInputNormal")
    align_euler = gn_nodes.new("FunctionNodeAlignEulerToVector")
    align_euler.axis = 'Z'
    gn_links.new(normal_node.outputs['Normal'], align_euler.inputs['Vector'])
    gn_links.new(align_euler.outputs['Rotation'], instance_pts.inputs['Rotation'])

    # Animated Wind Rotation
    time_node = gn_nodes.new("GeometryNodeInputSceneTime")
    math_time = gn_nodes.new("ShaderNodeMath")
    math_time.operation = 'MULTIPLY'
    math_time.inputs[1].default_value = 0.8 # Wind Speed
    gn_links.new(time_node.outputs['Seconds'], math_time.inputs[0])

    wind_noise = gn_nodes.new("ShaderNodeTexNoise")
    wind_noise.noise_dimensions = '4D'
    wind_noise.inputs['Scale'].default_value = 1.5
    gn_links.new(math_time.outputs[0], wind_noise.inputs['W'])
    
    # Store wind intensity for shader darkening
    store_attr = gn_nodes.new("GeometryNodeStoreNamedAttribute")
    store_attr.inputs['Name'].default_value = "WindMask"
    store_attr.data_type = 'FLOAT'
    store_attr.domain = 'INSTANCE'
    gn_links.new(wind_noise.outputs['Fac'], store_attr.inputs['Value'])

    wind_map = gn_nodes.new("ShaderNodeMapRange")
    wind_map.inputs[1].default_value = 0.2
    wind_map.inputs[2].default_value = 0.8
    wind_map.inputs[3].default_value = -0.3
    wind_map.inputs[4].default_value = 0.3
    gn_links.new(wind_noise.outputs['Fac'], wind_map.inputs['Value'])

    rand_rot_z = gn_nodes.new("FunctionNodeRandomValue")
    rand_rot_z.data_type = 'FLOAT'
    rand_rot_z.inputs['Max'].default_value = 6.283
    
    combine_rot = gn_nodes.new("ShaderNodeCombineXYZ")
    gn_links.new(wind_map.outputs[0], combine_rot.inputs['X']) # Pitch forward/back
    gn_links.new(rand_rot_z.outputs['Value'], combine_rot.inputs['Z']) # Random local YAW

    rotate_inst = gn_nodes.new("GeometryNodeRotateInstances")
    rotate_inst.space = 'LOCAL'
    gn_links.new(combine_rot.outputs[0], rotate_inst.inputs['Rotation'])

    # Join nodes
    join = gn_nodes.new("GeometryNodeJoinGeometry")
    
    # Final Flow mapping
    gn_links.new(group_in.outputs['Geometry'], distribute.inputs['Mesh'])
    gn_links.new(distribute.outputs['Points'], instance_pts.inputs['Points'])
    gn_links.new(obj_info.outputs['Geometry'], instance_pts.inputs['Instance'])
    
    gn_links.new(instance_pts.outputs['Instances'], rotate_inst.inputs['Instances'])
    gn_links.new(rotate_inst.outputs['Instances'], store_attr.inputs['Geometry'])
    
    gn_links.new(group_in.outputs['Geometry'], join.inputs['Geometry'])
    gn_links.new(store_attr.outputs['Geometry'], join.inputs['Geometry'])
    gn_links.new(join.outputs['Geometry'], group_out.inputs['Geometry'])

    return f"Created Procedural Anime Grass Field '{object_name}' at {location}. Press 'Play' (Spacebar) in EEVEE to see dynamic wind and shading."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricWaveCluster",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.2, 0.8, 1.0),
    **kwargs
) -> str:
    """
    Create a procedural Volumetric Wave-Cluster in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created abstract object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B, A) base color for the icy glass material.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Object ===
    bpy.ops.mesh.primitive_plane_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # === Step 2: Build the Icy Glass Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlassMat")
    mat.use_nodes = True
    mnodes = mat.node_tree.nodes
    mlinks = mat.node_tree.links
    mnodes.clear()

    # Glass component
    glass = mnodes.new('ShaderNodeBsdfGlass')
    glass.inputs['Color'].default_value = material_color
    glass.inputs['Roughness'].default_value = 0.1  # Slight frosting

    # Transparent component (brighter/more saturated)
    transparent = mnodes.new('ShaderNodeBsdfTransparent')
    trans_color = (min(material_color[0]*1.5, 1.0), 
                   min(material_color[1]*1.5, 1.0), 
                   min(material_color[2]*1.5, 1.0), 1.0)
    transparent.inputs['Color'].default_value = trans_color

    # Mix together
    mix = mnodes.new('ShaderNodeMixShader')
    mix.inputs['Fac'].default_value = 0.5
    mlinks.new(glass.outputs['BSDF'], mix.inputs[1])
    mlinks.new(transparent.outputs['BSDF'], mix.inputs[2])

    out = mnodes.new('ShaderNodeOutputMaterial')
    mlinks.new(mix.outputs['Shader'], out.inputs['Surface'])
    
    # === Step 3: Geometry Nodes Procedural Setup ===
    mod = obj.modifiers.new(name="VolumetricCluster", type='NODES')
    group = bpy.data.node_groups.new(name=f"{object_name}_GeoTree", type='GeometryNodeTree')
    mod.node_group = group
    nodes = group.nodes
    links = group.links
    
    # Initialize I/O for compatibility across versions
    if hasattr(group, "interface"):
        group.interface.new_socket(name="Geometry", in_out='OUT', socket_type='NodeSocketGeometry')
    else:
        group.outputs.new('NodeSocketGeometry', 'Geometry')

    out_node = nodes.new('NodeGroupOutput')
    
    # 3a. Base Volume to scatter onto (Low Res)
    vol_cube_base = nodes.new('GeometryNodeVolumeCube')
    vol2mesh_base = nodes.new('GeometryNodeVolumeToMesh')
    vol2mesh_base.resolution_mode = 'VOXEL_AMOUNT'
    
    # Safely target the correct resolution socket depending on Blender version
    res_socket_name = 'Voxel Amount' if 'Voxel Amount' in vol2mesh_base.inputs else 'Resolution'
    vol2mesh_base.inputs[res_socket_name].default_value = 3  # Low res to create sparse vertices
    links.new(vol_cube_base.outputs['Volume'], vol2mesh_base.inputs['Volume'])
    
    # 3b. Instance Volume (High Res, Detailed)
    vol_cube_inst = nodes.new('GeometryNodeVolumeCube')
    vol_cube_inst.inputs['Resolution X'].default_value = 64
    vol_cube_inst.inputs['Resolution Y'].default_value = 64
    vol_cube_inst.inputs['Resolution Z'].default_value = 64
    
    # Drive Density with Spherical Wave Texture
    grad_tex = nodes.new('ShaderNodeTexGradient')
    grad_tex.gradient_type = 'SPHERICAL'
    
    wave_tex = nodes.new('ShaderNodeTexWave')
    wave_tex.inputs['Scale'].default_value = 8.0
    
    links.new(grad_tex.outputs['Color'], wave_tex.inputs['Vector'])
    links.new(wave_tex.outputs['Color'], vol_cube_inst.inputs['Density'])
    
    vol2mesh_inst = nodes.new('GeometryNodeVolumeToMesh')
    vol2mesh_inst.resolution_mode = 'VOXEL_AMOUNT'
    vol2mesh_inst.inputs[res_socket_name].default_value = 64
    links.new(vol_cube_inst.outputs['Volume'], vol2mesh_inst.inputs['Volume'])
    
    # 3c. Instancing and Chaos
    inst_points = nodes.new('GeometryNodeInstancesOnPoints')
    links.new(vol2mesh_base.outputs['Mesh'], inst_points.inputs['Points'])
    links.new(vol2mesh_inst.outputs['Mesh'], inst_points.inputs['Instance'])
    
    rand_rot = nodes.new('GeometryNodeRandomValue')
    rand_rot.data_type = 'FLOAT'
    rand_rot.inputs['Min'].default_value = 0.0
    rand_rot.inputs['Max'].default_value = 1.0 # Will be mapped to (0..1, 0..1, 0..1) radians
    links.new(rand_rot.outputs['Value'], inst_points.inputs['Rotation'])
    
    math_scale = nodes.new('ShaderNodeMath')
    math_scale.operation = 'ADD'
    math_scale.inputs[1].default_value = 0.5  # Creates range 0.5 to 1.5
    links.new(rand_rot.outputs['Value'], math_scale.inputs[0])
    links.new(math_scale.outputs['Value'], inst_points.inputs['Scale'])
    
    # 3d. Polish & Final Output
    smooth = nodes.new('GeometryNodeSetShadeSmooth')
    links.new(inst_points.outputs['Instances'], smooth.inputs['Geometry'])
    
    set_mat = nodes.new('GeometryNodeSetMaterial')
    set_mat.inputs['Material'].default_value = mat
    links.new(smooth.outputs['Geometry'], set_mat.inputs['Geometry'])
    
    links.new(set_mat.outputs['Geometry'], out_node.inputs[0])
    
    # === Step 4: Accompanying Lighting Setup ===
    light_data = bpy.data.lights.new(name=f"{object_name}_PointLight", type='POINT')
    light_data.energy = 25000.0  # High energy required to blow out the glass specularity
    light_data.color = (material_color[0], material_color[1], 1.0)
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    # Position light dynamically based on object location
    light_obj.location = Vector(location) + Vector((2.5 * scale, -2.5 * scale, 3.0 * scale))
    
    return f"Created procedural '{object_name}' cluster with {res_socket_name} volumetric instancing and lighting."

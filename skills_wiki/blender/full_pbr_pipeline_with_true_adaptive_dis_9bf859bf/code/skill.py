def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.22, 0.15),
    **kwargs,
) -> str:
    """
    Create a plane utilizing the full PBR workflow with True Adaptive Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the bricks.

    Returns:
        Status string confirming creation.
    """
    import bpy

    # === Step 1: Engine & Feature Set Preparation ===
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # Enable Adaptive Subdivision (Requires Cycles Experimental)
    try:
        obj.cycles.use_adaptive_subdivision = True
    except AttributeError:
        # Fallback for unexpected API states, though valid in modern Blender
        subsurf.levels = 5
        subsurf.render_levels = 5

    # === Step 3: Material & PBR Shader Network ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to actually displace the geometry, not just fake it
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    obj.data.materials.append(mat)
    
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    # Create Core Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 100)
    
    # Create PBR Map Conversion Nodes
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -200)
    disp_node.inputs['Midlevel'].default_value = 0.0  # As instructed in tutorial to prevent mesh shifting
    disp_node.inputs['Scale'].default_value = 0.1     # Controlled strength
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (300, -200)
    bump_node.inputs['Distance'].default_value = 0.1
    
    ramp_rough = nodes.new('ShaderNodeValToRGB')
    ramp_rough.location = (300, 100)
    ramp_rough.color_ramp.elements[0].position = 0.0
    ramp_rough.color_ramp.elements[0].color = (0.3, 0.3, 0.3, 1.0)
    ramp_rough.color_ramp.elements[1].position = 1.0
    ramp_rough.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)
    
    # Create Procedural Generator (Replaces downloaded image textures)
    brick_node = nodes.new('ShaderNodeTexBrick')
    brick_node.location = (0, 0)
    brick_node.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_node.inputs['Color2'].default_value = (material_color[0]*0.7, material_color[1]*0.7, material_color[2]*0.7, 1.0)
    brick_node.inputs['Mortar'].default_value = (0.6, 0.6, 0.6, 1.0)
    brick_node.inputs['Scale'].default_value = 3.0
    
    # Create Mapping Network
    mapping_node = nodes.new('ShaderNodeMapping')
    mapping_node.location = (-200, 0)
    
    tc_node = nodes.new('ShaderNodeTexCoord')
    tc_node.location = (-400, 0)
    
    val_node = nodes.new('ShaderNodeValue')
    val_node.location = (-400, -200)
    val_node.outputs[0].default_value = 1.0  # Master control for uniform scaling
    
    # === Step 4: Wire the Network ===
    # Coordinate Mapping
    links.new(tc_node.outputs['UV'], mapping_node.inputs['Vector'])
    links.new(val_node.outputs[0], mapping_node.inputs['Scale'])
    links.new(mapping_node.outputs['Vector'], brick_node.inputs['Vector'])
    
    # Albedo / Base Color
    links.new(brick_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Roughness
    links.new(brick_node.outputs['Color'], ramp_rough.inputs['Fac'])
    roughness_input = bsdf_node.inputs.get('Roughness')
    if roughness_input:
        links.new(ramp_rough.outputs['Color'], roughness_input)
        
    # Normal / Bump
    links.new(brick_node.outputs['Color'], bump_node.inputs['Height'])
    normal_input = bsdf_node.inputs.get('Normal')
    if normal_input:
        links.new(bump_node.outputs['Normal'], normal_input)
        
    # True Displacement
    links.new(brick_node.outputs['Color'], disp_node.inputs['Height'])
    
    # Outputs
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Deselect all and select new object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created '{object_name}' at {location}. Cycles Experimental mode activated for true Adaptive Displacement."

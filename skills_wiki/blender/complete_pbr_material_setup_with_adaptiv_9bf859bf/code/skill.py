def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a complete PBR material setup with Adaptive Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) Base color fallback.
        **kwargs: Additional parameters.

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Configure Render Engine for Displacement ===
    # True displacement and Adaptive Subdivision require Cycles Experimental
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # UV Unwrap (Smart UV Project)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 3: Add Adaptive Subdivision Modifier ===
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'  # Simple maintains the hard edges of the plane
    
    # Enable Adaptive Subdivision (Only works if Cycles Experimental is active)
    try:
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass # Failsafe for older/different Blender API contexts

    # === Step 4: Build PBR Material Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Crucial Setting: Tell the material to use actual geometry displacement
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP' 
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # Output & Principled BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Mapping Setup (Ctrl+T equivalent)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # 1. Base Color (Using Noise as a stand-in for an Image Texture)
    tex_color = nodes.new('ShaderNodeTexNoise')
    tex_color.location = (-100, 300)
    tex_color.inputs['Scale'].default_value = 15.0
    tex_color.label = "Base Color Map"
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    links.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])

    # 2. Roughness via inverted Gloss Map
    tex_gloss = nodes.new('ShaderNodeTexNoise')
    tex_gloss.location = (-100, 0)
    tex_gloss.inputs['Scale'].default_value = 25.0
    tex_gloss.label = "Gloss Map"
    links.new(mapping.outputs['Vector'], tex_gloss.inputs['Vector'])

    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    links.new(tex_gloss.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf.inputs['Roughness'])

    # 3. Normal Mapping
    tex_normal = nodes.new('ShaderNodeTexVoronoi')
    tex_normal.location = (-100, -300)
    tex_normal.inputs['Scale'].default_value = 30.0
    tex_normal.label = "Normal Map Data"
    links.new(mapping.outputs['Vector'], tex_normal.inputs['Vector'])

    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (200, -300)
    normal_map.inputs['Strength'].default_value = 1.0 # Emphasizes the bump
    links.new(tex_normal.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    # 4. True Displacement
    tex_disp = nodes.new('ShaderNodeTexNoise')
    tex_disp.location = (-100, -600)
    tex_disp.inputs['Scale'].default_value = 5.0
    tex_disp.label = "Displacement Map"
    links.new(mapping.outputs['Vector'], tex_disp.inputs['Vector'])

    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (800, -400)
    disp_node.inputs['Midlevel'].default_value = 0.0 # Prevents the entire plane from shifting globally
    disp_node.inputs['Scale'].default_value = 0.1    # Controls the height intensity
    links.new(tex_disp.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 5: Assign Material ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created PBR Object '{object_name}' at {location}. Switch viewport to Cycles Rendered view to see adaptive displacement."

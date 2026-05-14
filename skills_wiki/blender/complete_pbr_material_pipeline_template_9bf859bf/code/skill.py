def create_pbr_pipeline_template(
    scene_name: str = "Scene",
    object_name: str = "PBR_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.15, 0.15), # Base brick/wood color
    **kwargs,
) -> str:
    """
    Creates a subdivided plane with a fully wired, image-based PBR material setup.
    Includes mapping, HSV correction, Gloss->Roughness inversion, and Displacement.
    
    Args:
        scene_name: Name of the scene.
        object_name: Name of the generated mesh.
        location: (x, y, z) placement.
        scale: Size scale.
        material_color: Initial color of the mock 1x1 Base Color texture.
        
    Returns:
        Status string.
    """
    import bpy
    
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # 1. Setup Cycles for True Displacement
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'
    
    # 2. Create Base Geometry
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision Surface (Simple) for displacement detail
    subsurf = obj.modifiers.new(name="Displacement_Subdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6
    # Try enabling adaptive subdivision if the version supports it directly on the modifier
    if hasattr(subsurf, 'use_adaptive_subdivision'):
        subsurf.use_adaptive_subdivision = True

    # 3. Create Material & Enable Displacement Settings
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    mat.cycles.displacement_method = 'DISPLACEMENT' # Allows true mesh displacement
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # --- Output & Shader ---
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (1200, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (800, 0)
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # --- Mapping & Coordinates ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    # Reroute to keep noodles clean (as taught in the tutorial)
    reroute = nodes.new('NodeReroute')
    reroute.location = (-400, -100)
    
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], reroute.inputs[0])

    # --- Helper Function: Create Mock 1x1 Image Textures ---
    def create_mock_texture_node(name, pixels, colorspace='Non-Color', y_loc=0):
        # Create 1x1 image
        img = bpy.data.images.new(f"Mock_{name}", width=1, height=1)
        img.pixels = pixels
        
        # Create Node
        tex_node = nodes.new('ShaderNodeTexImage')
        tex_node.location = (-200, y_loc)
        tex_node.image = img
        if tex_node.image.colorspace_settings:
            tex_node.image.colorspace_settings.name = colorspace
            
        links.new(reroute.outputs[0], tex_node.inputs['Vector'])
        return tex_node

    # --- Setup PBR Maps ---
    
    # 1. Base Color (sRGB) -> HSV -> Base Color
    c_rgba = (material_color[0], material_color[1], material_color[2], 1.0)
    tex_color = create_mock_texture_node("Color", c_rgba, colorspace='sRGB', y_loc=300)
    
    hsv_node = nodes.new('ShaderNodeHueSaturation')
    hsv_node.location = (100, 300)
    links.new(tex_color.outputs['Color'], hsv_node.inputs['Color'])
    links.new(hsv_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # 2. Gloss map (Non-Color) -> Invert -> Roughness
    # (Setting mock pixel to 0.3 dark gloss, which inverts to 0.7 high roughness)
    tex_gloss = create_mock_texture_node("Gloss", (0.3, 0.3, 0.3, 1.0), y_loc=0)
    
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (100, 0)
    links.new(tex_gloss.outputs['Color'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # 3. Normal Map (Non-Color) -> Normal Node -> Normal
    tex_norm = create_mock_texture_node("Normal", (0.5, 0.5, 1.0, 1.0), y_loc=-300)
    
    normal_map_node = nodes.new('ShaderNodeNormalMap')
    normal_map_node.location = (100, -300)
    normal_map_node.inputs['Strength'].default_value = 1.0
    links.new(tex_norm.outputs['Color'], normal_map_node.inputs['Color'])
    links.new(normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # 4. Displacement Map (Non-Color) -> Displacement Node -> Output Displacement
    tex_disp = create_mock_texture_node("Displacement", (0.5, 0.5, 0.5, 1.0), y_loc=-600)
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (800, -400)
    disp_node.inputs['Scale'].default_value = 0.1     # Scaled down to prevent geometry explosion
    disp_node.inputs['Midlevel'].default_value = 0.0  # Prevents object shifting
    
    links.new(tex_disp.outputs['Color'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    return f"Created '{object_name}' PBR pipeline template at {location}. Cycles set to Experimental for Adaptive Subdivision."

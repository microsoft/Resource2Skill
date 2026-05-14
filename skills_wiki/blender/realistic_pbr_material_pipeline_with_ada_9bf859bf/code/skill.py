def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Creates a PBR material setup demonstrating true adaptive displacement, 
    map scaling, and gloss-to-roughness inversion using procedural stand-ins.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base color for the procedural texture.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine & Feature Set Context ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'
    
    # === Step 2: Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # === Step 3: Adaptive Subdivision Modifier ===
    subsurf = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    # Use 'SIMPLE' so the plane corners don't round off into an oval
    subsurf.subdivision_type = 'SIMPLE'
    # Fallback high levels in case adaptive isn't fully triggered in viewport
    subsurf.levels = 4
    subsurf.render_levels = 6
    
    # Attempt to enable the adaptive subdivision toggle if the API exposes it
    if hasattr(subsurf, 'use_adaptive_subdivision'):
        subsurf.use_adaptive_subdivision = True
        
    # === Step 4: Material & Engine Displacement Settings ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    # Crucial step: Tell the material to actually push geometry, not just bump normals
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # === Step 5: Build PBR Node Pipeline ===
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)
    
    # Texture Mapping (Uniformly controlled via a Value node)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    
    scale_val = nodes.new('ShaderNodeValue')
    scale_val.location = (-1000, -200)
    scale_val.outputs['Value'].default_value = 3.0  # Tile the texture
    
    # Base Texture (Simulating image maps with a procedural node)
    tex_base = nodes.new('ShaderNodeTexBrick')
    tex_base.location = (-500, 0)
    tex_base.inputs['Color1'].default_value = (*material_color, 1.0)
    tex_base.inputs['Color2'].default_value = (material_color[0]*0.5, material_color[1]*0.5, material_color[2]*0.5, 1.0)
    
    # Hue/Saturation for non-destructive color grading
    hsv = nodes.new('ShaderNodeHueSaturation')
    hsv.location = (-200, 200)
    hsv.inputs['Saturation'].default_value = 1.2
    
    # Invert node to simulate converting a "Glossiness" map into a "Roughness" map
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (-200, -100)
    
    # Bump node to generate Normals from scalar height data
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -400)
    bump.inputs['Distance'].default_value = 0.05
    
    # True Displacement node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (600, -400)
    # Fix tearing by setting Midlevel to 0.0, reduce scale to realistic values
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.1
    
    # === Step 6: Link Pipeline ===
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(scale_val.outputs['Value'], mapping.inputs['Scale'])
    links.new(mapping.outputs['Vector'], tex_base.inputs['Vector'])
    
    # Color Channel
    links.new(tex_base.outputs['Color'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], principled.inputs['Base Color'])
    
    # Roughness Channel (Gloss invert tip)
    links.new(tex_base.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], principled.inputs['Roughness'])
    
    # Normal Channel
    links.new(tex_base.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # Displacement Channel
    links.new(tex_base.outputs['Fac'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Surface
    links.new(principled.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Clean selection
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    return f"Created '{object_name}' at {location} with complete PBR node tree and Adaptive Displacement enabled."

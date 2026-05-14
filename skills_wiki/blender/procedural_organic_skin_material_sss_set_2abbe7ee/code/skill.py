def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSkinHead",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.65, 0.55),
    **kwargs,
) -> str:
    """
    Create a procedural organic skin material applied to a subdivided base mesh.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base skin tone in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get the target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Store current selection to restore later (optional but good practice)
    original_active = bpy.context.active_object

    # === Step 1: Create Base Geometry ===
    # We use Suzanne as it has distinct folds/ears to show off SSS and AO
    bpy.ops.mesh.primitive_monkey_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision Surface for smooth organic curves
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 3
    subdiv.render_levels = 3
    
    # Shade smooth
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Procedural Skin Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_SkinMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Output Node
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Roughness'].default_value = 0.45
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # SSS Settings (Version agnostic handling for Blender 3.x and 4.0+)
    # Human skin scatters red furthest, then green, then blue.
    sss_radius = (1.0, 0.2, 0.1) 
    
    if 'Subsurface Weight' in bsdf.inputs: # Blender 4.0+
        bsdf.inputs['Subsurface Weight'].default_value = 1.0
        bsdf.inputs['Subsurface Radius'].default_value = sss_radius
        bsdf.inputs['Subsurface Scale'].default_value = 0.05 * scale
    elif 'Subsurface' in bsdf.inputs: # Blender 3.x
        bsdf.inputs['Subsurface'].default_value = 0.15
        bsdf.inputs['Subsurface Radius'].default_value = sss_radius
        if 'Subsurface Color' in bsdf.inputs:
            bsdf.inputs['Subsurface Color'].default_value = (*material_color, 1.0)
            
    # --- Micro-pores (Voronoi Bump) ---
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, -300)
    voronoi.inputs['Scale'].default_value = 250.0 / scale
    
    # ColorRamp to isolate cell centers as tiny pits
    ramp_pores = nodes.new('ShaderNodeValToRGB')
    ramp_pores.location = (-150, -300)
    ramp_pores.color_ramp.elements[0].position = 0.0
    ramp_pores.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0) # Pit center
    ramp_pores.color_ramp.elements[1].position = 0.15
    ramp_pores.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0) # Flat skin
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (100, -300)
    bump.inputs['Strength'].default_value = 0.12
    bump.inputs['Distance'].default_value = 0.02 * scale
    
    links.new(voronoi.outputs['Distance'], ramp_pores.inputs['Fac'])
    links.new(ramp_pores.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # --- Color Variation (Ambient Occlusion) ---
    # Creates darker, reddish mid-tones in cavities/folds
    ao = nodes.new('ShaderNodeAmbientOcclusion')
    ao.location = (-400, 200)
    
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (-150, 200)
    ramp_color.color_ramp.elements[0].position = 0.3
    # Darker, more saturated reddish-brown for folds
    dark_tone = (material_color[0]*0.6, material_color[1]*0.4, material_color[2]*0.4, 1.0)
    ramp_color.color_ramp.elements[0].color = dark_tone
    ramp_color.color_ramp.elements[1].position = 0.8
    # Base skin tone for exposed areas
    ramp_color.color_ramp.elements[1].color = (*material_color, 1.0)
    
    links.new(ao.outputs['Color'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    # Ensure object is linked to the target scene collection
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    # Restore active object
    if original_active:
        bpy.context.view_layer.objects.active = original_active

    return f"Created organic object '{obj.name}' with procedural SSS skin material at {location}."

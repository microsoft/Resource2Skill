def create_pbr_architecture(
    scene_name: str = "Scene",
    object_name: str = "PBR_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR Node Architecture demonstrating proper Color, Roughness, Normal, 
    and Displacement wiring using procedural textures as stand-ins for images.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision Surface for physical displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6

    # === Step 2: Build PBR Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Crucial: Enable True Displacement in material settings (Requires Cycles)
    mat.cycles.displacement_method = 'BOTH' # Displacement and Bump
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")
    
    # --- Coordinates & Universal Mapping ---
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (-1400, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-1200, 0)
    
    # Universal Scale Node (Tutorial Tip: Drive scale from one Value node)
    master_scale = nodes.new('ShaderNodeValue')
    master_scale.location = (-1400, -200)
    master_scale.outputs[0].default_value = 3.0
    master_scale.label = "Universal Scale"
    
    links.new(coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(master_scale.outputs[0], mapping.inputs['Scale'])
    
    # --- COLOR STREAM ---
    tex_color = nodes.new('ShaderNodeTexNoise')
    tex_color.location = (-900, 300)
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    
    # Tint the procedural noise with the requested material_color
    tint = nodes.new('ShaderNodeMixRGB')
    tint.location = (-700, 300)
    tint.blend_type = 'MULTIPLY'
    tint.inputs['Fac'].default_value = 0.8
    tint.inputs[2].default_value = (*material_color, 1.0)
    links.new(tex_color.outputs['Color'], tint.inputs[1])
    
    # HSV node for post-adjustments (Tutorial Tip)
    hsv = nodes.new('ShaderNodeHueSaturation')
    hsv.location = (-500, 300)
    hsv.inputs['Saturation'].default_value = 0.9
    links.new(tint.outputs['Color'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], bsdf.inputs['Base Color'])
    
    # --- ROUGHNESS STREAM (GLOSS TO ROUGHNESS) ---
    tex_gloss = nodes.new('ShaderNodeTexNoise')
    tex_gloss.location = (-900, 0)
    links.new(mapping.outputs['Vector'], tex_gloss.inputs['Vector'])
    
    # Invert node to convert Gloss data to Roughness data (Tutorial Tip)
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (-500, 0)
    links.new(tex_gloss.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])
    
    # --- NORMAL/BUMP STREAM ---
    tex_norm = nodes.new('ShaderNodeTexNoise')
    tex_norm.location = (-900, -300)
    links.new(mapping.outputs['Vector'], tex_norm.inputs['Vector'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-500, -300)
    bump.inputs['Strength'].default_value = 0.4
    links.new(tex_norm.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # --- DISPLACEMENT STREAM ---
    tex_disp = nodes.new('ShaderNodeTexNoise')
    tex_disp.location = (-900, -600)
    links.new(mapping.outputs['Vector'], tex_disp.inputs['Vector'])
    
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (-500, -600)
    # Midlevel 0 prevents the geometry from floating away from the object origin
    disp.inputs['Midlevel'].default_value = 0.0 
    disp.inputs['Scale'].default_value = 0.15
    links.new(tex_disp.outputs['Fac'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])

    return f"Created '{object_name}' at {location} with full PBR node architecture."

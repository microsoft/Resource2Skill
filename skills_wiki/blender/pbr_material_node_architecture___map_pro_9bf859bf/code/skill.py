def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Architecture",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Creates a surface demonstrating a complete PBR material node architecture,
    including Color, Specular, Roughness, Normal, and true Displacement channels.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for true geometric displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6

    # === Step 2: Build Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Enable Displacement in material settings (Required for Cycles displacement)
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # --- Output & Main Shader ---
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1200, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (800, 0)
    links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])

    # --- Mapping Setup (Synchronizes all maps) ---
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- Color Channel ---
    # Procedural stand-in for the Color Map
    color_tex = nodes.new(type='ShaderNodeTexNoise')
    color_tex.location = (-400, 350)
    color_tex.inputs['Scale'].default_value = 4.0

    color_mix = nodes.new(type='ShaderNodeMixRGB')
    color_mix.location = (-200, 350)
    color_mix.inputs['Color1'].default_value = (*material_color, 1.0)
    color_mix.inputs['Color2'].default_value = (material_color[0]*0.3, material_color[1]*0.3, material_color[2]*0.3, 1.0)

    # Tutorial Tip: Hue/Saturation node for global color tweaking
    hue_sat = nodes.new(type='ShaderNodeHueSaturation')
    hue_sat.location = (0, 350)
    hue_sat.inputs['Saturation'].default_value = 0.85

    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])
    links.new(color_tex.outputs['Fac'], color_mix.inputs['Fac'])
    links.new(color_mix.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], principled.inputs['Base Color'])

    # --- Specular/Reflection Channel ---
    spec_tex = nodes.new(type='ShaderNodeTexNoise')
    spec_tex.location = (-400, 100)
    spec_tex.inputs['Scale'].default_value = 15.0

    # Safe hookup supporting both Blender 3.x and 4.0+ BSDF changes
    spec_socket = principled.inputs.get('Specular IOR Level') or principled.inputs.get('Specular')
    if spec_socket:
        links.new(mapping.outputs['Vector'], spec_tex.inputs['Vector'])
        links.new(spec_tex.outputs['Fac'], spec_socket)

    # --- Roughness Channel ---
    # Procedural stand-in for the Gloss/Roughness Map
    gloss_tex = nodes.new(type='ShaderNodeTexNoise')
    gloss_tex.location = (-600, -150)
    gloss_tex.inputs['Scale'].default_value = 10.0

    # Tutorial Tip: Invert node to convert Gloss data to Roughness data
    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (-400, -150)

    # Tutorial Tip: ColorRamp to manually fine-tune surface shininess contrast
    ramp = nodes.new(type='ShaderNodeValToRGB')
    ramp.location = (-200, -150)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[1].position = 0.65

    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])
    links.new(gloss_tex.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], principled.inputs['Roughness'])

    # --- Normal/Bump Channel ---
    # Procedural stand-in for Normal Map (high frequency details)
    norm_tex = nodes.new(type='ShaderNodeTexVoronoi')
    norm_tex.location = (-400, -500)
    norm_tex.inputs['Scale'].default_value = 25.0

    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (0, -500)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.6

    links.new(mapping.outputs['Vector'], norm_tex.inputs['Vector'])
    links.new(norm_tex.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # --- Displacement Channel ---
    # Procedural stand-in for Displacement Map (low frequency physical height)
    disp_tex = nodes.new(type='ShaderNodeTexNoise')
    disp_tex.location = (-400, -800)
    disp_tex.inputs['Scale'].default_value = 2.0

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -300)
    disp_node.inputs['Scale'].default_value = 0.2
    disp_node.inputs['Midlevel'].default_value = 0.5

    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    # Note: Displacement routes to Material Output, NOT Principled BSDF
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    return f"Created '{object_name}' with complete procedural PBR material architecture at {location}."

def create_pbr_framework(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.7, 0.25, 0.2),
    **kwargs,
) -> str:
    """
    Create a PBR Material Framework with True Displacement in the active Blender scene.
    
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
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Engine Setup for Adaptive Subdivision ===
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Apply Simple Subdivision for the displacement to act upon
    subdiv = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    # Enable Adaptive Subdivision (Cycles Experimental Feature)
    if hasattr(subdiv, 'cycles'):
        subdiv.cycles.use_adaptive_subdivision = True

    # === Step 3: Build PBR Material Framework ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Crucial step: Tell the material to actually displace the geometry
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # --- Node Creation ---
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (1400, 0)

    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.location = (1000, 0)

    # 1. Coordinates & Master Scale
    node_tex_coord = nodes.new('ShaderNodeTexCoord')
    node_tex_coord.location = (-1200, 0)

    node_mapping = nodes.new('ShaderNodeMapping')
    node_mapping.location = (-1000, 0)

    node_scale_val = nodes.new('ShaderNodeValue')
    node_scale_val.label = "Master UV Scale"
    node_scale_val.location = (-1200, -250)
    node_scale_val.outputs[0].default_value = 5.0

    # 2. Texture Sources (Simulating Image Maps)
    node_tex_color = nodes.new('ShaderNodeTexNoise')
    node_tex_color.label = "Albedo Map"
    node_tex_color.location = (-600, 300)

    node_tex_gloss = nodes.new('ShaderNodeTexNoise')
    node_tex_gloss.label = "Gloss Map"
    node_tex_gloss.location = (-600, 0)

    node_tex_norm = nodes.new('ShaderNodeTexVoronoi')
    node_tex_norm.label = "Normal Map"
    node_tex_norm.location = (-600, -300)

    node_tex_disp = nodes.new('ShaderNodeTexNoise')
    node_tex_disp.label = "Displacement Map"
    node_tex_disp.location = (-600, -600)

    # 3. Processors & Converters
    # Color grading
    node_ramp = nodes.new('ShaderNodeValToRGB')
    node_ramp.location = (-400, 300)
    node_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0)
    node_ramp.color_ramp.elements[1].color = (*material_color, 1.0)

    node_hsv = nodes.new('ShaderNodeHueSaturation')
    node_hsv.location = (-100, 300)

    node_curves = nodes.new('ShaderNodeRGBCurve')
    node_curves.location = (200, 300)

    # Gloss -> Roughness Inversion
    node_invert = nodes.new('ShaderNodeInvert')
    node_invert.label = "Gloss to Roughness"
    node_invert.location = (-200, 0)

    # Normal Vector translation
    node_normal_map = nodes.new('ShaderNodeNormalMap')
    node_normal_map.location = (-200, -300)
    node_normal_map.inputs['Strength'].default_value = 1.5

    # True Displacement translation
    node_displacement = nodes.new('ShaderNodeDisplacement')
    node_displacement.location = (1000, -400)
    node_displacement.inputs['Scale'].default_value = 0.1
    node_displacement.inputs['Midlevel'].default_value = 0.0 # Prevents mesh inflation

    # --- Node Linking ---
    # Mapping
    links.new(node_tex_coord.outputs['UV'], node_mapping.inputs['Vector'])
    links.new(node_scale_val.outputs[0], node_mapping.inputs['Scale'])

    links.new(node_mapping.outputs['Vector'], node_tex_color.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex_gloss.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex_norm.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex_disp.inputs['Vector'])

    # Color Pipeline
    links.new(node_tex_color.outputs['Fac'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_hsv.inputs['Color'])
    links.new(node_hsv.outputs['Color'], node_curves.inputs['Color'])
    links.new(node_curves.outputs['Color'], node_bsdf.inputs['Base Color'])

    # Roughness Pipeline
    links.new(node_tex_gloss.outputs['Fac'], node_invert.inputs['Color'])
    links.new(node_invert.outputs['Color'], node_bsdf.inputs['Roughness'])

    # Normal Pipeline
    links.new(node_tex_norm.outputs['Color'], node_normal_map.inputs['Color'])
    links.new(node_normal_map.outputs['Normal'], node_bsdf.inputs['Normal'])

    # Displacement Pipeline
    links.new(node_tex_disp.outputs['Fac'], node_displacement.inputs['Height'])
    
    # Final Output
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    links.new(node_displacement.outputs['Displacement'], node_output.inputs['Displacement'])

    return f"Created PBR framework '{object_name}' at {location} with true adaptive displacement."

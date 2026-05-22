def create_object(
    scene_name: str = "Scene",
    object_name: str = "Adaptive_PBR_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a plane utilizing Cycles Adaptive Subdivision and a full PBR material setup.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the procedural texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Engine Configuration ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 3: Modifiers & Adaptive Subdivision ===
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Prevents rounding the corners of the plane
    
    # Enable adaptive dicing (only works when feature_set is EXPERIMENTAL)
    obj.cycles.use_adaptive_subdivision = True

    # === Step 4: Material Initialization ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Crucial Setting: Tell the material to actually displace geometry, not just bump
    mat.cycles.displacement_method = 'BOTH' # "Displacement and Bump"

    # === Step 5: Build PBR Node Tree ===
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (1200, 0)
    
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (800, 0)
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    # Mapping & Coordinates
    node_tex_coord = nodes.new(type='ShaderNodeTexCoord')
    node_tex_coord.location = (-800, 0)
    
    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-600, 0)
    node_mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0) # Adjust texture scale
    links.new(node_tex_coord.outputs['UV'], node_mapping.inputs['Vector'])

    # Procedural Maps (Acting as our downloaded PBR images)
    node_noise = nodes.new(type='ShaderNodeTexNoise')
    node_noise.location = (-300, 200)
    node_noise.inputs['Scale'].default_value = 5.0
    node_noise.inputs['Detail'].default_value = 15.0
    links.new(node_mapping.outputs['Vector'], node_noise.inputs['Vector'])

    node_voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    node_voronoi.location = (-300, -300)
    node_voronoi.inputs['Scale'].default_value = 12.0
    links.new(node_mapping.outputs['Vector'], node_voronoi.inputs['Vector'])

    # 5a. Base Color Pipeline (Color -> Hue/Sat -> RGB Curve)
    node_base_color = nodes.new(type='ShaderNodeRGB')
    node_base_color.location = (-300, 500)
    node_base_color.outputs[0].default_value = (*material_color, 1.0)

    node_mix = nodes.new(type='ShaderNodeMixRGB')
    node_mix.location = (0, 300)
    node_mix.blend_type = 'MULTIPLY'
    node_mix.inputs['Fac'].default_value = 0.8
    links.new(node_base_color.outputs[0], node_mix.inputs[1])
    links.new(node_noise.outputs['Color'], node_mix.inputs[2])

    node_hue_sat = nodes.new(type='ShaderNodeHueSaturation')
    node_hue_sat.location = (250, 300)
    links.new(node_mix.outputs['Color'], node_hue_sat.inputs['Color'])

    node_curve = nodes.new(type='ShaderNodeRGBCurve')
    node_curve.location = (450, 300)
    links.new(node_hue_sat.outputs['Color'], node_curve.inputs['Color'])
    links.new(node_curve.outputs['Color'], node_principled.inputs['Base Color'])

    # 5b. Gloss to Roughness Conversion (Using Invert Node)
    node_invert = nodes.new(type='ShaderNodeInvert')
    node_invert.location = (450, 0)
    links.new(node_noise.outputs['Fac'], node_invert.inputs['Color'])
    links.new(node_invert.outputs['Color'], node_principled.inputs['Roughness'])

    # 5c. Specular / Reflection Mapping (Handling Blender 3.x vs 4.x API changes)
    if 'Specular IOR Level' in node_principled.inputs:
        links.new(node_noise.outputs['Fac'], node_principled.inputs['Specular IOR Level'])
    elif 'Specular' in node_principled.inputs:
        links.new(node_noise.outputs['Fac'], node_principled.inputs['Specular'])

    # 5d. Normal Mapping
    node_bump = nodes.new(type='ShaderNodeBump')
    node_bump.location = (450, -300)
    node_bump.inputs['Strength'].default_value = 0.4
    links.new(node_voronoi.outputs['Distance'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_principled.inputs['Normal'])

    # 5e. True Displacement Setup
    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (800, -300)
    node_disp.inputs['Midlevel'].default_value = 0.0 # Crucial: prevents mesh from floating
    node_disp.inputs['Scale'].default_value = 0.1    # Crucial: scales spikes down to realistic levels
    links.new(node_voronoi.outputs['Distance'], node_disp.inputs['Height'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])

    return f"Created '{object_name}' at {location} with full PBR Adaptive Displacement configured for Cycles."

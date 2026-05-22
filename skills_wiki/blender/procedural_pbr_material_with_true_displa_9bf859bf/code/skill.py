def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR Material setup utilizing True Displacement and Adaptive Subdivision.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created object and material setup.
    """
    import bpy
    from mathutils import Vector

    # === Engine & Feature Setup ===
    # Enable Cycles and Experimental Features for Adaptive Subdivision
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier (Simple, Adaptive)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    # Enable adaptive subdivision on the object's cycles settings
    if hasattr(obj, 'cycles'):
        obj.cycles.use_adaptive_subdivision = True

    # === Step 2: Create Material & Node Tree ===
    mat = bpy.data.materials.new(name="PBR_Procedural_Displacement")
    mat.use_nodes = True
    
    # Crucial: Tell the material to actually displace the geometry, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Nodes
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_out.location = (1200, 0)

    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (800, 0)

    # Coordinate and Mapping (To scale textures globally)
    node_tex_coord = nodes.new(type='ShaderNodeTexCoord')
    node_tex_coord.location = (-800, 0)

    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-600, 0)
    node_mapping.inputs['Scale'].default_value = (5.0, 5.0, 5.0)

    # Procedural Textures replacing external images
    node_noise = nodes.new(type='ShaderNodeTexNoise')
    node_noise.location = (-300, 200)
    node_noise.inputs['Scale'].default_value = 3.0
    node_noise.inputs['Detail'].default_value = 15.0

    node_voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    node_voronoi.location = (-300, -300)
    node_voronoi.inputs['Scale'].default_value = 4.0

    # Color Data (Albedo mapping)
    node_colorramp = nodes.new(type='ShaderNodeValToRGB')
    node_colorramp.location = (0, 300)
    node_colorramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    node_colorramp.color_ramp.elements[1].color = (*material_color, 1.0)

    # Roughness Data (Demonstrating the Gloss -> Invert -> Roughness workflow from video)
    node_invert = nodes.new(type='ShaderNodeInvert')
    node_invert.location = (0, 0)

    # Normal Data (Using Bump to convert procedural scalar data to fake angle data)
    node_bump = nodes.new(type='ShaderNodeBump')
    node_bump.location = (300, -200)
    node_bump.inputs['Strength'].default_value = 0.5

    # True Displacement Data (Requires object subdivision to function)
    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (800, -400)
    node_disp.inputs['Midlevel'].default_value = 0.0
    node_disp.inputs['Scale'].default_value = 0.15 # Kept subtle as recommended

    # === Step 3: Link Nodes ===
    # Vectors
    links.new(node_tex_coord.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_noise.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_voronoi.inputs['Vector'])

    # Color
    links.new(node_noise.outputs['Fac'], node_colorramp.inputs['Fac'])
    links.new(node_colorramp.outputs['Color'], node_bsdf.inputs['Base Color'])

    # Roughness (Inverting noise to act like an inverted gloss map)
    links.new(node_noise.outputs['Fac'], node_invert.inputs['Color'])
    links.new(node_invert.outputs['Color'], node_bsdf.inputs['Roughness'])

    # Normal
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])

    # Displacement (Voronoi creates chunky height changes)
    links.new(node_voronoi.outputs['Distance'], node_disp.inputs['Height'])
    
    # Final Outputs
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
    links.new(node_disp.outputs['Displacement'], node_out.inputs['Displacement'])

    return f"Created '{object_name}' at {location} with Procedural Displacement PBR Shader (Cycles + Adaptive Subdiv activated)."

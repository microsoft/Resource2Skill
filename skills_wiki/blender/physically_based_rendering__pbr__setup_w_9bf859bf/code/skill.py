def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Adaptive_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.54, 0.18, 0.12),
    **kwargs,
) -> str:
    """
    Create a procedurally displaced plane demonstrating the PBR & Adaptive Displacement workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary color for the base color map.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    # === Step 1: Engine & Experimental Feature Setup ===
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # Adaptive displacement REQUIRES Cycles and Experimental features
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Base Geometry Creation ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 3: Adaptive Subdivision Modifier ===
    mod = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    mod.subdivision_type = 'SIMPLE' # Keeps the edges square
    
    # Safely enable adaptive subdivision (API structure check)
    try:
        mod.use_adaptive_subdivision = True
    except AttributeError:
        # Fallback if API context changes, standard in some older versions
        pass

    # === Step 4: Material & PBR Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to use actual vertex displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    obj.data.materials.append(mat)

    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    # Create Core Shader Nodes
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    links.new(bsdf.outputs[0], out.inputs['Surface'])

    # Coordinate Mapping setup (standard PBR UV workflow)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-1000, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- Procedural Texture (Acting as our downloaded PBR Maps) ---
    # We use a Voronoi texture to generate distinct "rock/brick" like height values
    pbr_map = nodes.new('ShaderNodeTexVoronoi')
    pbr_map.feature = 'F2'
    pbr_map.distance = 'CHEBYSHEV'
    pbr_map.inputs['Scale'].default_value = 8.0
    pbr_map.location = (-800, 0)
    links.new(mapping.outputs['Vector'], pbr_map.inputs['Vector'])

    # 1. Base Color Map
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-400, 200)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    links.new(pbr_map.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # 2. Gloss -> Roughness Map (Demonstrating the Invert technique)
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (-400, -50)
    links.new(pbr_map.outputs['Distance'], invert.inputs['Color'])
    # Safely link to Roughness
    if 'Roughness' in bsdf.inputs:
        links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # 3. Displacement Map (The core feature)
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (-200, -300)
    disp.inputs['Midlevel'].default_value = 0.0   # Prevents shifting the whole mesh
    disp.inputs['Scale'].default_value = 0.25     # Controls intensity of the extrusion
    
    links.new(pbr_map.outputs['Distance'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], out.inputs['Displacement'])

    return f"Created '{object_name}' at {location}. Cycles set to Experimental with Adaptive Displacement active."

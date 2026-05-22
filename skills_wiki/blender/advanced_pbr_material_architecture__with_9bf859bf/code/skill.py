def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.65, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR material setup featuring True Displacement,
    Adaptive Subdivision, and Gloss-to-Roughness inversion.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh and material.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base color for the procedural PBR texture.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine & Experimental Features ===
    # True displacement requires Cycles and Experimental feature set for Adaptive Subdiv
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Failsafe for specific Blender builds

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    subsurf.levels = 3  # Viewport fallback
    subsurf.render_levels = 4 # Render fallback
    
    # Enable Adaptive Subdivision if available in the API version
    if hasattr(subsurf, 'use_adaptive_subdivision'):
        subsurf.use_adaptive_subdivision = True
    elif hasattr(obj, 'cycles') and hasattr(obj.cycles, 'use_adaptive_subdivision'):
        obj.cycles.use_adaptive_subdivision = True

    # === Step 3: Build the PBR Node Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Critical: Set material to use both Displacement and Bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 200)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Mapping & Coordinates
    tc_node = nodes.new('ShaderNodeTexCoord')
    tc_node.location = (-800, 200)
    
    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (-600, 200)
    # Adjust scale as demonstrated in the video to tile the texture
    map_node.inputs['Scale'].default_value = (3.0, 3.0, 3.0) 
    links.new(tc_node.outputs['UV'], map_node.inputs['Vector'])

    # Procedural Map Generator (Standing in for Image Textures)
    tex_node = nodes.new('ShaderNodeTexNoise')
    tex_node.location = (-400, 200)
    tex_node.inputs['Scale'].default_value = 10.0
    tex_node.inputs['Detail'].default_value = 15.0
    tex_node.inputs['Roughness'].default_value = 0.6
    links.new(map_node.outputs['Vector'], tex_node.inputs['Vector'])

    # 1. Base Color Channel
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 400)
    color_ramp.color_ramp.elements[0].color = (material_color[0]*0.2, material_color[1]*0.2, material_color[2]*0.2, 1)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1)
    links.new(tex_node.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # 2. Roughness Channel (Using Gloss -> Invert logic from the video)
    # Pretend the texture is a "Gloss" map, which means white=shiny. 
    # We invert it to make white=rough for the Principled BSDF.
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (-100, 150)
    links.new(tex_node.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])

    # 3. Normal Channel
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -100)
    bump_node.inputs['Distance'].default_value = 0.05
    bump_node.inputs['Strength'].default_value = 0.8
    links.new(tex_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # 4. True Displacement Channel
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -200)
    disp_node.inputs['Midlevel'].default_value = 0.5  # Fixes geometry shifting as noted in the tutorial
    disp_node.inputs['Scale'].default_value = 0.15     # Keep low to prevent mesh explosion
    links.new(tex_node.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Deselect all and select the new object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created '{object_name}' at {location} with complete PBR node topology and Adaptive Displacement."

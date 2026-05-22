def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a plane with a fully wired PBR material and Adaptive Displacement.
    Simulates the image-texture workflow using procedural nodes for standalone execution.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural brick.
        **kwargs: Additional overrides (e.g., displacement_scale).

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine and Feature Setup ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for adaptive displacement
    subsurf = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'  # Simple keeps the plane's corners sharp
    
    # Enable adaptive subdivision (Micropolygons)
    try:
        obj.cycles.use_adaptive_subdivision = True
    except AttributeError:
        pass # Failsafe for specific Blender versions/configurations

    # === Step 3: PBR Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # CRITICAL: Tell the material to use actual geometry displacement, not just bump
    mat.cycles.displacement_method = 'BOTH' # "Displacement and Bump"

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clean slate

    # Main Output and BSDF
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # === Step 4: Vector Mapping Architecture (Ctrl+T equivalent) ===
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- PBR Data Streams ---
    # We use procedural textures to perfectly simulate the Image Texture workflow 
    # without requiring external downloads.

    # 1. Base Color (Albedo)
    brick_tex = nodes.new('ShaderNodeTexBrick')
    brick_tex.location = (-400, 400)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0]*0.7, material_color[1]*0.7, material_color[2]*0.7, 1.0)
    brick_tex.inputs['Scale'].default_value = 4.0
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    links.new(brick_tex.outputs['Color'], bsdf.inputs['Base Color'])

    # 2. Specular / Reflection Map
    refl_val = nodes.new('ShaderNodeValue')
    refl_val.location = (-400, 150)
    refl_val.outputs[0].default_value = 0.25 # Non-color value simulation
    # Handle Blender 4.0+ Specular naming change safely
    spec_socket = bsdf.inputs.get('Specular IOR Level') or bsdf.inputs.get('Specular')
    if spec_socket:
        links.new(refl_val.outputs[0], spec_socket)

    # 3. Gloss Map -> Inverted to Roughness
    gloss_tex = nodes.new('ShaderNodeTexNoise')
    gloss_tex.location = (-600, -100)
    gloss_tex.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])

    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (-400, -100)
    links.new(gloss_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf.inputs['Roughness'])

    # 4. Normal Map
    normal_noise = nodes.new('ShaderNodeTexNoise')
    normal_noise.location = (-600, -350)
    normal_noise.inputs['Scale'].default_value = 30.0
    links.new(mapping.outputs['Vector'], normal_noise.inputs['Vector'])

    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (-400, -350)
    normal_map.inputs['Strength'].default_value = 1.5
    links.new(normal_noise.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    # 5. Displacement Map
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -250)
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_scale = kwargs.get('displacement_scale', 0.1)
    disp_node.inputs['Scale'].default_value = disp_scale
    
    # Driving the physical height with the mortar lines of the brick texture
    links.new(brick_tex.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    # Deselect all, select newly created
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created PBR Plane '{object_name}' at {location}. Cycles engine activated for Adaptive Displacement."

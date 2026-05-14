def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR Material Pipeline with True Adaptive Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural bricks.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine Context ===
    # True displacement and Adaptive Subdivision require Cycles set to Experimental
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = Vector((scale, scale, scale))

    # Add Subdivision Surface Modifier
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'  # Prevents the plane's corners from rounding

    # Enable Adaptive Subdivision (Only active when Cycles is Experimental)
    try:
        subdiv.use_adaptive_subdivision = True
    except AttributeError:
        # Fallback for API mismatches in certain Blender versions
        subdiv.levels = 5
        subdiv.render_levels = 6

    # === Step 3: Build PBR Material Pipeline ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Enable True Displacement in Material Settings
    try:
        mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
    except AttributeError:
        pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (1200, 0)

    principled = nodes.new(type="ShaderNodeBsdfPrincipled")
    principled.location = (800, 0)

    # Texture Mapping Setup (equivalent to Ctrl+T)
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-400, 0)

    # Procedural texture acting as our PBR Image Maps (Substituting external files)
    brick_tex = nodes.new(type="ShaderNodeTexBrick")
    brick_tex.location = (-200, 0)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0] * 0.8, material_color[1] * 0.8, material_color[2] * 0.8, 1.0)
    brick_tex.inputs['Scale'].default_value = 4.0

    # Hue/Saturation node (Tutorial tip for art-directing Base Color)
    hsv_node = nodes.new(type="ShaderNodeHueSaturation")
    hsv_node.location = (200, 200)
    hsv_node.inputs['Saturation'].default_value = 0.9

    # Invert node for Gloss map -> Roughness (Tutorial technique)
    invert_node = nodes.new(type="ShaderNodeInvert")
    invert_node.location = (200, -100)

    # Bump node (Procedural substitute for Normal Map node)
    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.location = (200, -300)
    bump_node.inputs['Strength'].default_value = 0.5
    bump_node.inputs['Distance'].default_value = 0.1

    # Displacement node
    disp_node = nodes.new(type="ShaderNodeDisplacement")
    disp_node.location = (800, -300)
    disp_node.inputs['Midlevel'].default_value = 0.0  # Prevents mesh from detaching from origin
    disp_node.inputs['Scale'].default_value = 0.05    # Kept low to prevent extreme spikes

    # === Step 4: Route the PBR Channels ===
    
    # UV Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])

    # 1. Base Color pipeline
    links.new(brick_tex.outputs['Color'], hsv_node.inputs['Color'])
    links.new(hsv_node.outputs['Color'], principled.inputs['Base Color'])

    # 2. Specular pipeline (Tutorial uses Reflection map)
    # Handles API change in Blender 4.0+ ('Specular IOR Level' vs 'Specular')
    spec_input = principled.inputs.get('Specular IOR Level') or principled.inputs.get('Specular')
    if spec_input:
        links.new(brick_tex.outputs['Fac'], spec_input)

    # 3. Roughness pipeline (Gloss -> Invert -> Roughness)
    links.new(brick_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], principled.inputs['Roughness'])

    # 4. Normal pipeline
    links.new(brick_tex.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled.inputs['Normal'])

    # 5. Displacement pipeline
    links.new(brick_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    # Output routing
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    return f"Created '{object_name}' with Adaptive Displacement PBR pipeline at {location}. Switch to Rendered View in Cycles to see displacement."

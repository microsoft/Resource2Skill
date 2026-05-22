def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Demo",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane featuring a complete, procedural PBR material pipeline.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the brick texture.
        **kwargs: Additional optional overrides.

    Returns:
        Status string.
    """
    import bpy

    # Get the active scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add subdivision for true displacement
    subsurf = obj.modifiers.new(name="Displacement_Subdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6
    
    # === Step 2: Build Material & PBR Pipeline ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Enable true displacement in material settings (Crucial for Cycles)
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # --- Core Shader Nodes ---
    mat_out = nodes.new(type="ShaderNodeOutputMaterial")
    mat_out.location = (1200, 0)
    
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], mat_out.inputs['Surface'])
    
    # --- Coordinates & Universal Mapping ---
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Value node for uniform scale control (Tutorial tip)
    scale_val = nodes.new(type="ShaderNodeValue")
    scale_val.location = (-1000, -250)
    scale_val.outputs['Value'].default_value = 4.0
    # In newer Blender versions, Value plugs gracefully into Vector inputs
    links.new(scale_val.outputs['Value'], mapping.inputs['Scale'])
    
    # --- Texture Simulation (Replacing downloaded images) ---
    # We use a Brick Texture as our "Base map" to simulate the video's brick material
    brick_tex = nodes.new(type="ShaderNodeTexBrick")
    brick_tex.location = (-400, 200)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0]*0.7, material_color[1]*0.7, material_color[2]*0.7, 1.0)
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    
    # --- Base Color Channel (with Color Correction) ---
    hsv = nodes.new(type="ShaderNodeHueSaturation")
    hsv.location = (-100, 200)
    hsv.inputs['Saturation'].default_value = 0.85
    links.new(brick_tex.outputs['Color'], hsv.inputs['Color'])
    
    curves = nodes.new(type="ShaderNodeRGBCurve")
    curves.location = (200, 200)
    links.new(hsv.outputs['Color'], curves.inputs['Color'])
    links.new(curves.outputs['Color'], bsdf.inputs['Base Color'])
    
    # --- Roughness Channel (Simulating Gloss to Roughness inversion) ---
    noise_tex = nodes.new(type="ShaderNodeTexNoise")
    noise_tex.location = (-400, -150)
    noise_tex.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
    
    invert = nodes.new(type="ShaderNodeInvert")
    invert.location = (-100, -150)
    links.new(noise_tex.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])
    
    # --- Normal Channel ---
    bump = nodes.new(type="ShaderNodeBump")
    bump.location = (400, -300)
    bump.inputs['Strength'].default_value = 0.4
    links.new(brick_tex.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # --- Displacement Channel ---
    disp = nodes.new(type="ShaderNodeDisplacement")
    disp.location = (800, -400)
    disp.inputs['Midlevel'].default_value = 0.0  # As taught in tutorial
    disp.inputs['Scale'].default_value = 0.05
    links.new(brick_tex.outputs['Color'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], mat_out.inputs['Displacement'])
    
    # Ensure Cycles is set as the render engine to preview true displacement
    scene.render.engine = 'CYCLES'
    
    return f"Created '{object_name}' at {location} with full PBR mapping and Displacement pipeline."

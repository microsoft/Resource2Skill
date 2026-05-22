def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.7, 0.6),
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR material setup demonstrating true displacement, 
    gloss inversion, and normal mapping on a subdivided plane.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base tint for the procedural rock/paving surface.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Cycles as it is required for True Displacement
    scene.render.engine = 'CYCLES'
    if scene.cycles.feature_set != 'EXPERIMENTAL':
        # Recommended for adaptive subdivision, but standard works too
        pass

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for displacement geometry
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High level for viewport displacement
    subsurf.render_levels = 6 # High level for render displacement

    # === Step 2: Build PBR Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Blender to use true physical displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Define Core Nodes
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (1200, 0)
    
    bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf_node.location = (800, 200)
    
    # 1. Texture Coordinate & Mapping (Node Wrangler Ctrl+T logic)
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-600, 0)
    # Uniformly scale the texture across the surface
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    
    # 2. Procedural Texture Generator (Acting as our downloaded Image Textures)
    # In a real workflow, this would be 5 separate Image Texture nodes.
    # We use Voronoi here to generate an interesting bumpy stone/paving pattern.
    texture = nodes.new(type="ShaderNodeTexVoronoi")
    texture.location = (-400, 0)
    
    # 3. BASE COLOR Workflow
    # Video tip: Tweak base colors using ColorRamp and Hue/Sat nodes
    color_ramp = nodes.new(type="ShaderNodeValToRGB")
    color_ramp.location = (-100, 300)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    hue_sat = nodes.new(type="ShaderNodeHueSaturation")
    hue_sat.location = (200, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1 # Slight boost
    
    # 4. GLOSS TO ROUGHNESS Workflow
    # Video tip: If you download a Gloss map, you must Invert it for the Roughness socket
    invert_gloss = nodes.new(type="ShaderNodeInvert")
    invert_gloss.location = (200, 100)
    
    # 5. NORMAL MAP Workflow
    # Video tip: Non-color data into a Normal Map (or Bump) node
    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.location = (200, -100)
    bump_node.inputs['Strength'].default_value = 0.5
    
    # 6. DISPLACEMENT Workflow
    # Video tip: Midlevel 0.0, Scale adjusted low (e.g., 0.1)
    displacement_node = nodes.new(type="ShaderNodeDisplacement")
    displacement_node.location = (800, -200)
    displacement_node.inputs['Midlevel'].default_value = 0.0
    displacement_node.inputs['Scale'].default_value = 0.1
    
    # === Step 3: Wire Everything Together ===
    # Coordinate Mapping
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], texture.inputs['Vector'])
    
    # Color Branch
    links.new(texture.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Specular / Reflection Branch (Using raw distance value)
    links.new(texture.outputs['Distance'], bsdf_node.inputs['Specular IOR Level'])
    
    # Roughness Branch (Demonstrating Gloss inversion)
    links.new(texture.outputs['Distance'], invert_gloss.inputs['Color'])
    links.new(invert_gloss.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # Normal Branch
    links.new(texture.outputs['Distance'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # Displacement Branch
    links.new(texture.outputs['Distance'], displacement_node.inputs['Height'])
    
    # Final Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

    return f"Created '{object_name}' at {location} configured with advanced PBR shading and True Displacement. Switch viewport to Cycles Rendered view to see physical displacement."

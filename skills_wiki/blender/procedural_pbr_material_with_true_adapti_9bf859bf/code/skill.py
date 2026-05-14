def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Brick_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.1), # Brick base color
    **kwargs,
) -> str:
    """
    Create a procedurally textured PBR surface with True Adaptive Displacement.
    Simulates the image-texture workflow from the tutorial using procedural nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the bricks.
        **kwargs: Additional parameters (e.g., displacement_scale).

    Returns:
        Status string describing the created object.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Setup Render Engine for True Displacement
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # 2. Create Base Geometry
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier (Adaptive)
    subdiv = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    # Use simple subdivision to avoid rounding the corners of the plane
    subdiv.subdivision_type = 'SIMPLE'
    # Enable Adaptive Subdivision (only works if feature_set is EXPERIMENTAL)
    if hasattr(subdiv, "use_adaptive_subdivision"):
        subdiv.use_adaptive_subdivision = True

    # 3. Create Material & Node Tree
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # Crucial Step: Enable True Displacement in Material Settings
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
        
    # --- Create Nodes ---
    # Output & BSDF
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (1200, 0)
    
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (800, 0)
    
    # Mapping Coordinates (Tutorial: Ctrl+T)
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-600, 0)
    
    # Texture (Using Procedural Brick to simulate downloaded maps)
    brick_tex = nodes.new(type="ShaderNodeTexBrick")
    brick_tex.location = (-300, 0)
    brick_tex.inputs['Color 1'].default_value = (*material_color, 1.0) # RGB + Alpha
    brick_tex.inputs['Color 2'].default_value = (material_color[0]*0.8, material_color[1]*0.8, material_color[2]*0.8, 1.0)
    brick_tex.inputs['Mortar'].default_value = (0.8, 0.8, 0.8, 1.0)
    brick_tex.inputs['Scale'].default_value = 3.0
    
    # Color Adjustment (Tutorial: Tweaking Base Color with Hue/Sat)
    hue_sat = nodes.new(type="ShaderNodeHueSaturation")
    hue_sat.location = (400, 200)
    hue_sat.inputs['Saturation'].default_value = 0.9
    hue_sat.inputs['Value'].default_value = 1.1
    
    # Roughness Map Logic (Tutorial: Inverting a Gloss Map)
    # We use the mortar/brick factor as a base, then invert it to simulate the tutorial step
    invert_roughness = nodes.new(type="ShaderNodeInvert")
    invert_roughness.location = (400, 0)
    invert_roughness.inputs['Fac'].default_value = 1.0
    
    # Normal Map Logic (Tutorial: Adding fake bump detail)
    bump = nodes.new(type="ShaderNodeBump")
    bump.location = (400, -200)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.5
    
    # Displacement Logic (Tutorial: True geometry displacement)
    displacement = nodes.new(type="ShaderNodeDisplacement")
    displacement.location = (800, -300)
    displacement.inputs['Midlevel'].default_value = 0.0 # Tutorial recommends 0 to prevent plane shifting
    displacement_scale = kwargs.get('displacement_scale', 0.05) # Keep small to avoid crazy spikes
    displacement.inputs['Scale'].default_value = displacement_scale
    
    # --- Connect Nodes ---
    # Vectors
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    
    # Color -> Hue/Sat -> BSDF Base Color
    links.new(brick_tex.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Factor -> Invert -> BSDF Roughness
    links.new(brick_tex.outputs['Fac'], invert_roughness.inputs['Color'])
    links.new(invert_roughness.outputs['Color'], bsdf.inputs['Roughness'])
    
    # Factor -> Bump -> BSDF Normal
    links.new(brick_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Factor -> Displacement -> Output Displacement
    links.new(brick_tex.outputs['Fac'], displacement.inputs['Height'])
    
    # Final connections to Output
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    # Deselect all and make active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created PBR Object '{object_name}' at {location}. Cycles Experimental feature set enabled for Adaptive Displacement."

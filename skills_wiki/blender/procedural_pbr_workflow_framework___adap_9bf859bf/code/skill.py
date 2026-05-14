def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.25, 0.2),
    **kwargs,
) -> str:
    """
    Create a Procedural PBR Material framework utilizing Adaptive Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Context Setup for Adaptive Displacement ===
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier for Adaptive Subdivision
    subdiv = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    subdiv.subdivision_type = 'CATMULL_CLARK'
    try:
        # Fails gracefully if not in Cycles/Experimental context
        subdiv.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # === Step 3: Build PBR Material Framework ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Crucial: Tell the material to actually displace the geometry
    mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes safely
    for node in nodes:
        nodes.remove(node)
        
    # Standard Outputs
    mat_out = nodes.new('ShaderNodeOutputMaterial')
    mat_out.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    links.new(bsdf.outputs['BSDF'], mat_out.inputs['Surface'])
    
    # Coordinate System
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Unified Scale Node (Affects all maps simultaneously)
    scale_val = nodes.new('ShaderNodeValue')
    scale_val.location = (-600, -200)
    scale_val.label = "Master Scale"
    scale_val.outputs[0].default_value = 5.0
    links.new(scale_val.outputs[0], mapping.inputs['Scale'])
    
    # --- Simulated PBR Maps ---
    
    # 1. Base Color Map Simulation
    color_tex = nodes.new('ShaderNodeTexNoise')
    color_tex.location = (-100, 300)
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 300)
    links.new(color_tex.outputs['Color'], color_ramp.inputs['Fac'])
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    
    # Handle Blender 4.0+ vs 3.x Principled BSDF socket naming
    base_color_socket = bsdf.inputs.get('Base Color') or bsdf.inputs[0]
    links.new(color_ramp.outputs['Color'], base_color_socket)
    
    # 2. Gloss -> Roughness Inversion Logic
    gloss_tex = nodes.new('ShaderNodeTexNoise')
    gloss_tex.location = (-100, 0)
    gloss_tex.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])
    
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    links.new(gloss_tex.outputs['Fac'], invert_node.inputs['Color'])
    
    roughness_socket = bsdf.inputs.get('Roughness')
    if roughness_socket:
        links.new(invert_node.outputs['Color'], roughness_socket)
    
    # 3. Normal / Bump Map Simulation
    bump_tex = nodes.new('ShaderNodeTexVoronoi')
    bump_tex.location = (-100, -300)
    bump_tex.inputs['Scale'].default_value = 20.0
    links.new(mapping.outputs['Vector'], bump_tex.inputs['Vector'])
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -300)
    bump_node.inputs['Strength'].default_value = 0.5
    links.new(bump_tex.outputs['Distance'], bump_node.inputs['Height'])
    
    normal_socket = bsdf.inputs.get('Normal')
    if normal_socket:
        links.new(bump_node.outputs['Normal'], normal_socket)
    
    # 4. True Displacement Simulation
    disp_tex = nodes.new('ShaderNodeTexNoise')
    disp_tex.location = (200, -600)
    disp_tex.inputs['Scale'].default_value = 2.0
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -600)
    disp_node.inputs['Scale'].default_value = 0.15
    disp_node.inputs['Midlevel'].default_value = 0.0  # Kept at 0 per tutorial
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    disp_socket = mat_out.inputs.get('Displacement')
    if disp_socket:
        links.new(disp_node.outputs['Displacement'], disp_socket)

    # Force view update
    bpy.context.view_layer.update()

    return f"Created procedural PBR Framework '{object_name}' at {location} with Adaptive Subdivision."

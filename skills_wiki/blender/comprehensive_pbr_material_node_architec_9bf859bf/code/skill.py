def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Showcase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR material setup using procedural nodes mimicking
    image maps, with a unified mapping controller and true displacement.

    Args:
        scene_name: Name of the active scene.
        object_name: Name of the plane object.
        location: (x,y,z) position.
        scale: Uniform scale of the object.
        material_color: RGB base color.

    Returns:
        Status string.
    """
    import bpy
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Setup Cycles for True Displacement
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Fallback if experimental isn't available
        
    # 2. Create the Base Plane
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # 3. Add Subdivision Surface (Adaptive)
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    subdiv.levels = 4
    subdiv.render_levels = 4
    # Adaptive subdiv is only available in Cycles Experimental
    try:
        obj.cycles.use_adaptive_subdivision = True
    except AttributeError:
        pass
        
    # 4. Create Material & Enable Displacement Settings
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    if mat.name not in [m.name for m in obj.data.materials]:
        obj.data.materials.append(mat)
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # === Core Output Nodes ===
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1200, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (800, 0)
    
    # Handle API changes for Specular in Blender 4.0+
    specular_socket = principled.inputs.get('Specular IOR Level')
    if not specular_socket:
        specular_socket = principled.inputs.get('Specular')
    
    # === Conversion Nodes ===
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (800, -300)
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.1
    
    norm = nodes.new('ShaderNodeNormalMap')
    norm.location = (400, -200)
    norm.inputs['Strength'].default_value = 3.0
    
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (400, 0)
    
    hsv = nodes.new('ShaderNodeHueSaturation')
    hsv.location = (400, 200)
    
    # === Procedural Texture "Maps" (Substituting Images) ===
    # Base Color generator
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (100, 200)
    ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0)
    ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 15.0
    
    # === Unified Mapping Architecture ===
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-500, 0)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-700, 0)
    
    val = nodes.new('ShaderNodeValue')
    val.name = "Unified Texture Scale"
    val.label = "Unified Texture Scale"
    val.location = (-700, -200)
    val.outputs[0].default_value = 1.5
    
    # === Routing the Node Graph ===
    # Coordinate Mapping Path
    links.new(val.outputs[0], mapping.inputs['Scale'])
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    # Base Color Path (Color Map -> HSV -> BSDF)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], principled.inputs['Base Color'])
    
    # Roughness Path (Gloss Map -> Invert -> Roughness)
    links.new(noise.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], principled.inputs['Roughness'])
    
    # Specular Path
    if specular_socket:
        links.new(noise.outputs['Fac'], specular_socket)
        
    # Normal Path (Normal Map -> Normal Node -> BSDF)
    links.new(noise.outputs['Color'], norm.inputs['Color'])
    links.new(norm.outputs['Normal'], principled.inputs['Normal'])
    
    # Displacement Path (Height Map -> Disp Node -> Material Output)
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    
    # Final Surface Connections
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])
    
    # Frame organization (Optional visual cleanup)
    frame = nodes.new('NodeFrame')
    frame.name = "Unified Mapping Setup"
    frame.label = "Unified Mapping Setup"
    mapping.parent = frame
    tex_coord.parent = frame
    val.parent = frame
    
    return f"Created '{object_name}' with comprehensive PBR shader network at {location}."

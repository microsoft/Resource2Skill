def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralPBRPlane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 3.0,
    material_color: tuple = (0.5, 0.4, 0.3),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a True PBR Displacement material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        material_color: (R, G, B) base color for the highest points of the texture.
        **kwargs: Optional overrides (e.g., displacement_scale).

    Returns:
        Status string describing the creation.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Ensure Cycles for True Displacement ===
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Geometry & Topology ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)
    
    # Add Dense Subdivision (Procedural alternative to the video's 100 loop cuts)
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 7  # High level to give the displacement node enough vertices
    subsurf.render_levels = 7
    
    # === Step 3: Build Procedural PBR Displacement Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to actually displace the geometry, not just fake bump
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    
    if len(plane.data.materials) == 0:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Base Shader Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    
    # Displacement Node
    disp_scale = kwargs.get("displacement_scale", 0.2)
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (700, -300)
    disp.inputs['Midlevel'].default_value = 0.5
    disp.inputs['Scale'].default_value = disp_scale
    
    # Procedural Generation: Voronoi for macro rocky chunks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (0, 0)
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 6.0
    
    # Procedural Generation: Noise for micro surface details
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -300)
    noise.inputs['Scale'].default_value = 20.0
    if 'Detail' in noise.inputs:
        noise.inputs['Detail'].default_value = 15.0
        
    # Mix the noise and voronoi
    math_mul = nodes.new('ShaderNodeMath')
    math_mul.operation = 'MULTIPLY'
    math_mul.location = (200, -300)
    math_mul.inputs[1].default_value = 0.2
    
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    math_add.location = (400, -150)
    
    links.new(noise.outputs['Fac'], math_mul.inputs[0])
    links.new(voronoi.outputs['Distance'], math_add.inputs[0])
    links.new(math_mul.outputs['Value'], math_add.inputs[1])
    
    # Color Ramp for PBR Base Color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (400, 100)
    color_ramp.color_ramp.elements[0].position = 0.0
    # Crevices get a darker tint of the base color
    color_ramp.color_ramp.elements[0].color = (
        material_color[0]*0.2, 
        material_color[1]*0.2, 
        material_color[2]*0.2, 
        1.0
    )
    color_ramp.color_ramp.elements[1].position = 1.0
    # Peaks get the full base color
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    
    # Map Range for PBR Roughness
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (400, -400)
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = 0.6  # Min roughness
    map_range.inputs[4].default_value = 0.9  # Max roughness
    
    # Final Node Connections
    links.new(math_add.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(math_add.outputs['Value'], map_range.inputs['Value'])
    links.new(math_add.outputs['Value'], disp.inputs['Height'])
    
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
    
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # === Step 4: Add Lighting Context ===
    # Add the specific Sun light from the video to highlight the displacement shadows
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = math.radians(11.4)
    sun_obj = bpy.data.objects.new(name=f"{object_name}_SunLight", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    sun_obj.location = (location[0], location[1], location[2] + 10.0)
    # Angle it to rake across the surface to emphasize depth
    sun_obj.rotation_euler = (math.radians(45), math.radians(45), 0)
    
    return f"Created '{object_name}' with True Displacement Shader and Sun Light at {location}"

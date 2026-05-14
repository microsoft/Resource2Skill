def create_pbr_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Displaced_Ground",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true procedural geometric displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created grid object.
        location: (x, y, z) world-space position.
        scale: Size of the surface grid.
        material_color: (R, G, B) base color, from which light/dark variations are derived.
        **kwargs: 
            subdivisions (int): Density of the mesh (default: 100).
            displacement_strength (float): Height of the displacement (default: 0.25).

    Returns:
        Status string confirming creation.
    """
    import bpy
    import colorsys
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure Cycles is enabled, as true displacement does not work in EEVEE
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'feature_set'):
        scene.cycles.feature_set = 'SUPPORTED'
    
    # === Step 1: Geometry ===
    subdivisions = kwargs.get('subdivisions', 100)
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=subdivisions, 
        y_subdivisions=subdivisions, 
        size=scale, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    # === Step 2: Material Generation ===
    mat = bpy.data.materials.new(name=f"{object_name}_Displacement_Mat")
    mat.use_nodes = True
    
    # The critical setting that enables true geometric displacement in Cycles
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Derive dark and light color variations from the base material_color
    r, g, b = material_color
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    c_dark = colorsys.hls_to_rgb(h, max(0, l - 0.15), s) + (1.0,)
    c_light = colorsys.hls_to_rgb(h, min(1, l + 0.15), s) + (1.0,)
    
    # Create Shader Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 200)
    bsdf_node.inputs['Roughness'].default_value = 0.85 # Dry, rough surface
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -200)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = kwargs.get('displacement_strength', 0.25)
    
    # Macro Noise (drives the large physical bumps)
    noise_disp = nodes.new('ShaderNodeTexNoise')
    noise_disp.location = (200, -200)
    noise_disp.inputs['Scale'].default_value = 3.0
    noise_disp.inputs['Detail'].default_value = 15.0
    noise_disp.inputs['Roughness'].default_value = 0.6
    
    # Micro Noise (drives the color variation and fine bump)
    noise_color = nodes.new('ShaderNodeTexNoise')
    noise_color.location = (0, 200)
    noise_color.inputs['Scale'].default_value = 15.0
    noise_color.inputs['Detail'].default_value = 15.0
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (300, 200)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = c_dark
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = c_light
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (300, -50)
    bump_node.inputs['Strength'].default_value = 0.5
    bump_node.inputs['Distance'].default_value = 0.1
    
    # === Step 3: Linking ===
    # Displacement mapping
    links.new(noise_disp.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Color mapping
    links.new(noise_color.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Bump mapping (fine detail on top of the physical displacement)
    links.new(noise_color.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # Surface output
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
        
    return f"Created PBR Displaced Surface '{object_name}' with {subdivisions}x{subdivisions} subdivisions at {location}. (Engine switched to Cycles)"

def create_pbr_displacement_terrain(
    scene_name: str = "Scene",
    object_name: str = "PBR_Terrain_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 5.0,
    base_color_dark: tuple = (0.05, 0.03, 0.02, 1.0),
    base_color_light: tuple = (0.35, 0.25, 0.18, 1.0),
    displacement_scale: float = 0.25,
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a procedural PBR material featuring true displacement.
    Note: Automatically switches the scene render engine to CYCLES to enable true displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Size of the terrain grid.
        base_color_dark: (R, G, B, A) dark color for deep crevices.
        base_color_light: (R, G, B, A) light color for peaks.
        displacement_scale: How intense the physical displacement height is.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Force Cycles render engine (required for true displacement)
    scene.render.engine = 'CYCLES'
    # Optional: Enable experimental feature set for adaptive subdivision
    # scene.cycles.feature_set = 'EXPERIMENTAL'

    # 2. Create Dense Base Geometry
    # A 100x100 grid provides 10,000 faces, good base for displacement
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=100, 
        y_subdivisions=100, 
        size=scale, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add Subdivision Surface modifier for even smoother displacement resolution
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps the grid square
    subsurf.levels = 2
    subsurf.render_levels = 3

    # 3. Create Material & Enable Displacement Setting
    mat = bpy.data.materials.new(name=f"M_{object_name}_PBR")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to actually move vertices, not just fake lighting
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    obj.data.materials.append(mat)

    # 4. Build Procedural PBR Node Tree
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (800, 200)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    # Main Height/Structure Noise (acting as the Displacement/Height Map)
    macro_noise = nodes.new(type='ShaderNodeTexNoise')
    macro_noise.location = (-200, 0)
    macro_noise.inputs['Scale'].default_value = 3.0
    macro_noise.inputs['Detail'].default_value = 15.0
    macro_noise.inputs['Roughness'].default_value = 0.6
    links.new(tex_coord.outputs['Object'], macro_noise.inputs['Vector'])

    # Micro Detail Noise (acting as the specific Normal map)
    micro_noise = nodes.new(type='ShaderNodeTexNoise')
    micro_noise.location = (-200, -300)
    micro_noise.inputs['Scale'].default_value = 50.0
    micro_noise.inputs['Detail'].default_value = 5.0
    links.new(tex_coord.outputs['Object'], micro_noise.inputs['Vector'])

    # A. Color Map Routing
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (200, 300)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = base_color_dark
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = base_color_light
    links.new(macro_noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # B. Roughness Map Routing
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (200, 0)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0) # Medium rough
    rough_ramp.color_ramp.elements[1].position = 0.8
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0) # Very rough
    links.new(macro_noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    # C. Normal/Bump Map Routing
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (400, -200)
    bump_node.inputs['Strength'].default_value = 0.6
    bump_node.inputs['Distance'].default_value = 0.1
    links.new(micro_noise.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # D. Displacement Map Routing
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -200)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = displacement_scale
    links.new(macro_noise.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # 5. Add a Sun Light to highlight the displacement (as done in the video)
    # Check if a sun already exists, if not, create one
    if not any(l.type == 'SUN' for l in bpy.data.lights):
        sun_data = bpy.data.lights.new(name="Displacement_Sun", type='SUN')
        sun_data.energy = 5.0 # High strength to show shadows
        sun_obj = bpy.data.objects.new(name="Displacement_Sun_Obj", object_data=sun_data)
        scene.collection.objects.link(sun_obj)
        sun_obj.location = (0, 0, 10)
        sun_obj.rotation_euler = (0.785, 0.5, 0) # Angled to cast shadows across bumps

    return f"Created PBR terrain '{object_name}' with Cycles displacement enabled. Mesh is sub-divided grid at {location}."

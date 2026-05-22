def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Create a highly detailed, procedurally displaced plane in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock/surface.
        **kwargs: Optional overrides (e.g., disp_scale, subsurf_levels).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Context & Engine Setup ===
    # True displacement requires Cycles to function properly
    scene.render.engine = 'CYCLES'

    # === Step 2: Base Geometry & Modifiers ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Use bmesh to create a 10x10 pre-subdivided grid
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=10, y_segments=10, size=2.0)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for the micro-geometry
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps edges square
    subsurf.levels = kwargs.get('subsurf_levels', 5)
    subsurf.render_levels = kwargs.get('subsurf_levels', 6)

    # === Step 3: Material & Displacement Settings ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use true vertex displacement
    mat.cycles.displacement_method = 'DISPLACEMENT'
    obj.data.materials.append(mat)

    # === Step 4: Shader Node Tree (Procedural PBR Setup) ===
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (500, 200)
    bsdf_node.inputs['Roughness'].default_value = 0.85 # Rough rocky surface
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (500, -200)
    disp_scale = kwargs.get('disp_scale', 0.15)
    disp_node.inputs['Scale'].default_value = disp_scale * scale 
    disp_node.inputs['Midlevel'].default_value = 0.0

    # Procedural Height Generation (Voronoi Cracks + Noise)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    
    # Voronoi for structural cracks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 150)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    
    # Noise for surface grit
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, -150)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    
    # Math: Invert Voronoi edges so cracks are deep, plates are high
    math_inv = nodes.new('ShaderNodeMath')
    math_inv.operation = 'SUBTRACT'
    math_inv.inputs[0].default_value = 1.0
    math_inv.location = (-200, 150)
    
    # Math: Multiply inverted Voronoi by 0.7
    math_mult1 = nodes.new('ShaderNodeMath')
    math_mult1.operation = 'MULTIPLY'
    math_mult1.inputs[1].default_value = 0.7
    math_mult1.location = (0, 150)
    
    # Math: Multiply Noise by 0.3
    math_mult2 = nodes.new('ShaderNodeMath')
    math_mult2.operation = 'MULTIPLY'
    math_mult2.inputs[1].default_value = 0.3
    math_mult2.location = (0, -150)
    
    # Math: Add them together to get the final Height Map
    math_height = nodes.new('ShaderNodeMath')
    math_height.operation = 'ADD'
    math_height.location = (200, 0)

    # ColorRamp: Convert height data into Albedo (Color)
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (200, 300)
    ramp_color.color_ramp.elements[0].position = 0.1
    ramp_color.color_ramp.elements[0].color = (0.015, 0.015, 0.015, 1.0) # Deep dark cracks
    ramp_color.color_ramp.elements[1].position = 0.6
    ramp_color.color_ramp.elements[1].color = material_color + (1.0,) # Surface rock color

    # Wire it all together
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    links.new(voronoi.outputs['Distance'], math_inv.inputs[1])
    links.new(math_inv.outputs['Value'], math_mult1.inputs[0])
    links.new(noise.outputs['Fac'], math_mult2.inputs[0])
    
    links.new(math_mult1.outputs['Value'], math_height.inputs[0])
    links.new(math_mult2.outputs['Value'], math_height.inputs[1])
    
    links.new(math_height.outputs['Value'], ramp_color.inputs['Fac'])
    links.new(math_height.outputs['Value'], disp_node.inputs['Height'])
    
    links.new(ramp_color.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 5: Complementary Lighting ===
    # Add a Sun light to ensure the displacement casts visible shadows
    sun_exists = any(l.type == 'SUN' for l in bpy.data.lights)
    if not sun_exists:
        sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
        sun_data.energy = 5.0
        sun_data.angle = 0.05 # Smaller angle = sharper shadows for small crags
        sun_obj = bpy.data.objects.new(f"{object_name}_Sun", sun_data)
        
        sun_obj.location = Vector(location) + Vector((5, -5, 10))
        sun_obj.rotation_euler = (math.radians(45), 0, math.radians(45))
        scene.collection.objects.link(sun_obj)

    return f"Created '{object_name}' with Procedural Displacement at {location}. Cycles engine activated."

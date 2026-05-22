def create_cycles_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    subdivision_levels: int = 6,
    displacement_scale: float = 0.2,
    base_color_dark: tuple = (0.05, 0.04, 0.03, 1.0),
    base_color_light: tuple = (0.25, 0.20, 0.15, 1.0),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a procedural PBR material utilizing 
    Cycles True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        subdivision_levels: Density of the mesh (higher = finer displacement detail).
        displacement_scale: Intensity/height of the displacement.
        base_color_dark: (R, G, B, A) for the deep crevices.
        base_color_light: (R, G, B, A) for the raised bumps.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine Setup ===
    # True displacement REQUIRES Cycles
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.feature_set = 'SUPPORTED'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for required geometry density
    subsurf = obj.modifiers.new(name="Subdivision_For_Displacement", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps the edges square
    subsurf.levels = subdivision_levels
    subsurf.render_levels = subdivision_levels

    # === Step 3: Build PBR Material with True Displacement ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Displacement Node setup
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (0, -200)
    # Adjust scale relative to object scale so it doesn't blow out
    disp_node.inputs['Scale'].default_value = displacement_scale * scale 
    disp_node.inputs['Midlevel'].default_value = 0.0
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Procedural Height Map (Inverted Voronoi for chunky, rocky look)
    voronoi_disp = nodes.new('ShaderNodeTexVoronoi')
    voronoi_disp.location = (-400, -200)
    voronoi_disp.feature = 'F1'
    voronoi_disp.distance = 'EUCLIDEAN'
    voronoi_disp.inputs['Scale'].default_value = 2.0
    
    math_invert = nodes.new('ShaderNodeMath')
    math_invert.location = (-200, -200)
    math_invert.operation = 'SUBTRACT'
    math_invert.inputs[0].default_value = 1.0
    links.new(voronoi_disp.outputs['Distance'], math_invert.inputs[1])
    links.new(math_invert.outputs['Value'], disp_node.inputs['Height'])

    # Procedural Albedo (Color) and Roughness Map
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-600, 0)
    noise_tex.inputs['Scale'].default_value = 10.0
    noise_tex.inputs['Detail'].default_value = 15.0
    noise_tex.inputs['Roughness'].default_value = 0.7

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, 50)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[0].color = base_color_dark
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = base_color_light
    links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-300, -100)
    rough_ramp.color_ramp.elements[0].position = 0.0
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].position = 1.0
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    links.new(noise_tex.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # === Step 4: Add Lighting Context ===
    # Add a Sun light to cast harsh shadows over the physical displacement
    sun_data = bpy.data.lights.new(name=f"{object_name}_SunLight", type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = 0.05 # Sharp shadows
    
    sun_obj = bpy.data.objects.new(name=f"{object_name}_SunObj", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    # Position the sun up and to the side, pointing diagonally down at the plane
    sun_obj.location = Vector(location) + Vector((5, -5, 10))
    sun_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created '{object_name}' (Scale: {scale}, Subdivisions: {subdivision_levels}) with Cycles true displacement and Sun lighting."

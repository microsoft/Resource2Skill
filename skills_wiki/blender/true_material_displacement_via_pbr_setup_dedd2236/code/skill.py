def create_procedural_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    subdivision_levels: int = 6,
    displacement_scale: float = 0.2,
    base_color_dark: tuple = (0.1, 0.08, 0.06),
    base_color_light: tuple = (0.4, 0.35, 0.30),
    **kwargs
) -> str:
    """
    Create a highly subdivided plane with true material displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        subdivision_levels: Density of the mesh for displacement (higher = more detail, slower render).
        displacement_scale: Height multiplier for the displacement node.
        base_color_dark: (R, G, B) color for the deep cracks.
        base_color_light: (R, G, B) color for the high peaks.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render Engine Setup ===
    # True displacement requires Cycles. 
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'feature_set'):
        scene.cycles.feature_set = 'SUPPORTED'

    # === Step 2: Base Geometry & Topology ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier (Simple) for dense geometry
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdivision_levels
    subsurf.render_levels = subdivision_levels + 1

    # === Step 3: Material & Procedural Shading ===
    mat = bpy.data.materials.new(name=f"{object_name}_DisplacementMat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use true displacement instead of bump mapping
    mat.cycles.displacement_method = 'DISPLACEMENT'
    plane.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default setup

    # Outputs
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (500, 0)
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (500, -200)
    disp.inputs['Scale'].default_value = displacement_scale
    disp.inputs['Midlevel'].default_value = 0.0
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])

    # Procedural Height Map Generators (Rock-like)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    # Voronoi for cracks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 4.0
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])

    # Noise for surface detail
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -300)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])

    # Multiply them together to create final height map
    mix_math = nodes.new('ShaderNodeMath')
    mix_math.operation = 'MULTIPLY'
    mix_math.location = (-400, -100)
    links.new(voronoi.outputs['Distance'], mix_math.inputs[0])
    links.new(noise.outputs['Fac'], mix_math.inputs[1])

    # Connect height map to displacement
    links.new(mix_math.outputs['Value'], disp.inputs['Height'])

    # Map Height to Color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 100)
    color_ramp.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[1].color = (*base_color_light, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.5
    links.new(mix_math.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

    # Map Height to Roughness (Cracks are less rough/shadowed, peaks are rougher)
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (-100, -150)
    map_range.inputs[3].default_value = 0.6 # To Min
    map_range.inputs[4].default_value = 0.9 # To Max
    links.new(mix_math.outputs['Value'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], principled.inputs['Roughness'])

    # === Step 4: Lighting Setup ===
    # Add a Sun light to emphasize the displacement shadows (if one doesn't exist)
    if not any(obj.type == 'LIGHT' and obj.data.type == 'SUN' for obj in bpy.data.objects):
        bpy.ops.object.light_add(type='SUN', location=(location[0] + 5, location[1] - 5, location[2] + 10))
        sun = bpy.context.active_object
        sun.name = "Displacement_Sun"
        sun.data.energy = 5.0 # High strength as shown in tutorial
        sun.rotation_euler = (0.785, 0, 0.785) # Angle for dramatic shadows

    return f"Created procedural displaced surface '{object_name}' at {location} (Cycles required to view displacement)."

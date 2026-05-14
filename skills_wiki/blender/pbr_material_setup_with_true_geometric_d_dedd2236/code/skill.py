def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "Displaced_Rock_Terrain",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.3, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true PBR displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Extensibility overrides (e.g. subsurf_levels, disp_scale).

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector
    import math

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Setup ===
    # True displacement requires Cycles to function correctly.
    scene.render.engine = 'CYCLES'

    # === Step 2: Base Geometry & Topology ===
    # Add a plane
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier to create dense micro-geometry
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps corners sharp
    subsurf.levels = kwargs.get("subsurf_levels", 6) # High density for viewport
    subsurf.render_levels = kwargs.get("subsurf_levels", 6)

    # === Step 3: Material & True Displacement Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to actually displace geometry, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Material Nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)

    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (100, 100)
    # Set roughness to a relatively high value for rock/dirt
    node_principled.inputs['Roughness'].default_value = 0.8

    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (100, -200)
    node_disp.inputs['Scale'].default_value = kwargs.get("disp_scale", 0.3)
    node_disp.inputs['Midlevel'].default_value = 0.5

    # Procedural texture map (Replacing downloaded image maps)
    node_noise = nodes.new(type='ShaderNodeTexNoise')
    node_noise.location = (-400, 0)
    node_noise.inputs['Scale'].default_value = 3.0
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.6
    
    node_voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    node_voronoi.location = (-400, -300)
    node_voronoi.inputs['Scale'].default_value = 6.0
    node_voronoi.feature = 'F1'
    node_voronoi.distance = 'EUCLIDEAN'

    # Mix nodes to create a complex height map
    node_mix = nodes.new(type='ShaderNodeMath')
    node_mix.operation = 'MULTIPLY'
    node_mix.location = (-150, -200)

    # ColorRamp to apply the requested color
    node_ramp = nodes.new(type='ShaderNodeValToRGB')
    node_ramp.location = (-150, 100)
    node_ramp.color_ramp.elements[0].position = 0.2
    node_ramp.color_ramp.elements[0].color = (material_color[0]*0.2, material_color[1]*0.2, material_color[2]*0.2, 1.0)
    node_ramp.color_ramp.elements[1].position = 0.8
    node_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    # Node Links
    links.new(node_noise.outputs['Fac'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_principled.inputs['Base Color'])
    
    links.new(node_noise.outputs['Fac'], node_mix.inputs[0])
    links.new(node_voronoi.outputs['Distance'], node_mix.inputs[1])
    
    links.new(node_mix.outputs['Value'], node_disp.inputs['Height'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    # Assign material to object
    if len(plane.data.materials) == 0:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat

    # === Step 4: Sun Lighting Context ===
    # True displacement is best viewed with directional lighting to cast micro-shadows
    sun_data = bpy.data.lights.new(name=f"{object_name}_SunLight", type='SUN')
    sun_data.energy = 5.0 # High energy to match tutorial
    sun_data.angle = 0.1 # Sharp shadows
    
    sun_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    # Position sun above and angle it
    sun_obj.location = Vector(location) + Vector((5.0, -5.0, 5.0))
    # Point the sun slightly down and sideways
    sun_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created displaced terrain '{object_name}' with procedural PBR material and Sun light at {location}."

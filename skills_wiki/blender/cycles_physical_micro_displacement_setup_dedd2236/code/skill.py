def create_procedural_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "ProceduralRockWall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with physical Cycles displacement and a procedural rock material.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the rock blocks in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # --- Setup Scene for Cycles ---
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'  # True displacement requires Cycles

    # --- Step 1: Base Geometry & Subdivision ---
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=10, y_segments=10, size=2.0)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Add Subdivision Surface Modifier for displacement resolution
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 6

    # --- Step 2: Material & Displacement Setup ---
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    
    # CRITICAL: Enable physical displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()  # Clear default nodes

    # Output Node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    # Principled BSDF
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (700, 200)
    principled.inputs['Roughness'].default_value = 0.85

    # Procedural Height Map Generation (Mimicking Rock Wall)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    # Noise for mapping distortion (makes rocks look organic)
    noise_dist = nodes.new('ShaderNodeTexNoise')
    noise_dist.inputs['Scale'].default_value = 4.0
    noise_dist.location = (-600, -200)

    # Add distortion to coordinate
    vec_add = nodes.new('ShaderNodeVectorMath')
    vec_add.operation = 'ADD'
    vec_add.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], vec_add.inputs[0])
    links.new(noise_dist.outputs['Color'], vec_add.inputs[1])

    # Voronoi for crack/rock pattern
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 2.0
    voronoi.location = (-200, 0)
    links.new(vec_add.outputs['Vector'], voronoi.inputs['Vector'])

    # Color Ramp to pinch the cracks (creates flat blocks with deep cuts)
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.05
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp.color_ramp.elements[1].position = 0.15
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    ramp.location = (0, 0)
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])

    # Macro Noise for overall height variation
    macro_noise = nodes.new('ShaderNodeTexNoise')
    macro_noise.inputs['Scale'].default_value = 1.0
    macro_noise.location = (0, -300)

    # Multiply rock pattern with macro noise
    math_mul = nodes.new('ShaderNodeMath')
    math_mul.operation = 'MULTIPLY'
    math_mul.location = (200, -100)
    links.new(ramp.outputs['Color'], math_mul.inputs[0])
    links.new(macro_noise.outputs['Fac'], math_mul.inputs[1])

    # Color mix for Base Color based on height
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0) # Dark shadows in cracks
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0) # Provided material color
    color_ramp.location = (400, 200)
    links.new(math_mul.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

    # Displacement Node Setup
    disp = nodes.new('ShaderNodeDisplacement')
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.4
    disp.location = (700, -200)
    links.new(math_mul.outputs['Value'], disp.inputs['Height'])

    # Final Links
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])

    # --- Step 3: Lighting Context ---
    # Add an angled Sun light to cast shadows across the displaced geometry
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_light = bpy.data.objects.new(name=f"{object_name}_SunLight", object_data=sun_data)
    scene.collection.objects.link(sun_light)
    sun_light.location = Vector(location) + Vector((5, -5, 5))
    sun_light.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created '{object_name}' with level 6 subdivision, physical Cycles displacement, and supporting Sun light."

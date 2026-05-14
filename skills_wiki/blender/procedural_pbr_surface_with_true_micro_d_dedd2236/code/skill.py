def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Terrain",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    subdivisions: int = 50,
    displacement_scale: float = 0.25,
    base_color_dark: tuple = (0.2, 0.15, 0.1, 1.0),
    base_color_light: tuple = (0.5, 0.45, 0.4, 1.0),
    **kwargs
) -> str:
    """
    Creates a highly subdivided procedural PBR surface with True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        subdivisions: Base grid density (higher = better displacement resolution).
        displacement_scale: Extrusion intensity for the displacement.
        base_color_dark: RGBA color for the deepest crevices.
        base_color_light: RGBA color for the high peaks.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    # 1. Setup Scene & Rendering Context
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # True displacement REQUIRES Cycles
    scene.render.engine = 'CYCLES'

    # 2. Safely create Grid Base Geometry
    initial_objects = set(scene.objects)
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=subdivisions, 
        y_subdivisions=subdivisions, 
        size=2.0, 
        location=location
    )
    new_objects = set(scene.objects) - initial_objects
    
    if not new_objects:
        return "Error: Failed to create base geometry."
        
    obj = list(new_objects)[0]
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Shade Smooth
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # Add Subdivision Surface Modifier to multiply geometry density
    subsurf = obj.modifiers.new(name="Displacement_Subsurf", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    subsurf.levels = 3        # Viewport level
    subsurf.render_levels = 4 # Render level (provides ~1M faces for ultra-detail)

    # 3. Build Procedural PBR Material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use True Displacement for this material
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Start fresh

    # Core Output Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (400, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (100, 0)
    links.new(principled.outputs['BSDF'], out_node.inputs['Surface'])
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (100, -250)
    disp_node.inputs['Scale'].default_value = displacement_scale
    disp_node.inputs['Midlevel'].default_value = 0.5
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Procedural Texture Generation (Simulating a scanned rock texture)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    # Voronoi provides the macro rocky blocks/cracks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, 150)
    voronoi.inputs['Scale'].default_value = 4.0
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    
    # Noise provides the micro gritty surface detail
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-800, -150)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    # Math Add: Combine macro and micro maps
    mix_math = nodes.new('ShaderNodeMath')
    mix_math.operation = 'ADD'
    mix_math.location = (-600, 0)
    links.new(voronoi.outputs['Distance'], mix_math.inputs[0])
    links.new(noise.outputs['Fac'], mix_math.inputs[1])
    
    # Math Multiply: Normalize the combined strength
    scale_math = nodes.new('ShaderNodeMath')
    scale_math.operation = 'MULTIPLY'
    scale_math.inputs[1].default_value = 0.5
    scale_math.location = (-400, 0)
    links.new(mix_math.outputs['Value'], scale_math.inputs[0])
    
    # Drive Height Data directly into Displacement Node
    links.new(scale_math.outputs['Value'], disp_node.inputs['Height'])
    
    # Drive Color via ColorRamp
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, 200)
    color_ramp.color_ramp.elements[0].color = base_color_dark
    color_ramp.color_ramp.elements[1].color = base_color_light
    links.new(scale_math.outputs['Value'], color_ramp.inputs[0])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # Drive Roughness via ColorRamp (Rocks are generally rough)
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-200, -50)
    rough_ramp.color_ramp.elements[0].position = 0.3
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].position = 0.8
    rough_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)
    links.new(scale_math.outputs['Value'], rough_ramp.inputs[0])
    links.new(rough_ramp.outputs['Color'], principled.inputs['Roughness'])
    
    # Assign Material
    obj.data.materials.append(mat)
    
    # 4. Add dramatic Sun Light to showcase the displacement geometry
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = 0.05 # Smaller angle = sharper shadows
    
    sun_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    # Position and angle the sun to cast long shadows across the texture
    sun_obj.location = (location[0] + 5, location[1] - 5, location[2] + 10)
    sun_obj.rotation_euler = (math.radians(60), 0, math.radians(45))

    return f"Created '{object_name}' (PBR Displaced Surface) at {location} with {subdivisions}x{subdivisions} resolution. Switched renderer to Cycles."

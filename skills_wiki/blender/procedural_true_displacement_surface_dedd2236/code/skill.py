def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "PBR_Rock_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 5.0,
    material_color: tuple = (0.25, 0.20, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a True Displacement PBR material and Sun light.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        material_color: (R, G, B) base color for the lighter areas of the texture.
        **kwargs: Additional overrides (e.g., subdivision_levels, displacement_scale).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # The tutorial explicitly switches to Cycles to enable True Displacement
    scene.render.engine = 'CYCLES'
    
    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add subdivision modifier to create dense geometry for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subdivisions = kwargs.get('subdivision_levels', 6)
    subsurf.levels = subdivisions
    subsurf.render_levels = subdivisions
    
    # === Step 2: Build Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
        
    # Output Node
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    
    # Principled BSDF Node
    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.location = (100, 0)
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    
    # Procedural Noise Setup (Replaces external downloaded image maps)
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.inputs['Scale'].default_value = 5.0
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.65
    node_noise.location = (-600, 0)
    
    # Base Color Map (Albedo)
    node_color_ramp = nodes.new('ShaderNodeValToRGB')
    node_color_ramp.color_ramp.elements[0].position = 0.3
    # Use the parameter color for highlights, and a darker version for crevices
    dark_color = (material_color[0] * 0.2, material_color[1] * 0.2, material_color[2] * 0.2, 1.0)
    node_color_ramp.color_ramp.elements[0].color = dark_color
    node_color_ramp.color_ramp.elements[1].position = 0.7
    node_color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    node_color_ramp.location = (-300, 200)
    links.new(node_noise.outputs['Fac'], node_color_ramp.inputs['Fac'])
    links.new(node_color_ramp.outputs['Color'], node_bsdf.inputs['Base Color'])
    
    # Roughness Map
    node_rough_ramp = nodes.new('ShaderNodeValToRGB')
    node_rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    node_rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    node_rough_ramp.location = (-300, 0)
    links.new(node_noise.outputs['Fac'], node_rough_ramp.inputs['Fac'])
    links.new(node_rough_ramp.outputs['Color'], node_bsdf.inputs['Roughness'])
    
    # Normal/Bump Map
    node_bump = nodes.new('ShaderNodeBump')
    node_bump.inputs['Distance'].default_value = 0.05
    node_bump.location = (-300, -200)
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])
    
    # True Displacement Map
    node_disp = nodes.new('ShaderNodeDisplacement')
    node_disp.inputs['Scale'].default_value = kwargs.get('displacement_scale', 0.2)
    node_disp.inputs['Midlevel'].default_value = 0.0
    node_disp.location = (100, -300)
    links.new(node_noise.outputs['Fac'], node_disp.inputs['Height'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    # === Step 3: Add Lighting ===
    # A strong directional light is required to reveal the deep displacement shadows
    bpy.ops.object.light_add(type='SUN', location=(location[0] + 5, location[1] - 5, location[2] + 5))
    sun = bpy.context.active_object
    sun.name = f"{object_name}_Sun"
    sun.data.energy = 5.0
    sun.data.angle = 0.2  # Slightly softer shadows
    
    # Point the sun directly at the surface
    direction = Vector(location) - sun.location
    sun.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    return f"Created '{object_name}' with True PBR Displacement and a companion Sun light."

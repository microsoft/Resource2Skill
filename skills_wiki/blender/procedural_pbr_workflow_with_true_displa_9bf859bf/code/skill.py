def create_pbr_displacement_material_object(
    scene_name: str = "Scene",
    object_name: str = "Displaced_PBR_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Creates a plane featuring a full procedural PBR node network and True Displacement.
    Automatically configures Cycles and Subdivision settings to support physical micro-geometry.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary color for the base texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import bpy
    import math
    from mathutils import Vector

    # --- Setup Scene & Engine ---
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.render.engine = 'CYCLES'
    
    # Enable Experimental features for Adaptive Subdivision
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass

    # --- Create Geometry ---
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- Setup Subdivision for Displacement ---
    mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.subdivision_type = 'CATMULL_CLARK'
    mod.levels = 6        # High baseline for reliable displacement across versions
    mod.render_levels = 6
    
    # Attempt to enable Cycles Adaptive Subdivision (Micro-polygons)
    try:
        obj.cycles.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # --- Create Material & Node Tree ---
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Crucial: Tell the material to use actual geometry displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinate Mapping (The Ctrl+T setup from tutorial)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Base Pattern (Procedural stand-in for downloaded image maps)
    base_pattern = nodes.new('ShaderNodeTexNoise')
    base_pattern.location = (-400, 0)
    base_pattern.inputs['Scale'].default_value = 5.0
    base_pattern.inputs['Detail'].default_value = 15.0
    links.new(mapping.outputs['Vector'], base_pattern.inputs['Vector'])

    # 1. Base Color Channel
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 400)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.02, 0.02, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    links.new(base_pattern.outputs['Fac'], color_ramp.inputs['Fac'])

    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (200, 400)
    hue_sat.inputs['Saturation'].default_value = 1.1
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

    # 2. Specular / Reflection Channel
    spec_ramp = nodes.new('ShaderNodeValToRGB')
    spec_ramp.location = (-100, 150)
    spec_ramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1.0)
    spec_ramp.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1.0)
    links.new(base_pattern.outputs['Fac'], spec_ramp.inputs['Fac'])
    
    # Version safe specular assignment
    spec_socket = bsdf.inputs.get('Specular IOR Level') or bsdf.inputs.get('Specular')
    if spec_socket:
        links.new(spec_ramp.outputs['Color'], spec_socket)

    # 3. Roughness (Inverted Gloss) Channel
    gloss_ramp = nodes.new('ShaderNodeValToRGB')
    gloss_ramp.location = (-100, -100)
    links.new(base_pattern.outputs['Fac'], gloss_ramp.inputs['Fac'])

    invert = nodes.new('ShaderNodeInvert')
    invert.location = (200, -100)
    links.new(gloss_ramp.outputs['Color'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # 4. Normal / Bump Channel
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -300)
    bump.inputs['Distance'].default_value = 0.05
    links.new(base_pattern.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # 5. True Displacement Channel
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (600, -300)
    disp.inputs['Scale'].default_value = 0.2
    disp.inputs['Midlevel'].default_value = 0.0  # Prevents overall object shifting
    links.new(base_pattern.outputs['Fac'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])

    # Assign Material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
        
    # --- Add Directional Lighting to reveal Displacement ---
    light_data = bpy.data.lights.new(name=f"{object_name}_SunLight", type='SUN')
    light_data.energy = 5.0
    light_data.angle = 0.05 # Sharp angle for crisp displacement shadows
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = Vector(location) + Vector((3, -3, 5))
    light_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created PBR Displacement plane '{object_name}' with accompanying Sun light at {location}."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.2),
    **kwargs,
) -> str:
    """
    Create a highly detailed surface utilizing a full PBR workflow and true displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the surface.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine Setup ===
    # True displacement is a Cycles-specific feature
    if scene.render.engine != 'CYCLES':
        scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for physical displacement geometry
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High level for dense geometry
    subsurf.render_levels = 6
    
    # Attempt to enable adaptive subdivision (available in Experimental Cycles)
    try:
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # === Step 3: Build PBR Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # CRITICAL: Tell the material to physically displace the mesh, not just fake it
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1200, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (800, 0)

    displacement = nodes.new(type='ShaderNodeDisplacement')
    displacement.location = (800, -400)
    displacement.inputs['Scale'].default_value = 0.15
    displacement.inputs['Midlevel'].default_value = 0.0

    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    # Mapping & UV Nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- Channel 1: Base Color (with Hue/Saturation adjustment) ---
    tex_color = nodes.new(type='ShaderNodeTexNoise')
    tex_color.location = (-100, 300)
    tex_color.inputs['Scale'].default_value = 5.0

    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (150, 300)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)

    hue_sat = nodes.new(type='ShaderNodeHueSaturation')
    hue_sat.location = (450, 300)

    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    links.new(tex_color.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], principled.inputs['Base Color'])

    # --- Channel 2: Gloss / Roughness (with Invert conversion) ---
    tex_rough = nodes.new(type='ShaderNodeTexNoise')
    tex_rough.location = (-100, 0)
    tex_rough.inputs['Scale'].default_value = 15.0
    tex_rough.inputs['Detail'].default_value = 10.0

    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (150, 0)

    links.new(mapping.outputs['Vector'], tex_rough.inputs['Vector'])
    links.new(tex_rough.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], principled.inputs['Roughness'])

    # --- Channel 3: Normal Map ---
    tex_normal = nodes.new(type='ShaderNodeTexVoronoi')
    tex_normal.location = (-100, -300)
    tex_normal.inputs['Scale'].default_value = 25.0

    normal_map = nodes.new(type='ShaderNodeNormalMap')
    normal_map.location = (450, -300)
    normal_map.inputs['Strength'].default_value = 1.0

    links.new(mapping.outputs['Vector'], tex_normal.inputs['Vector'])
    links.new(tex_normal.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], principled.inputs['Normal'])

    # --- Channel 4: True Displacement Map ---
    tex_disp = nodes.new(type='ShaderNodeTexNoise')
    tex_disp.location = (-100, -600)
    tex_disp.inputs['Scale'].default_value = 2.0
    tex_disp.inputs['Detail'].default_value = 15.0

    links.new(mapping.outputs['Vector'], tex_disp.inputs['Vector'])
    links.new(tex_disp.outputs['Fac'], displacement.inputs['Height'])

    # === Step 4: Add Lighting Context ===
    # A point light is added off-center to properly cast shadows across the displacement
    bpy.ops.object.light_add(type='POINT', radius=1.0, location=(location[0] + 1.5, location[1] - 1.5, location[2] + 2.0))
    light = bpy.context.active_object
    light.name = f"{object_name}_Showcase_Light"
    light.data.energy = 1500.0

    return f"Created '{object_name}' with Procedural PBR and True Displacement at {location}"

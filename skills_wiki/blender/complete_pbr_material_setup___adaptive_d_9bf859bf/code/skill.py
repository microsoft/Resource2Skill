def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a PBR Material Setup with Adaptive Displacement in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # === Step 1: Ensure Scene and Render Engine Settings ===
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except Exception:
        pass

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Apply Adaptive Subdivision Modifier
    subdiv_mod = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    subdiv_mod.subdivision_type = 'SIMPLE'
    try:
        subdiv_mod.use_adaptive_subdivision = True
    except AttributeError:
        # Fallback if adaptive is not available in the current context/version
        subdiv_mod.levels = 6
        subdiv_mod.render_levels = 6

    # === Step 3: Build PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Enable True Displacement at the material level
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinate & Mapping Setup
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Unified Value Node for Mapping Scale
    val_node = nodes.new('ShaderNodeValue')
    val_node.location = (-600, -200)
    val_node.outputs[0].default_value = 3.0
    links.new(val_node.outputs[0], mapping.inputs['Scale'])

    # Base Color Layer
    brick_tex = nodes.new('ShaderNodeTexBrick')
    brick_tex.location = (-100, 200)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0]*0.8, material_color[1]*0.8, material_color[2]*0.8, 1.0)
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])

    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (200, 200)
    links.new(brick_tex.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

    # Roughness Layer (Simulating Gloss Map Inversion Workflow)
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-100, -100)
    noise_tex.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])

    invert = nodes.new('ShaderNodeInvert')
    invert.location = (200, -100)
    links.new(noise_tex.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # Normal Layer
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -300)
    bump.inputs['Strength'].default_value = 0.6
    bump.inputs['Distance'].default_value = 0.1
    links.new(noise_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # True Displacement Layer
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (700, -300)
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.15
    links.new(brick_tex.outputs['Fac'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' with full procedural PBR displacement material at {location}"

def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a Full PBR Material Node Setup with True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color mapping for the procedural texture.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Ensure Cycles is enabled, as True Displacement requires it
    if not bpy.context.preferences.addons.get('cycles'):
        bpy.ops.preferences.addon_enable(module='cycles')
    
    # === Step 1: Render Engine Setup ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # Enable Adaptive Subdivision (Only works when Cycles is Experimental)
    obj.cycles.use_adaptive_subdivision = True

    # === Step 3: Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to use True Displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    # Principled BSDF
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Mapping & Coordinates (Mimicking Ctrl+T from Node Wrangler)
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Procedural Texture (Substituting external downloaded maps)
    # Using Voronoi to simulate a stony/cobble height map
    texture = nodes.new(type='ShaderNodeTexVoronoi')
    texture.location = (-400, 0)
    texture.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], texture.inputs['Vector'])

    # 1. Base Color Setup
    # Simulates the Albedo map. Adds Hue/Saturation node as shown in video tips.
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-100, 250)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1)
    links.new(texture.outputs['Distance'], color_ramp.inputs['Fac'])

    hue_sat = nodes.new(type='ShaderNodeHueSat')
    hue_sat.location = (200, 250)
    hue_sat.inputs['Saturation'].default_value = 1.1 # Slight boost
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], principled.inputs['Base Color'])

    # 2. Roughness Setup
    # Simulates the video's technique of converting a Gloss map to Roughness via Invert
    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (200, 50)
    links.new(texture.outputs['Distance'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], principled.inputs['Roughness'])

    # 3. Normal Setup
    # Converts grayscale data to Normal data
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (200, -150)
    bump.inputs['Strength'].default_value = 0.5
    links.new(texture.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # 4. True Displacement Setup
    # Plugs directly into output. Midlevel set to 0.0 as explicitly warned in tutorial.
    displacement = nodes.new(type='ShaderNodeDisplacement')
    displacement.location = (600, -300)
    displacement.inputs['Midlevel'].default_value = 0.0
    displacement.inputs['Scale'].default_value = 0.15 # Kept subtle to prevent tearing
    links.new(texture.outputs['Distance'], displacement.inputs['Height'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    return f"Created '{object_name}' with PBR node setup, True Displacement, and Adaptive Subdivision enabled."

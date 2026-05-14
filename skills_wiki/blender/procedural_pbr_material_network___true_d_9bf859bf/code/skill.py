def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Sphere",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a mesh demonstrating proper PBR node routing and True Displacement.
    Simulates image textures using procedural noise to demonstrate the video's node setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color modifier.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Add Subdivision Surface for Displacement to have geometry to work with
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4

    # Setup Cycles for True Displacement (as explicitly highlighted in the video)
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass # Fallback gracefully if running on standard feature set or older versions

    # === Step 2: Build the PBR Material Network ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Material")
    mat.use_nodes = True
    
    # Video Tip: Enable true displacement in material settings
    if hasattr(mat, 'cycles'):
        mat.cycles.displacement_method = 'DISPLACEMENT'
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    links.new(bsdf.outputs[0], output.inputs['Surface'])

    # Coordinate Mapping (Video Tip: Ctrl+T Mapping Setup)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])

    # --- BASE COLOR STREAM ---
    # Simulating a downloaded Color map
    noise_col = nodes.new('ShaderNodeTexNoise')
    noise_col.location = (-100, 300)
    noise_col.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], noise_col.inputs['Vector'])

    col_ramp = nodes.new('ShaderNodeValToRGB')
    col_ramp.location = (100, 300)
    col_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    col_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    links.new(noise_col.outputs['Fac'], col_ramp.inputs['Fac'])

    # Video Tip: Tweaking downloaded color textures with Hue/Saturation
    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (400, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1
    links.new(col_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

    # --- ROUGHNESS STREAM (Handling "Gloss" maps) ---
    # Simulating a downloaded Gloss map
    voronoi_gloss = nodes.new('ShaderNodeTexVoronoi')
    voronoi_gloss.location = (-100, 0)
    voronoi_gloss.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], voronoi_gloss.inputs['Vector'])

    # Video Tip: If you have a Gloss map, use an INVERT node to make it a Roughness map
    invert_gloss = nodes.new('ShaderNodeInvert')
    invert_gloss.location = (100, 0)
    links.new(voronoi_gloss.outputs['Distance'], invert_gloss.inputs['Color'])

    # Video Tip: Use a ColorRamp to clamp/tweak the roughness values
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (400, 0)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[1].position = 0.8
    links.new(invert_gloss.outputs['Color'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # --- NORMAL STREAM ---
    # Simulating a Normal/Bump detail map
    noise_norm = nodes.new('ShaderNodeTexNoise')
    noise_norm.location = (100, -300)
    noise_norm.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], noise_norm.inputs['Vector'])

    # Video Tip: Normal Map Node
    norm_map = nodes.new('ShaderNodeNormalMap')
    norm_map.location = (400, -300)
    norm_map.inputs['Strength'].default_value = 0.6
    links.new(noise_norm.outputs['Color'], norm_map.inputs['Color'])
    links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])

    # --- DISPLACEMENT STREAM ---
    # Simulating a Height/Displacement map
    disp_noise = nodes.new('ShaderNodeTexNoise')
    disp_noise.location = (400, -600)
    disp_noise.inputs['Scale'].default_value = 2.0
    disp_noise.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], disp_noise.inputs['Vector'])

    # Video Tip: Displacement Node setup (Midlevel and Scale adjustment)
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (900, -600)
    disp_node.inputs['Midlevel'].default_value = 0.5  # Prevents object from expanding/shifting globally
    disp_node.inputs['Scale'].default_value = 0.15    # Kept low for realism
    links.new(disp_noise.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    # === Step 3: Assign Material ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 4: Add Lighting to view the effect ===
    # Displacement and Normals require light to cast shadows
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 3.0
    light_data.angle = 0.1 # Sharp shadows to reveal displacement
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = Vector(location) + Vector((5, -5, 5))
    # Point light at the object
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created PBR Object '{object_name}' at {location} configured for True Displacement."

def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a complete PBR material pipeline with True Displacement on a plane.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range for the procedural texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy

    # Get the scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Configuration for True Displacement ===
    # True displacement requires Cycles. We also enable the Experimental feature set
    # which allows for Adaptive Subdivision if the user wishes to enable it.
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add a Subdivision Surface modifier to provide geometry for displacement
    subsurf = obj.modifiers.new(name="Subdivision_Displacement", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    # Use heavy manual subdivision to guarantee results in the viewport and render,
    # avoiding dependency on specific API versions for Adaptive Subdivision.
    subsurf.levels = 6
    subsurf.render_levels = 6
    
    # === Step 3: Material Setup & PBR Node Pipeline ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Tell Cycles to use true physical displacement instead of bump mapping
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes
    
    # Core Shader Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Mapping & Coordinates (UV/Generated mapping equivalent)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    # --- PBR Map 1: BASE COLOR (Simulating sRGB Image Texture) ---
    color_noise = nodes.new('ShaderNodeTexNoise')
    color_noise.location = (-400, 300)
    color_noise.inputs['Scale'].default_value = 10.0
    color_noise.inputs['Detail'].default_value = 5.0
    links.new(mapping.outputs['Vector'], color_noise.inputs['Vector'])
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 300)
    color_ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    # Darker variant of the input color
    color_ramp.color_ramp.elements[1].color = (material_color[0]*0.4, material_color[1]*0.4, material_color[2]*0.4, 1.0)
    links.new(color_noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # --- PBR Map 2: ROUGHNESS (Simulating Non-Color Roughness/Gloss Map) ---
    rough_noise = nodes.new('ShaderNodeTexNoise')
    rough_noise.location = (-400, 0)
    rough_noise.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], rough_noise.inputs['Vector'])
    
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-100, 0)
    # Remap noise to a rougher spectrum (0.4 to 0.8)
    rough_ramp.color_ramp.elements[0].color = (0.4, 0.4, 0.4, 1.0)
    rough_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)
    links.new(rough_noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    # --- PBR Map 3: NORMAL (Simulating Non-Color Normal Map) ---
    bump_tex = nodes.new('ShaderNodeTexVoronoi')
    bump_tex.location = (-400, -300)
    bump_tex.inputs['Scale'].default_value = 40.0
    links.new(mapping.outputs['Vector'], bump_tex.inputs['Vector'])
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (-100, -300)
    bump_node.inputs['Strength'].default_value = 0.6
    bump_node.inputs['Distance'].default_value = 0.05
    links.new(bump_tex.outputs['Distance'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])
    
    # --- PBR Map 4: TRUE DISPLACEMENT (Simulating Non-Color Displacement Map) ---
    disp_tex = nodes.new('ShaderNodeTexNoise')
    disp_tex.location = (400, -500)
    disp_tex.inputs['Scale'].default_value = 3.0
    disp_tex.inputs['Detail'].default_value = 15.0
    disp_tex.inputs['Roughness'].default_value = 0.6
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (800, -500)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = 0.15  # Controls physical height
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    # Link displacement directly to Material Output, NOT the BSDF
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Deselect all and select the newly created object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created PBR Object '{object_name}' with True Displacement at {location} (Requires Cycles viewport to view)"

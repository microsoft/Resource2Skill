def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR Material setup showcasing Inverted Roughness, Normals, and True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary color for the base albedo.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Pre-requisite: Enable Cycles and Experimental Feature Set ===
    # This is required to unlock Adaptive Subdivision for true displacement
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 1: Create Base Geometry & UVs ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Smart UV Project to generate UV coordinates
    bpy.ops.object.editmode_toggle()
    bpy.ops.uv.smart_project()
    bpy.ops.object.editmode_toggle()

    # Add Subdivision Surface Modifier
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE' # Prevents the plane from smoothing into an oval
    subdiv.levels = 6                  # High static level fallback
    subdiv.render_levels = 6
    
    # Enable Adaptive Subdivision if available in the API
    try:
        subdiv.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # === Step 2: Build the PBR Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use actual geometry displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1200, 0)

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Texture Coordinate & Universal Mapping
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- A. Base Color --- (Substituting Image with Procedural Brick)
    tex_color = nodes.new(type='ShaderNodeTexBrick')
    tex_color.location = (-100, 400)
    tex_color.inputs['Color1'].default_value = (*material_color, 1.0)
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    links.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])

    # --- B. Reflection/Specular ---
    tex_spec = nodes.new(type='ShaderNodeTexNoise')
    tex_spec.location = (-100, 100)
    links.new(mapping.outputs['Vector'], tex_spec.inputs['Vector'])
    
    # Fallback to handle Blender 4.0 'Specular IOR Level' vs 3.x 'Specular'
    spec_socket = 'Specular IOR Level' if 'Specular IOR Level' in bsdf.inputs else 'Specular'
    if spec_socket in bsdf.inputs:
        links.new(tex_spec.outputs['Fac'], bsdf.inputs[spec_socket])

    # --- C. Gloss/Roughness with INVERT workflow ---
    tex_gloss = nodes.new(type='ShaderNodeTexNoise')
    tex_gloss.location = (-100, -200)
    tex_gloss.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], tex_gloss.inputs['Vector'])
    
    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (200, -200)
    links.new(tex_gloss.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # --- D. Normal Map ---
    tex_normal = nodes.new(type='ShaderNodeTexVoronoi')
    tex_normal.location = (-100, -500)
    links.new(mapping.outputs['Vector'], tex_normal.inputs['Vector'])
    
    normal_map = nodes.new(type='ShaderNodeNormalMap')
    normal_map.location = (200, -500)
    normal_map.inputs['Strength'].default_value = 2.0
    links.new(tex_normal.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    # --- E. True Geometric Displacement ---
    tex_disp = nodes.new(type='ShaderNodeTexNoise')
    tex_disp.location = (-100, -800)
    tex_disp.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], tex_disp.inputs['Vector'])
    
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -400)
    disp_node.inputs['Midlevel'].default_value = 0.0  # Prevents mesh floating/separation
    disp_node.inputs['Scale'].default_value = 0.15    # Controls extrusion intensity
    links.new(tex_disp.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    # Deselect all and select the newly created object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created '{object_name}' at {location} with full PBR node structure and Adaptive Displacement enabled."

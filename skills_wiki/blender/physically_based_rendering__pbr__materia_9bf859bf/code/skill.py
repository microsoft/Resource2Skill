def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Showcase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a highly subdivided mesh demonstrating a fully wired PBR material architecture.
    (Approximates image textures with procedural noise to ensure reproducibility while 
    maintaining the exact utility node structure taught in the tutorial).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add subdivision for displacement to work physically
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps flat edges
    subsurf.levels = 6
    subsurf.render_levels = 6

    # === Step 2: Build PBR Material Architecture ===
    mat_name = f"{object_name}_PBR_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Set material settings for True Displacement (Cycles specific)
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Output & BSDF
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Mapping & Coordinates
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-800, 0)
    # Replicating the 'Value' node trick for uniform scaling mentioned in the video
    scale_val = nodes.new(type='ShaderNodeValue')
    scale_val.location = (-1000, -200)
    scale_val.outputs[0].default_value = 5.0
    
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(scale_val.outputs[0], mapping.inputs['Scale'])

    # -- Base Color Setup (Tinted Procedural Approximation) --
    color_tex = nodes.new(type='ShaderNodeTexNoise')
    color_tex.location = (-500, 300)
    color_tex.inputs['Scale'].default_value = 2.0
    
    # Hue Saturation Value node for color correction as taught in video
    hsv = nodes.new(type='ShaderNodeHueSaturation')
    hsv.location = (-250, 300)
    hsv.inputs['Color'].default_value = (*material_color, 1.0) # Base tint
    
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])
    links.new(color_tex.outputs['Fac'], hsv.inputs['Value'])
    links.new(hsv.outputs['Color'], bsdf.inputs['Base Color'])

    # -- Gloss -> Roughness Workflow Setup --
    # Video uses a Gloss map and inverts it for the Roughness socket
    gloss_tex = nodes.new(type='ShaderNodeTexNoise')
    gloss_tex.location = (-500, 0)
    gloss_tex.inputs['Scale'].default_value = 15.0
    
    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (-250, 0)
    
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])
    links.new(gloss_tex.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # -- Normal Map Setup --
    norm_tex = nodes.new(type='ShaderNodeTexVoronoi')
    norm_tex.location = (-500, -300)
    norm_tex.inputs['Scale'].default_value = 20.0
    
    norm_map = nodes.new(type='ShaderNodeNormalMap')
    norm_map.location = (-250, -300)
    norm_map.inputs['Strength'].default_value = 0.5
    
    links.new(mapping.outputs['Vector'], norm_tex.inputs['Vector'])
    links.new(norm_tex.outputs['Color'], norm_map.inputs['Color'])
    links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])

    # -- Displacement Setup --
    disp_tex = nodes.new(type='ShaderNodeTexNoise')
    disp_tex.location = (-500, -600)
    disp_tex.inputs['Scale'].default_value = 3.0
    
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (-250, -600)
    disp_node.inputs['Scale'].default_value = 0.1 # Keep scale low as advised in video
    disp_node.inputs['Midlevel'].default_value = 0.0 # Set midlevel to 0 to prevent mesh shifting
    
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])
    links.new(disp_tex.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    # Switch to Cycles to allow displacement to be visible
    scene.render.engine = 'CYCLES'

    # Ensure smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    return f"Created PBR material architecture on '{object_name}' at {location}. Cycles engine activated for True Displacement."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Adaptive_Bricks",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.15),  # Base brick color
    **kwargs,
) -> str:
    """
    Create a plane with a fully configured PBR material and Adaptive Displacement.
    Mimics the image-texture workflow procedurally (Color, Inverted Gloss, Bump, Displacement).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the bricks.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    # Get the active scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Engine Setup for Adaptive Subdivision ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # Enable Adaptive Subdivision (Only active in Cycles Experimental)
    try:
        obj.cycles.use_adaptive_subdivision = True
    except Exception as e:
        print(f"Warning: Could not enable adaptive subdivision: {e}")

    # === Step 3: Build PBR Material Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Tell the material to use True Displacement
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # --- Output & BSDF ---
    mat_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_output.location = (1000, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)

    # --- Coordinates & Mapping ---
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)

    # --- Procedural Textures (Simulating Image Maps) ---
    # 1. Base Color / Displacement Map
    brick_tex = nodes.new(type='ShaderNodeTexBrick')
    brick_tex.location = (-300, 200)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0]*0.6, material_color[1]*0.6, material_color[2]*0.6, 1.0)
    brick_tex.inputs['Mortar'].default_value = (0.5, 0.5, 0.5, 1.0)
    brick_tex.inputs['Scale'].default_value = 3.0

    # 2. "Gloss" Map (Using Noise to simulate surface imperfections)
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    noise_tex.location = (-300, -150)
    noise_tex.inputs['Scale'].default_value = 25.0
    noise_tex.inputs['Detail'].default_value = 5.0

    # --- PBR Conversion Nodes ---
    # Convert "Gloss" to "Roughness" via Invert node (as taught in the tutorial)
    invert_node = nodes.new(type='ShaderNodeInvert')
    invert_node.location = (0, -150)
    
    # Map range to keep roughness realistic (not perfectly glossy or completely matte)
    map_range = nodes.new(type='ShaderNodeMapRange')
    map_range.location = (200, -150)
    map_range.inputs[3].default_value = 0.3 # To Min
    map_range.inputs[4].default_value = 0.8 # To Max

    # Bump Node (Simulating a Normal Map)
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (200, -400)
    bump_node.inputs['Strength'].default_value = 0.6
    bump_node.inputs['Distance'].default_value = 0.05

    # Displacement Node
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (600, -300)
    disp_node.inputs['Midlevel'].default_value = 0.0  # Set to 0 to prevent geometry shift
    disp_node.inputs['Scale'].default_value = 0.1     # Scaled down for realism

    # === Step 4: Link Everything Together ===
    # Vectors
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])

    # Color
    links.new(brick_tex.outputs['Color'], principled.inputs['Base Color'])

    # Roughness
    links.new(noise_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], principled.inputs['Roughness'])

    # Bump / Normal
    links.new(brick_tex.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled.inputs['Normal'])

    # Displacement
    links.new(brick_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    # Final Outputs
    links.new(principled.outputs['BSDF'], mat_output.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], mat_output.inputs['Displacement'])

    return f"Created '{object_name}' at {location}. Cycles engine set to Experimental for Adaptive Subdivision."

def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create an Adaptive Displacement PBR Plane in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range for the placeholder texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Context for Adaptive Subdivision ===
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Fallback if API changes in future versions

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for Adaptive Subdiv
    subdiv = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE' # Keeps edges square
    try:
        subdiv.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # === Step 3: Generate Placeholder Images for PBR Maps ===
    # This prevents magenta/black missing texture errors
    def create_placeholder(name, color, is_data=True):
        # Create a 16x16 image
        img = bpy.data.images.new(name, width=16, height=16)
        # R, G, B, A list multiplied by pixel count (16x16 = 256)
        img.pixels = list(color) * 256 
        if is_data:
            img.colorspace_settings.name = 'Non-Color'
        else:
            img.colorspace_settings.name = 'sRGB'
        return img

    img_col = create_placeholder(f"{object_name}_Color", (material_color[0], material_color[1], material_color[2], 1.0), is_data=False)
    img_refl = create_placeholder(f"{object_name}_Reflection", (0.5, 0.5, 0.5, 1.0), is_data=True)
    img_gloss = create_placeholder(f"{object_name}_Gloss", (0.7, 0.7, 0.7, 1.0), is_data=True)
    img_norm = create_placeholder(f"{object_name}_Normal", (0.5, 0.5, 1.0, 1.0), is_data=True) # Flat normal
    img_disp = create_placeholder(f"{object_name}_Displacement", (0.0, 0.0, 0.0, 1.0), is_data=True)

    # === Step 4: Build PBR Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Enable displacement calculation on the material
    try:
        mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    except AttributeError:
        pass
    try:
        mat.displacement_method = 'DISPLACEMENT_BUMP'
    except AttributeError:
        pass

    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Shader Nodes
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_out.location = (1200, 0)
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (800, 0)
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    # Mapping & Coordinates
    node_tc = nodes.new(type='ShaderNodeTexCoord')
    node_tc.location = (-800, 0)
    
    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-600, 0)
    links.new(node_tc.outputs['UV'], node_mapping.inputs['Vector'])

    # Uniform Scale Control (Bonus tip from video)
    node_scale_val = nodes.new(type='ShaderNodeValue')
    node_scale_val.location = (-800, -200)
    node_scale_val.label = "Uniform UV Scale"
    node_scale_val.outputs['Value'].default_value = 1.0
    links.new(node_scale_val.outputs['Value'], node_mapping.inputs['Scale'])

    # Helper to cleanly add image nodes
    def add_image_node(img, label, loc_y):
        node = nodes.new(type='ShaderNodeTexImage')
        node.image = img
        node.label = label
        node.location = (-300, loc_y)
        links.new(node_mapping.outputs['Vector'], node.inputs['Vector'])
        return node

    # Add Map Nodes
    node_img_col = add_image_node(img_col, "Color Map", 300)
    node_img_refl = add_image_node(img_refl, "Reflection Map", 0)
    node_img_gloss = add_image_node(img_gloss, "Gloss Map", -300)
    node_img_norm = add_image_node(img_norm, "Normal Map", -600)
    node_img_disp = add_image_node(img_disp, "Displacement Map", -900)

    # Base Color Branch (with Hue/Sat bonus tip)
    node_hsv = nodes.new(type='ShaderNodeHueSaturation')
    node_hsv.location = (200, 300)
    links.new(node_img_col.outputs['Color'], node_hsv.inputs['Color'])
    links.new(node_hsv.outputs['Color'], node_bsdf.inputs['Base Color'])

    # Specular / Reflection Branch
    # Handles Blender 4.0+ 'Specular IOR Level' vs older 'Specular'
    spec_input = node_bsdf.inputs.get('Specular IOR Level') or node_bsdf.inputs.get('Specular')
    if spec_input:
        links.new(node_img_refl.outputs['Color'], spec_input)

    # Roughness / Gloss Branch (Invert node workflow)
    node_invert = nodes.new(type='ShaderNodeInvert')
    node_invert.location = (200, -300)
    links.new(node_img_gloss.outputs['Color'], node_invert.inputs['Color'])
    links.new(node_invert.outputs['Color'], node_bsdf.inputs['Roughness'])

    # Normal Branch
    node_normal_map = nodes.new(type='ShaderNodeNormalMap')
    node_normal_map.location = (200, -600)
    links.new(node_img_norm.outputs['Color'], node_normal_map.inputs['Color'])
    links.new(node_normal_map.outputs['Normal'], node_bsdf.inputs['Normal'])

    # Displacement Branch
    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (800, -500)
    node_disp.inputs['Midlevel'].default_value = 0.0 # From tutorial, avoids object shifting
    node_disp.inputs['Scale'].default_value = 0.1    # From tutorial, controls displacement intensity
    links.new(node_img_disp.outputs['Color'], node_disp.inputs['Height'])
    links.new(node_disp.outputs['Displacement'], node_out.inputs['Displacement'])

    return f"Created '{object_name}' with PBR template material and Adaptive Subdivision setup at {location}."

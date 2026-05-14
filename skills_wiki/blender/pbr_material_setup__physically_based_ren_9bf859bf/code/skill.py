def create_pbr_material_setup(
    object_name: str = "PBR_Object",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_paths: dict = None, # Dict of {'COL': 'path/to/color.jpg', ...}
    material_name: str = "PBR_Material",
    normal_strength: float = 1.0,
    displacement_scale: float = 0.05,
    displacement_midlevel: float = 0.5,
    subdivision_levels_viewport: int = 2,
    subdivision_levels_render: int = 2,
    use_adaptive_subdivision: bool = False, # Requires Cycles Experimental
    scene_name: str = "Scene",
    **kwargs,
) -> str:
    """
    Creates a plane, adds a new material, and sets up a PBR shader node tree
    with provided image textures, mimicking Node Wrangler's Principled Texture Setup.

    Args:
        object_name (str): Name for the created mesh object.
        location (tuple): (x, y, z) world-space position for the object.
        scale (float): Uniform scale factor for the object.
        texture_paths (dict): A dictionary where keys are map types (e.g., 'COL', 'NRM', 'GLOSS', 'REFL', 'DISP')
                              and values are full file paths to the image textures.
        material_name (str): Name for the created Blender material.
        normal_strength (float): Strength of the Normal Map node.
        displacement_scale (float): Scale input for the Displacement node.
        displacement_midlevel (float): Midlevel input for the Displacement node.
        subdivision_levels_viewport (int): Viewport levels for Subdivision Surface modifier.
        subdivision_levels_render (int): Render levels for Subdivision Surface modifier.
        use_adaptive_subdivision (bool): If True, enables adaptive subdivision on the Subsurf modifier.
                                         Requires Cycles render engine and 'Experimental' feature set.
        scene_name (str): Name of the target scene (default is "Scene").
        **kwargs: Additional keyword arguments for future expansion or overrides.

    Returns:
        str: Status message describing the outcome of the operation.
    """
    import bpy
    import os
    from mathutils import Vector

    if texture_paths is None:
        texture_paths = {}

    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        return f"Error: Scene '{scene_name}' not found."

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- 2. Create Material ---
    mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes (except Principled BSDF and Material Output)
    for node in nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(node)

    principled_bsdf = nodes.get("Principled BSDF")
    if not principled_bsdf:
        principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.name = "Principled BSDF"
    
    material_output = nodes.get("Material Output")
    if not material_output:
        material_output = nodes.new('ShaderNodeOutputMaterial')
        material_output.name = "Material Output"

    # Arrange default nodes
    principled_bsdf.location = (400, 0)
    material_output.location = (600, 0)
    
    # Ensure BSDF is connected to Surface
    if not principled_bsdf.outputs['BSDF'].is_linked:
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # --- 3. Add Mapping and Texture Coordinate Nodes ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    
    # Add a reroute node for cleaner connections from mapping (mimics Node Wrangler layout)
    reroute_mapping = nodes.new('NodeReroute')

    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    reroute_mapping.location = (-400, 0) # Adjust as needed for better visual flow

    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], reroute_mapping.inputs[0]) # Connect mapping to reroute

    # --- Helper to load image and connect to mapping via reroute ---
    def setup_image_node(filepath, node_name, label, y_offset, color_space_name='Non-Color'):
        if not filepath or not os.path.exists(filepath):
            print(f"Warning: Texture file not found for {label}: {filepath}")
            return None
        
        img_tex = nodes.new('ShaderNodeTexImage')
        img_tex.image = bpy.data.images.load(filepath, check_existing=True)
        img_tex.name = node_name
        img_tex.label = label
        img_tex.image.colorspace_settings.name = color_space_name
        img_tex.location = (-50, y_offset) # Position closer to principled BSDF
        links.new(reroute_mapping.outputs[0], img_tex.inputs['Vector']) # Connect reroute to image texture
        return img_tex

    current_y_offset = 300 # Starting Y position for texture nodes
    
    # --- Base Color Map (Albedo) ---
    col_map = setup_image_node(texture_paths.get('COL'), "Texture_BaseColor", "Base Color", current_y_offset, 'sRGB')
    if col_map:
        links.new(col_map.outputs['Color'], principled_bsdf.inputs['Base Color'])
    current_y_offset -= 150

    # --- Roughness / Gloss Map ---
    rough_map = None
    if 'ROUGH' in texture_paths:
        rough_map = setup_image_node(texture_paths['ROUGH'], "Texture_Roughness", "Roughness", current_y_offset, 'Non-Color')
    elif 'GLOSS' in texture_paths: # If gloss map is provided, use it and invert
        rough_map = setup_image_node(texture_paths['GLOSS'], "Texture_Gloss", "Gloss", current_y_offset, 'Non-Color')
        
    if rough_map:
        if 'GLOSS' in texture_paths: 
            invert_node = nodes.new('ShaderNodeInvert')
            invert_node.location = (rough_map.location.x + 200, rough_map.location.y)
            links.new(rough_map.outputs['Color'], invert_node.inputs['Color'])
            links.new(invert_node.outputs['Color'], principled_bsdf.inputs['Roughness'])
        else:
            links.new(rough_map.outputs['Color'], principled_bsdf.inputs['Roughness'])
    current_y_offset -= 150

    # --- Normal Map ---
    nrm_map = setup_image_node(texture_paths.get('NRM'), "Texture_Normal", "Normal", current_y_offset, 'Non-Color')
    if nrm_map:
        normal_map_node = nodes.new('ShaderNodeNormalMap')
        normal_map_node.location = (nrm_map.location.x + 200, nrm_map.location.y)
        normal_map_node.inputs['Strength'].default_value = normal_strength
        links.new(nrm_map.outputs['Color'], normal_map_node.inputs['Color'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
    current_y_offset -= 150

    # --- Reflection / Specular Map ---
    refl_map = setup_image_node(texture_paths.get('REFL'), "Texture_Reflection", "Reflection", current_y_offset, 'Non-Color')
    if refl_map:
        # Connect to Specular input. Principled BSDF's specular expects 0-1.
        links.new(refl_map.outputs['Color'], principled_bsdf.inputs['Specular'])
    current_y_offset -= 150

    # --- Displacement Map ---
    disp_map = setup_image_node(texture_paths.get('DISP'), "Texture_Displacement", "Displacement", current_y_offset, 'Non-Color')
    if disp_map:
        displacement_node = nodes.new('ShaderNodeDisplacement')
        displacement_node.location = (disp_map.location.x + 200, disp_map.location.y)
        displacement_node.inputs['Scale'].default_value = displacement_scale
        displacement_node.inputs['Midlevel'].default_value = displacement_midlevel
        links.new(disp_map.outputs['Color'], displacement_node.inputs['Height'])
        links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

        # --- Enable true Displacement in Material Settings for Cycles ---
        if bpy.context.scene.render.engine == 'CYCLES':
            mat.cycles.displacement_method = 'DISPLACEMENT'
            
            # Add Subdivision Surface modifier for true displacement
            subdiv_mod = obj.modifiers.get("Subdivision")
            if not subdiv_mod: # Add if not present
                subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
            
            subdiv_mod.levels = subdivision_levels_viewport
            subdiv_mod.render_levels = subdivision_levels_render
            subdiv_mod.subdivision_type = 'SIMPLE' # Often preferred for displacement for sharp detail

            if use_adaptive_subdivision:
                # Adaptive subdivision requires experimental feature set in Cycles
                bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                subdiv_mod.use_adaptive_subdivision = True
                # dicing_scale can be adjusted: e.g., subdiv_mod.dicing_scale = 0.5
                # The default for dicing scale is usually 1.0. Lower values give more detail.

    return f"Created PBR material '{material_name}' on object '{object_name}' with associated textures."


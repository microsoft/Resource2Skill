def create_pbr_material_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Textured_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_folder_path: str = "",  # IMPORTANT: User must provide a valid absolute path to the texture folder
    texture_base_name: str = "BricksOldWhiteWashedRed001",
    resolution: str = "3K", # e.g., "3K", "8K" for texture file names
    displacement_strength: float = 0.02, # Strength of the displacement effect
    normal_strength: float = 1.0, # Strength of the normal map effect
    subdivision_level_render: int = 4, # Render subdivision level for displacement
    subdivision_level_viewport: int = 2, # Viewport subdivision level for displacement
    use_hsv: bool = False, # Whether to add a Hue/Saturation node for Base Color
    hsv_hue: float = 0.5,
    hsv_saturation: float = 1.0,
    hsv_value: float = 1.0,
    use_rgb_curves: bool = False, # Whether to add an RGB Curves node for Base Color
    **kwargs,
) -> str:
    """
    Create a plane object with a PBR material setup using image textures.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        texture_folder_path: Absolute path to the folder containing the PBR texture files.
                             E.g., "C:/Users/YourUser/Blender/Textures/_STONE/BricksOldWhiteWashedRed001"
                             Note: This must be a valid path on your system.
        texture_base_name: The base name of the texture files without suffixes or resolution.
                           E.g., "BricksOldWhiteWashedRed001" if files are like "BricksOldWhiteWashedRed001_COL_3K.jpg".
        resolution: The resolution suffix for the texture files, e.g., "3K", "8K".
        displacement_strength: Strength of the displacement effect.
        normal_strength: Strength of the normal map effect.
        subdivision_level_render: Render subdivision level for the Subdivision Surface modifier (for displacement).
        subdivision_level_viewport: Viewport subdivision level for the Subdivision Surface modifier (for displacement).
        use_hsv: If True, adds a Hue/Saturation/Value node for base color adjustment.
        hsv_hue: Hue value for the HSV node (0.0 to 1.0).
        hsv_saturation: Saturation value for the HSV node (0.0 to 2.0).
        hsv_value: Value (brightness) for the HSV node (0.0 to 2.0).
        use_rgb_curves: If True, adds an RGB Curves node for base color adjustment (manual curve editing required in UI).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_Textured_Plane' at (0, 0, 0) with PBR material."
    """
    # --- Imports ---
    import bpy
    import os
    from mathutils import Vector

    # --- Scene and Object Setup ---
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create Base Geometry (Plane)
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location,
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add a Subdivision Surface modifier for displacement
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.render_levels = subdivision_level_render
    subdiv_mod.levels = subdivision_level_viewport
    subdiv_mod.subdivision_type = 'SIMPLE' # Important for retaining sharp details of displacement

    # --- Create Material ---
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True

    # Remove all existing materials from the object and add the new one
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear existing nodes (except Principled BSDF and Material Output)
    for node in nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(node)

    principled_bsdf = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
    material_output = next((node for node in nodes if node.type == 'OUTPUT_MATERIAL'), None)

    # Ensure Principled BSDF and Material Output exist and are positioned
    if not principled_bsdf:
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (0, 0)

    if not material_output:
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (400, 0)

    # Link Principled BSDF to Material Output's Surface input
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # --- Texture Loading and Node Creation ---
    tex_map_config = {
        "COL": {"suffix": "_COL_", "ext": ".jpg", "colorspace": 'sRGB'},
        "GLOSS": {"suffix": "_GLOSS_", "ext": ".jpg", "colorspace": 'Non-Color'}, # Used for Roughness
        "NRM": {"suffix": "_NRM_", "ext": ".png", "colorspace": 'Non-Color'},
        "DISP": {"suffix": "_DISP_", "ext": ".jpg", "colorspace": 'Non-Color'},
        "REFL": {"suffix": "_REFL_", "ext": ".jpg", "colorspace": 'Non-Color'}, # Used for Specular
    }

    tex_files_found = {}
    for map_type, config in tex_map_config.items():
        path = os.path.join(texture_folder_path, f"{texture_base_name}{config['suffix']}{resolution}{config['ext']}")
        if os.path.exists(path):
            tex_files_found[map_type] = {'path': path, 'colorspace': config['colorspace']}
        else:
            print(f"Warning: Texture file not found for {map_type} at {path}")

    image_nodes = {}
    x_pos_images = -1000
    y_pos_start = 600
    y_offset = -300

    # Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (x_pos_images - 400, y_pos_start + 100)
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (x_pos_images - 200, y_pos_start + 100)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])


    current_y_for_images = y_pos_start
    for map_type in ["COL", "REFL", "GLOSS", "NRM", "DISP"]: # Order for visual organization
        if map_type in tex_files_found:
            config = tex_files_found[map_type]
            img_node = nodes.new(type='ShaderNodeTexImage')
            img_node.location = (x_pos_images, current_y_for_images)
            img_node.name = f"Image_{map_type}"
            try:
                img_node.image = bpy.data.images.load(config['path'])
            except RuntimeError as e:
                print(f"Error loading image {config['path']}: {e}")
                nodes.remove(img_node)
                continue

            img_node.image.colorspace_settings.name = config['colorspace']
            image_nodes[map_type] = img_node
            links.new(mapping.outputs['Vector'], img_node.inputs['Vector'])
            current_y_for_images += y_offset # Move down for next node

    # --- Connect PBR Maps to Principled BSDF ---
    x_pos_utility = -300

    # Base Color
    if "COL" in image_nodes:
        output_socket = image_nodes["COL"].outputs['Color']
        if use_hsv:
            hsv_node = nodes.new(type='ShaderNodeHueSaturation')
            hsv_node.location = (x_pos_utility, principled_bsdf.location.y + 300)
            hsv_node.inputs['Hue'].default_value = hsv_hue
            hsv_node.inputs['Saturation'].default_value = hsv_saturation
            hsv_node.inputs['Value'].default_value = hsv_value
            links.new(output_socket, hsv_node.inputs['Color'])
            output_socket = hsv_node.outputs['Color']
        elif use_rgb_curves:
            rgb_curves_node = nodes.new(type='ShaderNodeRGBCurves')
            rgb_curves_node.location = (x_pos_utility, principled_bsdf.location.y + 300)
            links.new(output_socket, rgb_curves_node.inputs['Color'])
            output_socket = rgb_curves_node.outputs['Color']
        
        links.new(output_socket, principled_bsdf.inputs['Base Color'])
    else:
        principled_bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1) # Default to grey

    # Specular (using REFL map directly)
    if "REFL" in image_nodes:
        links.new(image_nodes["REFL"].outputs['Color'], principled_bsdf.inputs['Specular'])
        principled_bsdf.inputs['Specular Tint'].default_value = 0.0 # Clear tint for raw specular map
        print(f"Note: Using REFL map for Specular.")
    else:
        principled_bsdf.inputs['Specular'].default_value = 0.5 # Default if no specular map

    # Roughness (using GLOSS map and Invert node)
    if "GLOSS" in image_nodes:
        invert_node = nodes.new(type='ShaderNodeInvert')
        invert_node.location = (x_pos_utility, principled_bsdf.location.y - 100)
        links.new(image_nodes["GLOSS"].outputs['Color'], invert_node.inputs['Color'])
        links.new(invert_node.outputs['Color'], principled_bsdf.inputs['Roughness'])
        print(f"Note: Using GLOSS map inverted for Roughness.")
    else:
        principled_bsdf.inputs['Roughness'].default_value = 0.5 # Default if no gloss/roughness map


    # Normal Map
    if "NRM" in image_nodes:
        normal_map_node = nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (x_pos_utility, principled_bsdf.location.y - 400)
        normal_map_node.inputs['Strength'].default_value = normal_strength
        links.new(image_nodes["NRM"].outputs['Color'], normal_map_node.inputs['Color'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # Displacement Map
    if "DISP" in image_nodes:
        disp_node = nodes.new(type='ShaderNodeDisplacement')
        disp_node.location = (x_pos_utility, principled_bsdf.location.y - 700)
        disp_node.inputs['Scale'].default_value = displacement_strength # Use Scale for strength
        disp_node.inputs['Midlevel'].default_value = 0.0 # To prevent object shift
        links.new(image_nodes["DISP"].outputs['Color'], disp_node.inputs['Height'])
        links.new(disp_node.outputs['Displacement'], material_output.inputs['Displacement'])

        # --- Cycles and Adaptive Subdivision Setup for Displacement ---
        # Note: This part modifies scene/modifier settings and works best in Cycles.
        if bpy.context.scene.render.engine == 'CYCLES':
            # Set Cycles Feature Set to Experimental for Adaptive Subdivision
            if bpy.context.scene.cycles.feature_set != 'EXPERIMENTAL':
                bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                print("Note: Cycles feature set changed to 'Experimental' for Adaptive Subdivision.")
            
            # Enable Adaptive Subdivision on the modifier
            if subdiv_mod:
                subdiv_mod.use_adaptive_subdivision = True
                print(f"Note: Adaptive Subdivision enabled on modifier '{subdiv_mod.name}'.")
            
            # Set material displacement method
            mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
            print(f"Note: Material displacement method set to 'DISPLACEMENT_AND_BUMP' for material '{mat.name}'.")
        else:
            print("Warning: Displacement map works best in Cycles. Currently using EEVEE/Workbench. "
                  "Switch to Cycles and enable 'Experimental' feature set for full effect.")

    # --- Finalize ---
    # Select the newly created object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created '{object_name}' at {location} with PBR material from '{texture_base_name}'."


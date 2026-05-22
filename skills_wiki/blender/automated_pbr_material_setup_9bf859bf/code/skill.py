def create_pbr_material_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    pbr_texture_base_path: str = "C:/path/to/your/BricksOldWhiteWashedRed001/",
    displacement_scale: float = 0.05,
    normal_strength: float = 1.0,
    subdivision_levels: int = 4, # For viewport and render in simple mode
    enable_adaptive_subdivision: bool = True,
    dicing_scale: float = 0.5, # For adaptive subdivision
    **kwargs,
) -> str:
    """
    Creates a plane with an automated PBR material setup using Node Wrangler's
    principled_texture_setup operator. Requires specific PBR texture files
    to be present at the given base path and Node Wrangler to be enabled.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        pbr_texture_base_path: Absolute path to the folder containing PBR texture files.
                                E.g., "C:/Users/YourName/Blender/Textures/BricksOldWhiteWashedRed001/"
                                Files expected: *_COL_3K.jpg, *_NRM_3K.png, *_GLOSS_3K.jpg,
                                                *_DISP_3K.jpg, *_REFL_3K.jpg (or similar).
        displacement_scale: Strength of the displacement effect.
        normal_strength: Strength of the normal map effect.
        subdivision_levels: Levels of subdivision for the Subdivision Surface modifier.
        enable_adaptive_subdivision: Whether to enable adaptive subdivision (requires Cycles
                                     and Experimental feature set).
        dicing_scale: Dicing scale for adaptive subdivision.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_Plane' at (0, 0, 0) with PBR material."
    """
    import bpy
    import os
    from mathutils import Vector

    # Check if Node Wrangler is enabled
    if not bpy.app.addon_utils.is_enabled("node_wrangler"):
        print("Warning: Node Wrangler add-on is not enabled. PBR setup will not be fully automated.")
        # Attempt to enable it, might require user interaction or Blender restart
        try:
            bpy.ops.preferences.addon_enable(module="node_wrangler")
        except Exception as e:
            print(f"Failed to enable Node Wrangler: {e}. Please enable it manually.")
            return "Failed to setup PBR material: Node Wrangler not enabled."

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Geometry (Plane) ===
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.object
    obj.name = object_name

    # Apply scale and location
    obj.scale = (scale, scale, scale)
    obj.location = Vector(location)

    # Ensure the plane is unwrapped (Smart UV Project as default by Node Wrangler's Ctrl+T)
    # The principled_texture_setup operator usually adds mapping and texture coordinate nodes,
    # and defaults to UV output if available. A basic unwrap is good to ensure this.
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project() # The video mentioned Smart UV Project
    bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 2: Build Material using Node Wrangler ===
    # Create a new material if none exists or replace existing
    if not obj.data.materials:
        mat = bpy.data.materials.new(name=f"{object_name}_Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]
        mat.name = f"{object_name}_Material"

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear existing nodes for a clean setup (optional, but good for robust automation)
    for node in nodes:
        nodes.remove(node)

    # Add Principled BSDF and Material Output nodes
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Find relevant texture files in the specified base path
    texture_files = []
    map_keywords = ["COL", "NRM", "GLOSS", "DISP", "REFL"] # Common PBR maps
    for keyword in map_keywords:
        for ext in ['.jpg', '.png', '.tif']: # Check common extensions
            file_name = f"{os.path.basename(pbr_texture_base_path.rstrip('/\\'))}_{keyword}_3K{ext}"
            full_path = os.path.join(pbr_texture_base_path, file_name)
            if os.path.exists(full_path):
                texture_files.append(full_path)
                break # Found one, move to next keyword

    if not texture_files:
        return f"Failed to setup PBR material: No PBR texture files found at {pbr_texture_base_path}"

    # Use Node Wrangler's principled_texture_setup operator
    # This operator does the heavy lifting: adds Image Texture nodes, Mapping,
    # Texture Coordinate, Normal Map, Invert (for gloss), and Displacement nodes.
    # It also sets correct color spaces.
    bpy.context.view_layer.objects.active = obj # Ensure object is active for operator
    bpy.context.area.type = 'NODE_EDITOR' # Set active area to Node Editor
    bpy.ops.node.select_all(action='DESELECT')
    principled_node.select = True
    bpy.context.view_layer.objects.active = obj

    # Call the operator. It requires the 'filepath' property to be set for the selected files.
    # The operator automatically detects map types based on common naming conventions.
    # Note: This part needs careful handling if running in a headless environment without actual files.
    # For a fully self-contained script without external file dependencies, you'd have to
    # create all these nodes and connections manually.
    try:
        # A common issue is the operator failing if the paths aren't exactly right or files don't exist.
        # This is the point where an agent might need actual local files or mock files.
        bpy.ops.node.principled_texture_setup(
            filepath=texture_files[0], # The first file is used to open the dialog
            files=[{"name": os.path.basename(f)} for f in texture_files],
            directory=pbr_texture_base_path # Important: Pass the directory to find other files
        )
    except Exception as e:
        print(f"Error running principled_texture_setup: {e}")
        print("Please ensure Node Wrangler is enabled and PBR texture files exist at the specified path.")
        return f"Failed to setup PBR material: Node Wrangler operator error - {e}"

    # Re-reference nodes after operator, as it creates new ones or moves them.
    # The operator often renames nodes, so we need to find them by type or by what they connect to.
    principled_node = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not principled_node:
        return "Failed to find Principled BSDF node after setup."

    # Adjust displacement settings
    disp_node = next((n for n in nodes if n.type == 'DISPLACEMENT'), None)
    if disp_node:
        disp_node.inputs['Midlevel'].default_value = 0.0 # Remove geometry offset
        disp_node.inputs['Scale'].default_value = displacement_scale

    # Adjust normal map strength
    normal_map_node = next((n for n in nodes if n.type == 'NORMAL_MAP'), None)
    if normal_map_node:
        normal_map_node.inputs['Strength'].default_value = normal_strength

    # === Step 3: Add Subdivision Surface Modifier for true displacement ===
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels
    subdiv_mod.subdivision_type = 'SIMPLE' # To preserve texture shape, as per video

    # Enable experimental feature set for adaptive subdivision
    if enable_adaptive_subdivision:
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
        subdiv_mod.use_adaptive_subdivision = True
        subdiv_mod.dicing_scale = dicing_scale
    
    # Configure material displacement settings for Cycles
    mat.cycles.displacement_method = 'DISPLACEMENT' # For true displacement (or 'DISPLACEMENT_BUMP')

    return f"Created '{object_name}' at {location} with PBR material setup. (Note: Requires PBR textures and Node Wrangler)."


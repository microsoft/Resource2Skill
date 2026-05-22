def create_pbr_material(
    scene_name: str = "Scene",
    object_name: str = "PBR_Plane",
    material_name: str = "MyPBRMaterial",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    pbr_folder_path: str = "C:/path/to/your/pbr_textures",  # IMPORTANT: Change this path!
    midlevel: float = 0.0,
    displacement_scale: float = 0.020,
    normal_strength: float = 1.0,
    subdivision_levels_viewport: int = 2,
    subdivision_levels_render: int = 4,
    use_adaptive_subdivision: bool = True,
    **kwargs,
) -> str:
    """
    Creates a new plane, sets up a PBR material using Node Wrangler's
    Principled Texture Setup, and applies it to the plane.
    Also configures a Subdivision Surface modifier and render settings for displacement.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        material_name: Name for the created PBR material.
        location: (x, y, z) world-space position for the plane.
        scale: Uniform scale factor for the plane.
        pbr_folder_path: Absolute path to the folder containing PBR texture images.
                         (e.g., 'C:/Users/YourName/Blender/Textures/BricksOldWhiteWashedRed001')
                         Texture files must follow Node Wrangler's naming conventions
                         (e.g., *_COL.jpg, *_GLOSS.jpg, *_NRM.png, *_DISP.jpg).
        midlevel: Midlevel value for the Displacement node (0.0 for no offset).
        displacement_scale: Scale for the Displacement node.
        normal_strength: Strength for the Normal Map node.
        subdivision_levels_viewport: Subdivision levels for viewport.
        subdivision_levels_render: Subdivision levels for render.
        use_adaptive_subdivision: Whether to enable adaptive subdivision (Cycles Experimental only).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_Plane' with material 'MyPBRMaterial'
        and PBR textures from 'C:/path/to/your/pbr_textures'"
    """
    import bpy
    import os
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 0. Check for Node Wrangler Add-on ---
    if not bpy.app.addon_utils.is_enabled("node_wrangler"):
        print("Node Wrangler add-on is not enabled. Please enable it in Preferences -> Add-ons.")
        return "Failed: Node Wrangler add-on not enabled."

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location, scale=(scale, scale, scale)
    )
    obj = bpy.context.active_object
    obj.name = object_name

    # --- 2. Create Material and Apply to Object ---
    mat = bpy.data.materials.get(material_name)
    if not mat:
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        # Clear default nodes (Principled BSDF and Material Output will be recreated)
        nodes = mat.node_tree.nodes
        for node in nodes:
            nodes.remove(node)
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # --- 3. Use Node Wrangler's Principled Texture Setup ---
    # This operator expects the Principled BSDF node to be selected.
    # It creates new nodes (Image Texture, Mapping, Texture Coordinate, Normal Map, Displacement)
    # and connects them appropriately based on common PBR naming conventions.

    # Add a Principled BSDF node
    principled_bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (200, 0)
    
    # Add a Material Output node
    material_output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (400, 0)
    
    # Link Principled BSDF to Material Output
    mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Select the Principled BSDF node for Node Wrangler
    principled_bsdf.select = True
    bpy.context.view_layer.objects.active = obj # Ensure object is active for context
    bpy.context.area.type = 'NODE_EDITOR' # Temporarily switch area to make operator context valid
    
    # Run Node Wrangler's PBR setup
    # This operator uses bpy.context.space_data.node_tree for its context.
    # To make it work reliably, we ensure the node_tree is the material's node_tree.
    current_node_tree = bpy.context.space_data.node_tree
    bpy.context.space_data.node_tree = mat.node_tree
    
    # Get all image files from the specified folder
    image_files = []
    if os.path.isdir(pbr_folder_path):
        for f in os.listdir(pbr_folder_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif')):
                image_files.append(os.path.join(pbr_folder_path, f))
    else:
        return f"Failed: PBR folder path '{pbr_folder_path}' is not a valid directory."

    if not image_files:
        return f"Failed: No image files found in '{pbr_folder_path}'."

    # Use Node Wrangler's principled texture setup operator
    bpy.ops.node.nw_principled_texture_setup(filepath=pbr_folder_path, check_existing=True, files=[{'name': os.path.basename(f)} for f in image_files])
    
    bpy.context.space_data.node_tree = current_node_tree # Restore original node tree context

    # --- 4. Adjust specific nodes added by Node Wrangler ---
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            if "_DISP" in node.image.name.upper():
                # Set Displacement node midlevel and scale
                if 'Displacement' in mat.node_tree.nodes:
                    disp_node = mat.node_tree.nodes['Displacement']
                    disp_node.inputs['Midlevel'].default_value = midlevel
                    disp_node.inputs['Scale'].default_value = displacement_scale
            elif "_NRM" in node.image.name.upper():
                # Set Normal Map node strength
                if 'Normal Map' in mat.node_tree.nodes:
                    normal_map_node = mat.node_tree.nodes['Normal Map']
                    normal_map_node.inputs['Strength'].default_value = normal_strength

    # --- 5. Configure Subdivision Surface Modifier for Displacement ---
    if obj.type == 'MESH':
        subdiv_mod = obj.modifiers.get("Subdivision")
        if not subdiv_mod:
            subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        
        subdiv_mod.render_levels = subdivision_levels_render
        subdiv_mod.levels = subdivision_levels_viewport
        subdiv_mod.quality = 3 # High quality for displacement
        subdiv_mod.subdivision_type = 'SIMPLE' # To preserve hard edges and not smooth the base mesh

    # --- 6. Set Render Settings for Cycles and Adaptive Subdivision ---
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'

    if use_adaptive_subdivision and subdiv_mod:
        subdiv_mod.use_adaptive_subdivision = True
        # Dicing scale is set globally in render properties, not per modifier
        bpy.context.scene.cycles.dicing_rate = 1.0 # Default value, can be overridden via kwargs if needed
        
        # Ensure shader uses displacement for Cycles
        if mat.cycles.displacement_method == 'BUMP':
             mat.cycles.displacement_method = 'DISPLACEMENT' # Or 'DISPLACEMENT_AND_BUMP'
             
        # Find Material Output node to set displacement method
        material_output_node = mat.node_tree.nodes.get("Material Output")
        if material_output_node:
            material_output_node.inputs["Displacement"]._set_value_from_vector((0,0,0,1)) # Trigger update for displacement


    # --- 7. Finalize ---
    bpy.ops.object.shade_smooth() # Optional: Smooth shading for the object

    return f"Created '{object_name}' with material '{material_name}' and PBR textures from '{pbr_folder_path}'"


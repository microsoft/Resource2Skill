def create_pbr_displaced_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    subdivision_levels: int = 4,
    texture_folder_path: str = "",
    sun_strength: float = 5.0,
    displacement_scale: float = 0.2,
    mid_level: float = 0.5,
    texture_base_name: str = "Rock_Wall_10", # Base name for Poly Haven textures
    **kwargs,
) -> str:
    """
    Create a plane with PBR textures and displacement in the active Blender scene.
    Assumes PBR textures (color, normal, roughness, displacement) are in
    texture_folder_path with standard Poly Haven naming conventions.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object (e.g., "RockWall").
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        subdivision_levels: Number of subdivision levels for the mesh.
                            Higher values yield finer displacement detail.
        texture_folder_path: Full path to the directory containing PBR textures.
                             e.g., "/path/to/textures/Rock_Wall_10/"
        sun_strength: Strength of the sun lamp used for lighting.
        displacement_scale: Scale factor for the displacement map.
        mid_level: Mid-level value for the displacement node.
        texture_base_name: The common prefix for the texture files
                           (e.g., "Rock_Wall_10" for "Rock_Wall_10_col.jpg").
        **kwargs: Additional overrides (currently none used).

    Returns:
        Status string, e.g., "Created 'RockWall_PBR' at (0, 0, 0) with PBR displacement"
    """
    import bpy
    from mathutils import Vector
    import os

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Plane) ===
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location, scale=(1, 1, 1)
    )
    plane_obj = bpy.context.active_object
    plane_obj.name = object_name

    # Apply uniform scale
    plane_obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels
    bpy.ops.object.shade_smooth() # Smooth shading for better visual

    # === Step 2: Build Material ===
    material_name = f"{object_name}_Material"
    if material_name in bpy.data.materials:
        mat = bpy.data.materials[material_name]
    else:
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True

    plane_obj.data.materials.clear()
    plane_obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF and Material Output nodes
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (0, 0)

    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (400, 0)

    # Connect Principled BSDF to Material Output
    links.new(principled_node.outputs['BSDF'], material_output.inputs['Surface'])

    # Create Texture Coordinate and Mapping nodes
    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    tex_coord_node.location = (-1000, 300)

    mapping_node = nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (-800, 300)

    links.new(tex_coord_node.outputs['UV'], mapping_node.inputs['Vector'])

    # Load PBR Textures
    if texture_folder_path and os.path.exists(texture_folder_path):
        def load_image_node(filepath, name, location, is_color=True):
            img = bpy.data.images.load(filepath)
            img_node = nodes.new(type='ShaderNodeTexImage')
            img_node.image = img
            img_node.location = location
            if not is_color:
                img_node.image.colorspace_settings.name = 'Non-Color'
            links.new(mapping_node.outputs['Vector'], img_node.inputs['Vector'])
            return img_node

        # Base Color (Albedo)
        col_path = os.path.join(texture_folder_path, f"{texture_base_name}_col.jpg")
        if os.path.exists(col_path):
            col_node = load_image_node(col_path, "Base Color", (-400, 400), is_color=True)
            links.new(col_node.outputs['Color'], principled_node.inputs['Base Color'])

        # Roughness Map
        rough_path = os.path.join(texture_folder_path, f"{texture_base_name}_rough.jpg")
        if os.path.exists(rough_path):
            rough_node = load_image_node(rough_path, "Roughness", (-400, 200), is_color=False)
            links.new(rough_node.outputs['Color'], principled_node.inputs['Roughness'])

        # Normal Map
        nrm_path = os.path.join(texture_folder_path, f"{texture_base_name}_nrm.jpg")
        if os.path.exists(nrm_path):
            nrm_img_node = load_image_node(nrm_path, "Normal Map Image", (-400, -50), is_color=False)
            normal_map_node = nodes.new(type='ShaderNodeNormalMap')
            normal_map_node.location = (-200, -50)
            links.new(nrm_img_node.outputs['Color'], normal_map_node.inputs['Color'])
            links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])

        # Displacement Map
        disp_path_exr = os.path.join(texture_folder_path, f"{texture_base_name}_disp.exr")
        disp_path_jpg = os.path.join(texture_folder_path, f"{texture_base_name}_disp.jpg")

        disp_path = disp_path_exr if os.path.exists(disp_path_exr) else disp_path_jpg

        if os.path.exists(disp_path):
            disp_img_node = load_image_node(disp_path, "Displacement Map Image", (-400, -300), is_color=False)
            displacement_node = nodes.new(type='ShaderNodeDisplacement')
            displacement_node.location = (-100, -300)
            displacement_node.inputs['Scale'].default_value = displacement_scale
            displacement_node.inputs['Midlevel'].default_value = mid_level
            links.new(disp_img_node.outputs['Color'], displacement_node.inputs['Height'])
            links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

    # Set material displacement settings for Cycles
    mat.cycles.displacement_method = 'DISPLACEMENT' # 'DISPLACEMENT_AND_BUMP' or 'DISPLACEMENT'
    # 'DISPLACEMENT' means true displacement only, 'DISPLACEMENT_AND_BUMP' means combine.
    # Tutorial suggests 'Displacement Only' in UI, which corresponds to 'DISPLACEMENT'
    # For more robust results, 'DISPLACEMENT_AND_BUMP' is often preferred to get fine details from normal map.
    # Let's stick to 'DISPLACEMENT' as shown in the video for strict reproduction.


    # === Step 3: Lighting & Rendering Context ===
    # Set render engine to Cycles
    scene.render.engine = 'CYCLES'
    # Use GPU if available
    if bpy.context.preferences.addons['cycles'].preferences.has_gpu_device:
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        scene.cycles.device = 'GPU'
        # Set all available GPUs
        for device in bpy.context.preferences.addons['cycles'].preferences.devices:
            device.use = True
    else:
        scene.cycles.device = 'CPU'

    # Add a Sun Light
    # Check if a sun light already exists, if so, modify it
    sun_obj = None
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'SUN':
            sun_obj = obj
            break

    if sun_obj is None:
        bpy.ops.object.light_add(type='SUN', location=(5, -5, 5))
        sun_obj = bpy.context.active_object
        sun_obj.name = f"{object_name}_Sun"
    else:
        sun_obj.location = (5, -5, 5) # Reposition existing sun light

    sun_obj.data.energy = sun_strength
    sun_obj.data.color = (1.0, 1.0, 1.0) # White light
    sun_obj.rotation_euler = (0.7, -0.7, 0.5) # Example rotation for angled light

    # Set background color (optional, but good for consistent renders)
    scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes["Background"]
    bg_node.inputs[0].default_value = (0.05, 0.05, 0.05, 1) # Dark grey background
    bg_node.inputs[1].default_value = 1.0 # Strength

    return f"Created '{object_name}' at {location} with PBR displacement and Sun light. " \
           f"Please ensure PBR textures are correctly named and located at: {texture_folder_path}"


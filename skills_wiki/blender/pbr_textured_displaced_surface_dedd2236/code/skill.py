def add_pbr_displaced_plane(
    object_name: str = "PBR_Rock_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    color_map_path: str = "",
    normal_map_path: str = "",
    roughness_map_path: str = "",
    displacement_map_path: str = "",
    subdivision_cuts: int = 50, # Number of subdivisions for displacement detail
    displacement_strength: float = 0.2,
    sun_strength: float = 5.0,
    use_gpu: bool = True,
    **kwargs,
) -> str:
    """
    Create a plane with PBR textures and true displacement in the active Blender scene.
    Assumes valid paths to PBR texture maps (Albedo, Normal, Roughness, Displacement).

    Args:
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        color_map_path: Full path to the Albedo/Color texture image file.
        normal_map_path: Full path to the Normal texture image file.
        roughness_map_path: Full path to the Roughness texture image file.
        displacement_map_path: Full path to the Displacement/Height texture image file.
        subdivision_cuts: Number of subdivisions to add to the plane for displacement detail.
                          Higher values increase detail but also memory usage and render time.
        displacement_strength: Scale factor for the displacement effect.
        sun_strength: Strength of the added Sun lamp.
        use_gpu: If True, attempts to set Cycles to use GPU compute if available.
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'PBR_Rock_Wall' at (0, 0, 0) with 1 object"
    """
    import bpy
    from mathutils import Vector
    import os

    scene = bpy.context.scene

    # --- 1. Configure Render Engine ---
    scene.render.engine = 'CYCLES'
    if use_gpu:
        try:
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' # or 'OPTIX', 'HIP'
            scene.cycles.device = 'GPU'
            print("Cycles device set to GPU.")
        except:
            print("Failed to set Cycles device to GPU. Falling back to CPU.")
            scene.cycles.device = 'CPU'
    else:
        scene.cycles.device = 'CPU'
    bpy.context.preferences.addons['cycles'].preferences.get_devices() # Update device list


    # --- 2. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location)
    plane_obj = bpy.context.object
    plane_obj.name = object_name
    plane_obj.scale = (scale, scale, scale)

    # Subdivide the plane for displacement detail
    bpy.context.view_layer.objects.active = plane_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=subdivision_cuts)
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- 3. Create Material and Node Tree ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    plane_obj.data.materials.append(material)

    node_tree = material.node_tree
    # Clear existing nodes to start fresh (Principle BSDF and Material Output are kept)
    for node in node_tree.nodes:
        if node.type != 'BSDF_PRINCIPLED' and node.type != 'OUTPUT_MATERIAL':
            node_tree.nodes.remove(node)

    principled_node = node_tree.nodes.get("Principled BSDF")
    output_node = node_tree.nodes.get("Material Output")

    # Set material settings for displacement
    material.cycles.displacement_method = 'DISPLACEMENT_ONLY'

    # Function to add image texture node
    def add_image_texture(filepath, color_space='sRGB', location=(0,0)):
        if not os.path.exists(filepath):
            print(f"Warning: Texture file not found: {filepath}")
            return None
        img_node = node_tree.nodes.new(type='SHADER_NODE_TEX_IMAGE')
        img_node.image = bpy.data.images.load(filepath, check_existing=True)
        img_node.image.colorspace_settings.name = color_space
        img_node.location = location
        return img_node

    # Add Color Map
    if color_map_path:
        color_node = add_image_texture(color_map_path, 'sRGB', (-800, 300))
        if color_node:
            node_tree.links.new(color_node.outputs['Color'], principled_node.inputs['Base Color'])

    # Add Roughness Map
    if roughness_map_path:
        rough_node = add_image_texture(roughness_map_path, 'Non-Color', (-800, 0))
        if rough_node:
            node_tree.links.new(rough_node.outputs['Color'], principled_node.inputs['Roughness'])

    # Add Normal Map
    if normal_map_path:
        normal_img_node = add_image_texture(normal_map_path, 'Non-Color', (-800, -300))
        if normal_img_node:
            normal_map_node = node_tree.nodes.new(type='SHADER_NODE_NORMAL_MAP')
            normal_map_node.location = (-400, -300)
            node_tree.links.new(normal_img_node.outputs['Color'], normal_map_node.inputs['Color'])
            node_tree.links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])

    # Add Displacement Map
    if displacement_map_path:
        disp_img_node = add_image_texture(displacement_map_path, 'Non-Color', (-800, -600))
        if disp_img_node:
            disp_node = node_tree.nodes.new(type='SHADER_NODE_DISPLACEMENT')
            disp_node.location = (-400, -600)
            disp_node.inputs['Midlevel'].default_value = 0.5 # Standard for displacement maps
            disp_node.inputs['Scale'].default_value = displacement_strength
            node_tree.links.new(disp_img_node.outputs['Color'], disp_node.inputs['Height'])
            node_tree.links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    # --- 4. Add a Sun Light ---
    sun_name = f"{object_name}_Sun"
    bpy.ops.object.light_add(type='SUN', location=(location[0] + scale * 2, location[1] + scale * 2, location[2] + scale * 3))
    sun_light = bpy.context.object
    sun_light.name = sun_name
    sun_light.data.energy = sun_strength
    sun_light.rotation_euler = (math.radians(30), math.radians(45), math.radians(0)) # Angle the sun for good shadows

    return f"Created '{object_name}' at {location} with PBR material and displacement"


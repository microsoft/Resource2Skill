def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_paths: dict = None,
    subdivision_levels: int = 4, # Higher for more displacement detail
    displacement_scale: float = 0.2, # Adjust displacement strength
    sun_strength: float = 5.0,
    use_gpu: bool = True,
    **kwargs,
) -> str:
    """
    Create a plane with PBR textures and true displacement in the active Blender scene.
    Requires texture file paths for Base Color, Roughness, Normal, and Displacement.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position for the plane.
        scale: Uniform scale factor for the plane.
        texture_paths: A dictionary containing paths to PBR textures.
                       Expected keys: 'diffuse', 'roughness', 'normal', 'displacement'.
                       Example: {'diffuse': '/path/to/diffuse.jpg', ...}
        subdivision_levels: Number of subdivision levels for the Subdivision Surface modifier.
                            Higher values provide more detail for displacement.
        displacement_scale: The strength of the displacement effect.
        sun_strength: Strength of the sun lamp to illuminate the scene.
        use_gpu: Whether to try and use GPU for Cycles rendering.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_Displacement_Plane' at (0, 0, 0)"
    """
    import bpy
    from mathutils import Vector

    if texture_paths is None:
        return "Error: texture_paths dictionary is required with keys 'diffuse', 'roughness', 'normal', 'displacement'."

    required_textures = ['diffuse', 'roughness', 'normal', 'displacement']
    for key in required_textures:
        if key not in texture_paths or not texture_paths[key]:
            return f"Error: Missing texture path for '{key}'."

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Setup Render Engine to Cycles ---
    scene.render.engine = 'CYCLES'
    if use_gpu:
        try:
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' # or 'OPTIX', 'HIP', 'METAL'
            bpy.context.preferences.addons['cycles'].preferences.get_devices()
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                d.use = False
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                if d.type == 'GPU':
                    d.use = True
                    break
            scene.cycles.device = 'GPU'
        except Exception as e:
            print(f"Warning: Could not enable GPU for Cycles. Falling back to CPU. Error: {e}")
            scene.cycles.device = 'CPU'
    else:
        scene.cycles.device = 'CPU'

    # --- Add a Sun Light ---
    # Delete existing sun light if it exists to avoid duplicates in subsequent calls
    existing_sun = scene.objects.get("Sun_Light")
    if existing_sun:
        bpy.data.objects.remove(existing_sun, do_unlink=True)

    bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
    sun_obj = bpy.context.object
    sun_obj.name = "Sun_Light"
    sun_obj.data.strength = sun_strength
    sun_obj.data.angle = math.radians(11.47) # Angle from video for soft shadows
    sun_obj.rotation_euler = (math.radians(30), math.radians(-30), math.radians(0)) # Example rotation

    # --- Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane_obj = bpy.context.object
    plane_obj.name = object_name
    plane_obj.location = Vector(location)
    plane_obj.scale = (scale, scale, scale)

    # --- Add Subdivision Surface Modifier ---
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels
    bpy.ops.object.shade_smooth() # Apply smooth shading

    # --- Create Material and Node Setup ---
    mat_name = f"{object_name}_Material"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True

    plane_obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF and Material Output
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (0, 0)

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # --- Add PBR Texture Nodes ---

    # Diffuse/Albedo
    diffuse_tex = nodes.new(type='ShaderNodeTexImage')
    diffuse_tex.image = bpy.data.images.load(texture_paths['diffuse'])
    diffuse_tex.location = (-800, 300)
    links.new(diffuse_tex.outputs['Color'], principled_node.inputs['Base Color'])

    # Roughness
    roughness_tex = nodes.new(type='ShaderNodeTexImage')
    roughness_tex.image = bpy.data.images.load(texture_paths['roughness'])
    roughness_tex.image.colorspace_settings.name = 'Non-Color'
    roughness_tex.location = (-800, 100)
    links.new(roughness_tex.outputs['Color'], principled_node.inputs['Roughness'])

    # Normal Map
    normal_map_tex = nodes.new(type='ShaderNodeTexImage')
    normal_map_tex.image = bpy.data.images.load(texture_paths['normal'])
    normal_map_tex.image.colorspace_settings.name = 'Non-Color'
    normal_map_tex.location = (-800, -100)

    normal_map_node = nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.location = (-200, -100)
    links.new(normal_map_tex.outputs['Color'], normal_map_node.inputs['Color'])
    links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])

    # Displacement/Height Map
    displacement_tex = nodes.new(type='ShaderNodeTexImage')
    displacement_tex.image = bpy.data.images.load(texture_paths['displacement'])
    displacement_tex.image.colorspace_settings.name = 'Non-Color'
    displacement_tex.location = (-800, -300)

    displacement_node = nodes.new(type='ShaderNodeDisplacement')
    displacement_node.inputs['Scale'].default_value = displacement_scale
    displacement_node.location = (200, -300)
    links.new(displacement_tex.outputs['Color'], displacement_node.inputs['Height'])
    links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

    # --- Enable True Displacement in Material Settings ---
    mat.cycles.displacement_method = 'DISPLACEMENT' # or 'DISPLACEMENT_AND_BUMP'

    return f"Created '{object_name}' at {location} with PBR material and displacement."


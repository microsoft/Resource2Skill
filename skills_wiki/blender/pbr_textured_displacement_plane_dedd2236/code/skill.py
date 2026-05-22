def create_pbr_textured_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Textured_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    albedo_path: str = "",
    normal_path: str = "",
    roughness_path: str = "",
    displacement_path: str = "",
    displacement_scale: float = 0.2,
    subdivision_levels: int = 5,
    uv_scale: float = 1.0,
    sun_strength: float = 5.0,
    sun_direction: tuple = (45, 0, 45), # Euler angles in degrees
    **kwargs,
) -> str:
    """
    Create a plane with PBR textures and true displacement in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        albedo_path: Absolute path to the albedo/base color texture image (e.g., "C:/Textures/rock_albedo.png").
        normal_path: Absolute path to the normal map texture image (e.g., "C:/Textures/rock_normal.png").
        roughness_path: Absolute path to the roughness texture image (e.g., "C:/Textures/rock_roughness.png").
        displacement_path: Absolute path to the displacement/height map texture image (e.g., "C:/Textures/rock_disp.png").
        displacement_scale: Scale factor for the displacement effect (default 0.2).
        subdivision_levels: Number of subdivision levels for the plane's geometry (default 5).
        uv_scale: Scale factor for the UV mapping of all textures (default 1.0).
        sun_strength: Strength of the added/modified sun lamp (default 5.0).
        sun_direction: (x, y, z) Euler angles in degrees for the sun lamp's rotation (default 45, 0, 45).
        **kwargs: Additional overrides (currently none specific).

    Returns:
        Status string, e.g., "Created 'PBR_Textured_Plane' at (0, 0, 0) with PBR material and displacement."
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Set up Render Engine (Cycles for Displacement) ---
    scene.render.engine = 'CYCLES'
    # Optional: Enable GPU compute if available, as shown in the video context
    try:
        if hasattr(bpy.context.preferences.addons['cycles'].preferences, 'compute_device_type'):
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' # or 'OPTIX'
            bpy.context.preferences.addons['cycles'].preferences.get_devices()
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                if d.type == 'CUDA' or d.type == 'OPTIX':
                    d.use = True
                else:
                    d.use = False
    except Exception:
        pass # Fallback to CPU if GPU not available or setup fails

    # --- 2. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane_obj = bpy.context.object
    plane_obj.name = object_name
    plane_obj.location = Vector(location)
    plane_obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for displacement
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.render_levels = subdivision_levels
    subdiv_mod.levels = subdivision_levels # For viewport
    subdiv_mod.subdivision_type = 'CATMULL_CLARK'

    # --- 3. Build Material with PBR Textures ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    plane_obj.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes for a clean setup (mimics Node Wrangler's fresh setup)
    for node in nodes:
        nodes.remove(node)

    # Create new Principled BSDF and Material Output nodes
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.location = (0, 0)

    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.name = "Material Output"
    material_output.location = (400, 0)

    # Link Principled BSDF to Material Output
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Add Texture Coordinate and Mapping nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 200)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.vector_type = 'TEXTURE'
    mapping.location = (-800, 200)

    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Set UV scale
    mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, uv_scale)

    # --- Load and connect PBR textures (if paths provided) ---
    # Albedo Texture
    if albedo_path:
        try:
            albedo_image = bpy.data.images.load(albedo_path, check_existing=True)
            albedo_tex = nodes.new('ShaderNodeTexImage')
            albedo_tex.image = albedo_image
            albedo_tex.location = (-400, 300)
            links.new(mapping.outputs['Vector'], albedo_tex.inputs['Vector'])
            links.new(albedo_tex.outputs['Color'], principled_bsdf.inputs['Base Color'])
        except RuntimeError:
            print(f"Warning: Could not load albedo texture from {albedo_path}. Please check the path.")

    # Roughness Texture
    if roughness_path:
        try:
            roughness_image = bpy.data.images.load(roughness_path, check_existing=True)
            roughness_tex = nodes.new('ShaderNodeTexImage')
            roughness_tex.image = roughness_image
            roughness_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            roughness_tex.location = (-400, 100)
            links.new(mapping.outputs['Vector'], roughness_tex.inputs['Vector'])
            links.new(roughness_tex.outputs['Color'], principled_bsdf.inputs['Roughness'])
        except RuntimeError:
            print(f"Warning: Could not load roughness texture from {roughness_path}. Please check the path.")

    # Normal Map Texture
    if normal_path:
        try:
            normal_image = bpy.data.images.load(normal_path, check_existing=True)
            normal_tex = nodes.new('ShaderNodeTexImage')
            normal_tex.image = normal_image
            normal_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            normal_tex.location = (-400, -100)
            
            normal_map_node = nodes.new('ShaderNodeNormalMap')
            normal_map_node.location = (-200, -100)
            
            links.new(mapping.outputs['Vector'], normal_tex.inputs['Vector'])
            links.new(normal_tex.outputs['Color'], normal_map_node.inputs['Color'])
            links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
        except RuntimeError:
            print(f"Warning: Could not load normal texture from {normal_path}. Please check the path.")

    # Displacement Texture
    if displacement_path:
        try:
            displacement_image = bpy.data.images.load(displacement_path, check_existing=True)
            displacement_tex = nodes.new('ShaderNodeTexImage')
            displacement_tex.image = displacement_image
            displacement_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            displacement_tex.location = (-400, -300)
            
            displacement_node = nodes.new('ShaderNodeDisplacement')
            displacement_node.location = (200, -300)
            
            displacement_node.inputs['Scale'].default_value = displacement_scale
            # Midlevel default 0.5 is suitable for standard height maps where 50% gray is zero displacement.
            
            links.new(mapping.outputs['Vector'], displacement_tex.inputs['Vector'])
            links.new(displacement_tex.outputs['Color'], displacement_node.inputs['Height'])
            links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
            
            # Set material displacement method to 'Displacement Only' as shown in the video
            material.cycles.displacement_method = 'DISPLACEMENT'
        except RuntimeError:
            print(f"Warning: Could not load displacement texture from {displacement_path}. Please check the path.")
    else:
        # If no displacement path is provided, ensure displacement is not active
        material.cycles.displacement_method = 'BUMP' # Default to bump only if no displacement map

    # --- 4. Lighting (Sun Lamp) ---
    # Attempt to find an existing sun light to modify, otherwise create a new one.
    sun_light_obj = None
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'SUN':
            sun_light_obj = obj
            break
    
    if sun_light_obj is None:
        # No sun light found, create one
        bpy.ops.object.light_add(type='SUN', location=(0,0,0)) # Position at origin for easier rotation
        sun_light_obj = bpy.context.object
        sun_light_obj.name = f"{object_name}_Sun"
    else:
        print(f"Modifying existing sun light: '{sun_light_obj.name}'")

    sun_light_obj.data.energy = sun_strength
    sun_light_obj.rotation_euler = (math.radians(sun_direction[0]), math.radians(sun_direction[1]), math.radians(sun_direction[2]))

    # Set viewport shading to rendered to immediately see the effect (optional)
    # This part depends on context (e.g., if there's an active 3D view)
    # for area in bpy.context.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         for space in area.spaces:
    #             if space.type == 'VIEW_3D':
    #                 space.shading.type = 'RENDERED'
    #                 break
    #         break

    return f"Created '{object_name}' at {location} with PBR material and displacement."


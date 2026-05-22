def create_pbr_rock_wall(
    scene_name: str = "Scene",
    object_name: str = "PBR_RockWall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_paths: dict = None, # Expects {'albedo':..., 'roughness':..., 'normal':..., 'displacement':...}
    subdivision_cuts: int = 5, # Number of cuts for subdividing the base plane (e.g., 5 for 32x32 faces)
    displacement_scale: float = 0.2, # Scale for the displacement effect
    light_strength: float = 5.0, # Strength of the added Sun light
    **kwargs,
) -> str:
    """
    Create a PBR-textured rock wall plane with displacement in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position for the plane.
        scale: Uniform scale factor for the plane (1.0 = default 2m size).
        texture_paths: Dictionary with paths to PBR textures (albedo, roughness, normal, displacement).
                       Example: {'albedo': 'path/to/rock_col.jpg', 'roughness': 'path/to/rock_rough.jpg', ...}
        subdivision_cuts: Number of cuts for subdividing the plane (e.g., 5 for 32x32 faces).
        displacement_scale: Scale for the displacement effect (default 0.2).
        light_strength: Strength of the added Sun light (default 5.0).
        **kwargs: Additional overrides (e.g., normal_map_strength=1.0).

    Returns:
        Status string, e.g., "Created 'PBR_RockWall' at (0, 0, 0) with PBR textures and displacement."
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Validate texture_paths
    if texture_paths is None:
        return "Error: texture_paths dictionary is required with 'albedo', 'roughness', 'normal', 'displacement' keys."
    required_textures = ['albedo', 'roughness', 'normal', 'displacement']
    if not all(key in texture_paths for key in required_textures):
        return f"Error: texture_paths must contain keys for {', '.join(required_textures)}."

    # --- Step 1: Create Base Geometry (Plane) ---
    # Create at origin first, then apply location/scale
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0,0,0))
    plane_obj = bpy.context.active_object
    plane_obj.name = object_name

    # Apply scaling
    plane_obj.scale = (scale, scale, scale)
    # Apply location
    plane_obj.location = Vector(location)

    # Ensure object is selected and active for subdivision
    bpy.ops.object.select_all(action='DESELECT')
    plane_obj.select_set(True)
    bpy.context.view_layer.objects.active = plane_obj

    # Subdivide the plane for displacement
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=subdivision_cuts)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Shade smooth for better visual interpolation of displaced mesh
    bpy.ops.object.shade_smooth()


    # --- Step 2: Build Material with PBR Textures and Displacement ---
    mat_name = f"{object_name}_Material"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # Assign material to the plane
    if len(plane_obj.data.materials) == 0:
        plane_obj.data.materials.append(mat)
    else:
        plane_obj.data.materials[0] = mat # Replace existing material if any

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear existing nodes for a clean setup (useful if material already existed)
    for node in nodes:
        nodes.remove(node)

    # Create core shader nodes
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    displacement_node = nodes.new(type='ShaderNodeDisplacement')
    normal_map_node = nodes.new(type='ShaderNodeNormalMap')

    # Position nodes for better readability in Shader Editor (optional)
    principled_node.location = (0, 0)
    material_output.location = (400, 0)
    displacement_node.location = (0, -300)
    normal_map_node.location = (-300, 0)

    # Load and link Albedo (Base Color) texture
    albedo_tex = nodes.new(type='ShaderNodeTexImage')
    albedo_tex.image = bpy.data.images.load(texture_paths['albedo'])
    albedo_tex.image.colorspace_settings.name = 'sRGB'
    albedo_tex.location = (-800, 300)
    links.new(albedo_tex.outputs['Color'], principled_node.inputs['Base Color'])

    # Load and link Roughness texture
    roughness_tex = nodes.new(type='ShaderNodeTexImage')
    roughness_tex.image = bpy.data.images.load(texture_paths['roughness'])
    roughness_tex.image.colorspace_settings.name = 'Non-Color'
    roughness_tex.location = (-800, 100)
    links.new(roughness_tex.outputs['Color'], principled_node.inputs['Roughness'])

    # Load and link Normal Map texture
    normal_tex = nodes.new(type='ShaderNodeTexImage')
    normal_tex.image = bpy.data.images.load(texture_paths['normal'])
    normal_tex.image.colorspace_settings.name = 'Non-Color'
    normal_tex.location = (-800, -100)
    links.new(normal_tex.outputs['Color'], normal_map_node.inputs['Color'])
    links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
    normal_map_node.inputs['Strength'].default_value = kwargs.get('normal_map_strength', 1.0) # Allow adjusting normal map strength

    # Load and link Displacement Map texture
    displacement_tex = nodes.new(type='ShaderNodeTexImage')
    displacement_tex.image = bpy.data.images.load(texture_paths['displacement'])
    displacement_tex.image.colorspace_settings.name = 'Non-Color'
    displacement_tex.location = (-800, -500)
    links.new(displacement_tex.outputs['Color'], displacement_node.inputs['Height'])
    
    displacement_node.inputs['Scale'].default_value = displacement_scale
    displacement_node.inputs['Midlevel'].default_value = 0.5 # Standard for grayscale height maps from Poly Haven

    # Final connections to Material Output
    links.new(principled_node.outputs['BSDF'], material_output.inputs['Surface'])
    links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

    # Enable Displacement in Material Settings (as explicitly set in the video tutorial)
    mat.cycles.displacement_method = 'DISPLACEMENT_ONLY'

    # --- Step 3: Lighting Setup (Optional but good for demo) ---
    # Add a Sun light to illuminate the displaced texture clearly
    sun_name = f"{object_name}_SunLight"
    sun_light_data = bpy.data.lights.new(name=sun_name, type='SUN')
    sun_light_obj = bpy.data.objects.new(name=sun_name, object_data=sun_light_data)
    scene.collection.objects.link(sun_light_obj)

    # Position the sun light relative to the plane, and rotate it for a good angle
    sun_light_obj.location = Vector((location[0] + 5*scale, location[1] - 5*scale, location[2] + 5*scale)) # Offset from plane
    sun_light_obj.rotation_euler = (math.radians(-45), math.radians(0), math.radians(45)) # Top-left light angle
    sun_light_data.energy = light_strength
    sun_light_data.angle = math.radians(10) # Soften shadows, default is 0.

    # --- Step 4: Set Render Engine (Cycles) ---
    scene.render.engine = 'CYCLES'
    
    # Try to set Cycles to use GPU compute if available for better performance
    try:
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        if cycles_prefs.compute_device_type == 'NONE':
            for device_type in ('OPTIX', 'CUDA', 'OPENCL'):
                if device_type in cycles_prefs.get_devices():
                    cycles_prefs.compute_device_type = device_type
                    bpy.context.scene.cycles.device = 'GPU'
                    break
    except Exception:
        pass # Ignore if Cycles addon not found or device setup fails

    return f"Created '{object_name}' at {location} with PBR rock wall textures and displacement. A Sun light '{sun_name}' was added. Render engine set to Cycles."
